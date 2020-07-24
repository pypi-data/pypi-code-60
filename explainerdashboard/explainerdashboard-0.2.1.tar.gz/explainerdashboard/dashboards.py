# -*- coding: utf-8 -*-

__all__ = ['ExplainerTabsLayout',
            'ExplainerPageLayout',
            'ExplainerDashboard', 
            'JupyterExplainerDashboard',
            'ExplainerTab',
            'JupyterExplainerTab',
            'InlineExplainer']

import inspect 
import requests

import shortuuid
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from jupyter_dash import JupyterDash

import plotly.io as pio

from .dashboard_components import *
from .dashboard_tabs import *


def instantiate_component(component, explainer, **kwargs):
    """Returns an instantiated ExplainerComponent.
    If the component input is just a class definition, instantiate it with
    explainer and k**wargs.
    If it is already an ExplainerComponent instance then return it.
    If it is any other instance with layout and register_components methods,
    then add a name property and return it. 

    Args:
        component ([type]): Either a class definition or instance
        explainer ([type]): An Explainer object that will be used to instantiate class definitions
        kwargs: kwargs will be passed on to the instance

    Raises:
        ValueError: if component is not a subclass or instance of ExplainerComponent,
                or is an instance without layout and register_callbacks methods

    Returns:
        [type]: instantiated component
    """

    if inspect.isclass(component) and issubclass(component, ExplainerComponent):
        return component(explainer,  **kwargs)
    elif isinstance(component, ExplainerComponent):
        return component
    elif (not inspect.isclass(component)
          and hasattr(component, "layout")):
        if not (hasattr(component, "name") and isinstance(component.name, str)):
            component_name = shortuuid.ShortUUID().random(length=10)
            print(f"Warning: setting {component}.name to {component_name}")
            component.name = component_name
        if not hasattr(component, "title"):
            print(f"Warning: setting {component}.title to 'CustomTab'")
            component.title = "Custom"
        return component
    else:
        raise ValueError(f"{component} is not a valid component...")


class ExplainerTabsLayout:
    def __init__(self, explainer, tabs,
                 title='Model Explainer',
                 hide_title=False,
                 hide_selector=False,
                 block_selector_callbacks=False,
                 pos_label=None,
                 fluid=True,
                 **kwargs):
        """Generates a multi tab layout from a a list of ExplainerComponents.
        If the component is a class definition, it gets instantiated first. If 
        the component is not derived from an ExplainerComponent, then attempt
        with duck typing to nevertheless instantiate a layout.

        Args:
            explainer ([type]): explainer
            tabs (list[ExplainerComponent class or instance]): list of
                ExplainerComponent class definitions or instances.
            title (str, optional): [description]. Defaults to 'Model Explainer'.
            hide_title (bool, optional): Hide the title. Defaults to False.
            hide_selector (bool, optional): Hide the positive label selector. 
                        Defaults to False.
            block_selector_callbacks (bool, optional): block the callback of the
                        pos label selector. Useful to avoid clashes when you
                        have your own PosLabelSelector in your layout. 
                        Defaults to False.
            pos_label ({int, str}, optional): initial pos label. 
                        Defaults to explainer.pos_label
            fluid (bool, optional): Stretch layout to fill space. Defaults to False.
        """
        self.title = title
        self.hide_title = hide_title
        self.hide_selector = hide_selector
        self.block_selector_callbacks = block_selector_callbacks
        if self.block_selector_callbacks:
            self.hide_selector = True
        self.fluid = fluid
        
        self.selector = PosLabelSelector(explainer, pos_label=pos_label)
        self.tabs  = [instantiate_component(tab, explainer, **kwargs) for tab in tabs]
        assert len(self.tabs) > 0, 'When passing a list to tabs, need to pass at least one valid tab!'

        self.connector = PosLabelConnector(self.selector, self.tabs)
   
    def layout(self):
        """returns a multitab layout plus ExplainerHeader"""
        return dbc.Container([
            dbc.Row([
                make_hideable(
                    dbc.Col([
                        html.H1(self.title)
                    ], width="auto"), hide=self.hide_title),
                make_hideable(
                    dbc.Col([
                        self.selector.layout()
                    ], md=3), hide=self.hide_selector),
            ], justify="start"),
            dcc.Tabs(id="tabs", value=self.tabs[0].name, 
                        children=[dcc.Tab(label=tab.title, id=tab.name, value=tab.name,
                                        children=tab.layout()) for tab in self.tabs]),
        ], fluid=self.fluid)

    def register_callbacks(self, app):
        """Registers callbacks for all tabs"""
        for tab in self.tabs:
            try:
                tab.register_callbacks(app)
            except AttributeError:
                print(f"Warning: {tab} does not have a register_callbacks method!")
                
        if not self.block_selector_callbacks:
            if any([tab.has_pos_label_connector() for tab in self.tabs]):
                print("Warning: detected PosLabelConnectors already in the layout. "
                    "This may clash with the global pos label selector and generate duplicate callback errors. "
                    "If so set block_selector_callbacks=True.")
            self.connector.register_callbacks(app)

    def calculate_dependencies(self):
        """Calculates dependencies for all tabs"""
        for tab in self.tabs:
            try:
                tab.calculate_dependencies()
            except AttributeError:
                print(f"Warning: {tab} does not have a calculate_dependencies method!")


class ExplainerPageLayout(ExplainerComponent):
    def __init__(self, explainer, component,
                 title='Model Explainer',
                 hide_title=False,
                 hide_selector=False,
                 block_selector_callbacks=False,
                 pos_label=None,
                 fluid=False,
                 **kwargs):
        """Generates a single page layout from a single ExplainerComponent.
        If the component is a class definition, it gets instantiated. 

        If the component is not derived from an ExplainerComponent, then tries
        with duck typing to nevertheless instantiate a layout.


        Args:
            explainer ([type]): explainer
            component (ExplainerComponent class or instance): ExplainerComponent 
                        class definition or instance.
            title (str, optional): [description]. Defaults to 'Model Explainer'.
            hide_title (bool, optional): Hide the title. Defaults to False.
            hide_selector (bool, optional): Hide the positive label selector.
                        Defaults to False.
            block_selector_callbacks (bool, optional): block the callback of the
                        pos label selector. Useful to avoid clashes when you
                        have your own PosLabelSelector in your layout. 
                        Defaults to False.
            pos_label ({int, str}, optional): initial pos label. 
                        Defaults to explainer.pos_label
            fluid (bool, optional): Stretch layout to fill space. Defaults to False.
        """
        self.title = title
        self.hide_title = hide_title
        self.hide_selector = hide_selector
        self.block_selector_callbacks = block_selector_callbacks
        if self.block_selector_callbacks:
            self.hide_selector = True
        self.fluid = fluid
        
        self.selector = PosLabelSelector(explainer, pos_label=pos_label)
        self.page  = instantiate_component(component, explainer, **kwargs) 
        self.connector = PosLabelConnector(self.selector, self.page)
        
        self.fluid = fluid
        
    def layout(self):
        """returns single page layout with an ExplainerHeader"""
        return dbc.Container([
            dbc.Row([
                make_hideable(
                    dbc.Col([
                        html.H1(self.title)
                    ], width="auto"), hide=self.hide_title),
                make_hideable(
                    dbc.Col([
                        self.selector.layout()
                    ], md=3), hide=self.hide_selector),
            ], justify="start"),
            self.page.layout()
        ], fluid=self.fluid)

    def register_callbacks(self, app):
        """Register callbacks of page"""
        try:
            self.page.register_callbacks(app)
        except AttributeError:
            print(f"Warning: {self.page} does not have a register_callbacks method!")
        if not self.block_selector_callbacks:
            if hasattr(self.page, "has_pos_label_connector") and self.page.has_pos_label_connector():
                print("Warning: detected PosLabelConnectors already in the layout. "
                    "This may clash with the global pos label selector and generate duplicate callback errors. "
                    "If so set block_selector_callbacks=True.")
            self.connector.register_callbacks(app)

    def calculate_dependencies(self):
        """Calculate dependencies of page"""
        try:
            self.page.calculate_dependencies()
        except AttributeError:
            print(f"Warning: {self.page} does not have a calculate_dependencies method!")


class ExplainerDashboard:
    def __init__(self, explainer=None, tabs=None,
                 title='Model Explainer',
                 hide_header=False,
                 header_hide_title=False,
                 header_hide_selector=False,
                 block_selector_callbacks=False,
                 pos_label=None,
                 fluid=True,
                 mode="dash",
                 width=1000,
                 height=800,
                 external_stylesheets=None,
                 server=True,
                 url_base_pathname=None,
                 importances=True,
                 model_summary=True,
                 contributions=True,
                 shap_dependence=True,
                 shap_interaction=True,
                 decision_trees=True,
                 **kwargs):
        """Creates an explainerdashboard out of an Explainer object.


        single page dashboard:
            If tabs is a single ExplainerComponent class or instance, display it 
            as a standalone page without tabs.

        Multi tab dashboard:
            If tabs is a list of ExplainerComponent classes or instances, then construct
            a layout with a tab per component. Instead of components you can also pass
            the following strings: "importances", "model_summary", "contributions", 
            "shap_dependence", "shap_interaction" or "decision_trees". You can mix and
            combine these different modularities, e.g.: 
                tabs=[ImportancesTab, "contributions", custom_tab]

        If tabs is None, then construct tabs based on the boolean parameters:
            importances, model_summary, contributions, shap_dependence, 
            shap_interaction and decision_trees, which all default to True.

        You can select four different modes:
            - 'dash': standard dash.Dash() app
            - 'inline': JupyterDash app inline in a notebook cell output
            - 'jupyterlab': JupyterDash app in jupyterlab pane
            - 'external': JupyterDash app in external tab

        You can switch off the title and positive label selector
            with header_hide_title=True and header_hide_selector=True.

        You run the dashboard
            with e.g. ExplainerDashboard(explainer).run(port=8050)


        Args:
            explainer(): explainer object
            tabs(): single component or list of components
            title(str, optional): title of dashboard, defaults to 'Model Explainer'
            hide_header (bool, optional) hide the header (title+selector), defaults to False.
            header_hide_title(bool, optional): hide the title, defaults to False
            header_hide_selector(bool, optional): hide the positive class selector for classifier models, defaults, to False
            block_selector_callbacks (bool, optional): block the callback of the
                        pos label selector. Useful to avoid clashes when you
                        have your own PosLabelSelector in your layout. 
                        Defaults to False.
            pos_label ({int, str}, optional): initial pos label. 
                        Defaults to explainer.pos_label
            mode(str, {'dash', 'inline' , 'jupyterlab', 'external'}, optional): 
                type of dash server to start. 'inline' runs in a jupyter notebook output cell. 
                'jupyterlab' runs in a jupyterlab pane. 'external' runs in an external tab
                while keeping the notebook interactive. 
            fluid(bool, optional): whether to stretch the layout to available space.
                    Defaults to True.
            width(int, optional): width of notebook output cell in pixels, defaults to 1000.
            height(int, optional): height of notebookn output cell in pixels, defaults to 800.
            external_stylesheets(list, optional): attach dbc themes e.g. 
                `external_stylesheets=[dbc.themes.FLATLY]`. 
            importances(bool, optional): include ImportancesTab, defaults to True.
            model_summary(bool, optional): include ModelSummaryTab, defaults to True.
            contributions(bool, optional): include ContributionsTab, defaults to True.
            shap_dependence(bool, optional): include ShapDependenceTab, defaults to True.
            shap_interaction(bool, optional): include InteractionsTab if model allows it, defaults to True.
            decision_trees(bool, optional): include DecisionTreesTab if model allows it, defaults to True.
        """
        if hide_header:
            header_hide_title = True
            header_hide_selector = True
        self.mode, self.width, self.height = mode, width, height
        self.hide_header, self.header_hide_title, self.header_hide_selector = \
            hide_header, header_hide_title, header_hide_selector
        self.external_stylesheets = external_stylesheets
        self.server, self.url_base_pathname = server, url_base_pathname
        
        self.app = self._get_dash_app()
        self.app.title = title
        
        if tabs is None:
            tabs = []
            if shap_interaction and not explainer.interactions_should_work:
                print("For this type of model and model_output interactions don't "
                          "work, so setting shap_interaction=False...")
                shap_interaction = False
            if decision_trees and not hasattr(explainer, 'decision_trees'):
                print("the explainer object has no decision_trees property. so "
                        "setting decision_trees=False...")
                decision_trees = False
        
            if importances:
                tabs.append(ImportancesTab)
            if model_summary:
                tabs.append(ModelSummaryTab)
            if contributions:
                tabs.append(ContributionsTab)
            if shap_dependence:
                tabs.append(ShapDependenceTab)
            if shap_interaction:
                tabs.append(ShapInteractionsTab)
            if decision_trees:
                tabs.append(DecisionTreesTab)

        if isinstance(tabs, list) and len(tabs)==1:
            tabs = tabs[0]
                    
        if isinstance(tabs, list):
            tabs = [self._convert_str_tabs(tab) for tab in tabs]
            explainer_layout = ExplainerTabsLayout(explainer, tabs, title, 
                            hide_title=header_hide_title, 
                            hide_selector=header_hide_selector, 
                            block_selector_callbacks=block_selector_callbacks,
                            pos_label=pos_label,
                            fluid=fluid)
        else:
            tabs = self._convert_str_tabs(tabs)
            explainer_layout = ExplainerPageLayout(explainer, tabs, title, 
                            hide_title=header_hide_title, 
                            hide_selector=header_hide_selector, 
                            block_selector_callbacks=block_selector_callbacks,
                            pos_label=pos_label,
                            fluid=fluid)

        self.app.layout = explainer_layout.layout()
        explainer_layout.calculate_dependencies()
        explainer_layout.register_callbacks(self.app)

    def _convert_str_tabs(self, component):
        if isinstance(component, str):
            if component == 'importances':
                return ImportancesTab
            elif component == 'model_summary':
                return ModelSummaryTab
            elif component == 'contributions':
                return ContributionsTab
            elif component == 'shap_dependence':
                return ShapDependenceTab
            elif component == 'shap_interaction':
                return ShapInteractionsTab
            elif component == 'decision_trees':
                return  DecisionTreesTab
        return component

    def _get_dash_app(self):
        if self.mode=="dash":
            if self.external_stylesheets is not None:
                app = dash.Dash(server=self.server, 
                                external_stylesheets=self.external_stylesheets, 
                                assets_url_path="", 
                                url_base_pathname=self.url_base_pathname)
                app.config['suppress_callback_exceptions'] = True
            else:
                app = dash.Dash(__name__, 
                                server=self.server, 
                                url_base_pathname=self.url_base_pathname)
                app.config['suppress_callback_exceptions'] = True
                app.css.config.serve_locally = True
                app.scripts.config.serve_locally = True
            return app
        elif self.mode in ['inline', 'jupyterlab', 'external']:
            if self.external_stylesheets is not None:
                app = JupyterDash(
                            external_stylesheets=self.external_stylesheets, 
                            assets_url_path="")
            else:
                app = JupyterDash(__name__)
            return app
        else:
            raise ValueError(f"mode=={self.mode} but should be in "
                 "['dash', 'inline', 'juypyterlab', 'external']")

    def flask_server(self):
        """returns self.app.server so that it can be exposed to e.g. gunicorn"""
        if self.mode != 'dash':
            print("Warning: in production you should probably use mode='dash'...")
        return self.app.server
        
    def run(self, port=8050, **kwargs):
        """Start ExplainerDashboard on port

        Args:
            port (int, optional): port to run on. Defaults to 8050.

        Raises:
            ValueError: if mode is unknown

        """

        pio.templates.default = "none"
        self.port = port
        
        if self.mode == 'dash':
            print(f"Starting ExplainerDashboard on http://localhost:{port}")
            self.app.run_server(port=port, **kwargs)
        elif self.mode == 'external':
            print(f"Starting ExplainerDashboard on http://localhost:{port}")
            self.app.run_server(port=port, mode=self.mode, **kwargs)
        elif self.mode in ['inline', 'jupyterlab']:
            self.app.run_server(port=port, mode=self.mode, 
                                width=self.width, height=self.height, **kwargs)
        else:
            raise ValueError(f"Unknown mode: {mode}...")

    def terminate(self, port=None, token=None):
        """terminate a JupyterDash based DashboardExplainer i.e. mode 
        in ['inline', 'jupyterlab', 'external']

        You can kill any JupyterDash dashboard from any ExplainerDashboard
        by specifying the right port. 

        Args:
            port (int, optional): port on which the dashboard is running. 
                        Defaults to the last port the instance had started on.
            token (str, optional): JupyterDash._token class property. 
                Defaults to the _token of the JupyterDash in the current namespace.

        Raises:
            ValueError: if can't find the port to terminate.
        """
        if port is None:
            try:
                port = self.port
            except:
                raise ValueError("Can't find port to terminate. You either first "
                        "need to run() a dashboard with this instance, or you "
                        "need to pass a port to terminate...")
        if token is None:
            token = JupyterDash._token
        
        shutdown_url = f"http://localhost:{port}/_shutdown_{token}"
        print(f"Trying to shut down dashboard on port {port}...")
        try:
            response = requests.get(shutdown_url)
        except Exception as e:
            print(f"Something seems to have failed: {e}")


class JupyterExplainerDashboard(ExplainerDashboard):
    def __init__(self, *args, **kwargs):
        raise ValueError("JupyterExplainerDashboard has been deprecated. "
                    "Use e.g. ExplainerDashboard(mode='inline') instead.")

class ExplainerTab:
    def __init__(self, *args, **kwargs):
        raise ValueError("ExplainerTab has been deprecated. "
                        "Use e.g. ExplainerDashboard(explainer, ImportancesTab) instead.")


class JupyterExplainerTab(ExplainerTab):
    def __init__(self, *args, **kwargs):
        raise ValueError("ExplainerTab has been deprecated. "
                        "Use e.g. ExplainerDashboard(explainer, ImportancesTab, mode='inline') instead.")


class InlineExplainer:
    """
    Run a single tab inline in a Jupyter notebook using specific method calls.
    """
    def __init__(self, explainer, mode='inline', width=1000, height=800, 
                    port=8050, **kwargs):
        """
        :param explainer: an Explainer object
        :param mode: either 'inline', 'jupyterlab' or 'external' 
        :type mode: str, optional
        :param width: width in pixels of inline iframe
        :param height: height in pixels of inline iframe
        :param port: port to run if mode='external'
        """
        assert mode in ['inline', 'external', 'jupyterlab'], \
            "mode should either be 'inline', 'external' or 'jupyterlab'!"
        self._explainer = explainer
        self._mode = mode
        self._width = width
        self._height = height
        self._port = port
        self._kwargs = kwargs
        self.tab = InlineExplainerTabs(self, "tabs") 
        """subclass with InlineExplainerTabs layouts, e.g. InlineExplainer(explainer).tab.modelsummary()"""
        self.shap = InlineShapExplainer(self, "shap") 
        """subclass with InlineShapExplainer layouts, e.g. InlineExplainer(explainer).shap.dependence()"""
        self.classifier = InlineClassifierExplainer(self, "classifier") 
        """subclass with InlineClassifierExplainer plots, e.g. InlineExplainer(explainer).classifier.confusion_matrix()"""
        self.regression = InlineRegressionExplainer(self, "regression") 
        """subclass with InlineRegressionExplainer plots, e.g. InlineExplainer(explainer).regression.residuals()"""
        self.decisiontrees =InlineDecisionTreesExplainer(self, "decisiontrees") 
        """subclass with InlineDecisionTreesExplainer plots, e.g. InlineExplainer(explainer).decisiontrees.decisiontrees()"""

    def terminate(self, port=None, token=None):
        """terminate an InlineExplainer on particular port.

        You can kill any JupyterDash dashboard from any ExplainerDashboard
        by specifying the right port. 

        Args:
            port (int, optional): port on which the InlineExplainer is running. 
                        Defaults to the last port the instance had started on.
            token (str, optional): JupyterDash._token class property. 
                Defaults to the _token of the JupyterDash in the current namespace.

        Raises:
            ValueError: if can't find the port to terminate.
        """
        if port is None:
            port = self._port
        if token is None:
            token = JupyterDash._token
        
        shutdown_url = f"http://localhost:{port}/_shutdown_{token}"
        print(f"Trying to shut down dashboard on port {port}...")
        try:
            response = requests.get(shutdown_url)
        except Exception as e:
            print(f"Something seems to have failed: {e}")

    def _run_app(self, app, **kwargs):
        """Starts the dashboard either inline or in a seperate tab

        :param app: the JupyterDash app to be run
        :type mode: JupyterDash app instance
        """
        pio.templates.default = "none"
        if self._mode in ['inline', 'jupyterlab']:
            app.run_server(mode=self._mode, width=self._width, height=self._height, port=self._port)
        elif self._mode == 'external':
             app.run_server(mode=self._mode, port=self._port, **self._kwargs)
        else:
            raise ValueError("mode should either be 'inline', 'jupyterlab'  or 'external'!")

    def _run_component(self, component, title):
        app = JupyterDash(__name__)
        app.title = title
        app.layout = component.layout()
        component.register_callbacks(app)
        self._run_app(app)
    
    @delegates_kwargs(ImportancesComponent)
    @delegates_doc(ImportancesComponent)
    def importances(self, title='Importances', **kwargs):
        """Runs model_summary tab inline in notebook"""
        comp = ImportancesComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    def model_stats(self, title='Models Stats', **kwargs):
        """Runs model_stats inline in notebook"""
        if self._explainer.is_classifier:
            comp = ClassifierModelStatsComposite(self._explainer, **kwargs)
        elif self._explainer.is_regression:
            comp = RegressionModelStatsComposite(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(PredictionSummaryComponent)
    @delegates_doc(PredictionSummaryComponent)
    def prediction(self,  title='Prediction', **kwargs):
        """Show contributions (permutation or shap) inline in notebook"""
        comp = PredictionSummaryComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    def random_index(self, title='Random Index', **kwargs):
        """show random index selector inline in notebook"""
        if self._explainer.is_classifier:
            comp = ClassifierRandomIndexComponent(self._explainer, **kwargs)
        elif self._explainer.is_regression:
            comp = RegressionRandomIndexComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(PdpComponent)
    @delegates_doc(PdpComponent)
    def pdp(self, title="Partial Dependence Plots", **kwargs):
        """Show contributions (permutation or shap) inline in notebook"""
        comp = PdpComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    
class InlineExplainerComponent:
    def __init__(self, inline_explainer, name):
        self._inline_explainer = inline_explainer
        self._explainer = inline_explainer._explainer
        self._name = name

    def _run_component(self, component, title):
        self._inline_explainer._run_component(component, title)

    def __repr__(self):
        component_methods = [method_name for method_name in dir(self)
                  if callable(getattr(self, method_name)) and not method_name.startswith("_")]

        return f"InlineExplainer.{self._name} has the following components: {', '.join(component_methods)}"


class InlineExplainerTabs(InlineExplainerComponent):
    
    @delegates_kwargs(ImportancesTab)
    @delegates_doc(ImportancesTab)
    def importances(self,  title='Importances', **kwargs):
        """Show contributions (permutation or shap) inline in notebook"""
        tab = ImportancesTab(self._explainer, **kwargs)
        self._run_component(tab, title)

    @delegates_kwargs(ModelSummaryTab)
    @delegates_doc(ModelSummaryTab)
    def modelsummary(self, title='Model Summary', **kwargs):
        """Runs model_summary tab inline in notebook"""
        tab = ModelSummaryTab(self._explainer, **kwargs)
        self._run_component(tab, title)

    @delegates_kwargs(ContributionsTab)
    @delegates_doc(ContributionsTab)
    def contributions(self,  title='Contributions', **kwargs):
        """Show contributions (permutation or shap) inline in notebook"""
        tab = ContributionsTab(self._explainer, **kwargs)
        self._run_component(tab, title)

    @delegates_kwargs(ShapDependenceTab)
    @delegates_doc(ShapDependenceTab)
    def dependence(self, title='Shap Dependence', **kwargs):
        """Runs shap_dependence tab inline in notebook"""
        tab = ShapDependenceTab(self._explainer, **kwargs)
        self._run_component(tab, title)

    @delegates_kwargs(ShapInteractionsTab)
    @delegates_doc(ShapInteractionsTab)
    def interactions(self, title='Shap Interactions', **kwargs):
        """Runs shap_interactions tab inline in notebook"""
        tab = ShapInteractionsTab(self._explainer, **kwargs)
        self._run_component(tab, title)

    @delegates_kwargs(DecisionTreesTab)
    @delegates_doc(DecisionTreesTab)
    def decisiontrees(self, title='Decision Trees', **kwargs):
        """Runs shap_interactions tab inline in notebook"""
        tab = DecisionTreesTab(self._explainer, **kwargs)
        self._run_component(tab, title)


class InlineShapExplainer(InlineExplainerComponent):

    @delegates_kwargs(ShapDependenceComposite)
    @delegates_doc(ShapDependenceComposite)
    def overview(self, title='Shap Overview', **kwargs):
        """Runs shap_dependence tab inline in notebook"""
        comp = ShapDependenceComposite(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(ShapSummaryComponent)
    @delegates_doc(ShapSummaryComponent)
    def summary(self, title='Shap Summary', **kwargs):
        """Show shap summary inline in notebook"""
        comp = ShapSummaryComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(ShapDependenceComponent)
    @delegates_doc(ShapDependenceComponent)
    def dependence(self, title='Shap Dependence', **kwargs):
        """Show shap summary inline in notebook"""
        
        comp = ShapDependenceComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(ShapInteractionsComposite)
    @delegates_doc(ShapInteractionsComposite)
    def interaction_overview(self, title='Interactions Overview', **kwargs):
        """Runs shap_dependence tab inline in notebook"""
        comp = ShapInteractionsComposite(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(InteractionSummaryComponent)
    @delegates_doc(InteractionSummaryComponent)
    def interaction_summary(self, title='Shap Interaction Summary', **kwargs):
        """show shap interaction summary inline in notebook"""
        comp =InteractionSummaryComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(InteractionDependenceComponent)
    @delegates_doc(InteractionDependenceComponent)
    def interaction_dependence(self, title='Shap Interaction Dependence', **kwargs):
        """show shap interaction dependence inline in notebook"""
        comp =InteractionDependenceComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(ShapContributionsGraphComponent)
    @delegates_doc(ShapContributionsGraphComponent)
    def contributions_graph(self,  title='Contributions', **kwargs):
        """Show contributions (permutation or shap) inline in notebook"""
        comp = ShapContributionsGraphComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(ShapContributionsTableComponent)
    @delegates_doc(ShapContributionsTableComponent)
    def contributions_table(self,  title='Contributions', **kwargs):
        """Show contributions (permutation or shap) inline in notebook"""
        comp = ShapContributionsTableComponent(self._explainer, **kwargs)
        self._run_component(comp, title)


class InlineClassifierExplainer(InlineExplainerComponent):
    @delegates_kwargs(ClassifierModelStatsComposite)
    @delegates_doc(ClassifierModelStatsComposite)
    def model_stats(self, title='Models Stats', **kwargs):
        """Runs model_stats inline in notebook"""
        comp = ClassifierModelStatsComposite(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(PrecisionComponent)
    @delegates_doc(PrecisionComponent)
    def precision(self, title="Precision Plot", **kwargs):
        """shows precision plot"""
        assert self._explainer.is_classifier
        comp = PrecisionComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(ConfusionMatrixComponent)
    @delegates_doc(ConfusionMatrixComponent)
    def confusion_matrix(self, title="Confusion Matrix", **kwargs):
        """shows precision plot"""
        comp= ConfusionMatrixComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(LiftCurveComponent)
    @delegates_doc(LiftCurveComponent)
    def lift_curve(self, title="Lift Curve", **kwargs):
        """shows precision plot"""
        assert self._explainer.is_classifier
        comp = LiftCurveComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(ClassificationComponent)
    @delegates_doc(ClassificationComponent)
    def classification(self, title="Classification", **kwargs):
        """shows precision plot"""
        assert self._explainer.is_classifier
        comp = ClassificationComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(RocAucComponent)
    @delegates_doc(RocAucComponent)
    def roc_auc(self, title="ROC AUC Curve", **kwargs):
        """shows precision plot"""
        assert self._explainer.is_classifier
        comp = RocAucComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(PrAucComponent)
    @delegates_doc(PrAucComponent)
    def pr_auc(self, title="PR AUC Curve", **kwargs):
        """shows precision plot"""
        assert self._explainer.is_classifier
        comp = PrAucComponent(self._explainer, **kwargs)
        self._run_component(comp, title)


class InlineRegressionExplainer(InlineExplainerComponent):
    
    @delegates_kwargs(RegressionModelStatsComposite)
    @delegates_doc(RegressionModelStatsComposite)
    def model_stats(self, title='Models Stats', **kwargs):
        """Runs model_stats inline in notebook"""
        comp = RegressionModelStatsComposite(self._explainer, **kwargs)
        self._run_component(comp, title)
    
    @delegates_kwargs(PredictedVsActualComponent)
    @delegates_doc(PredictedVsActualComponent)
    def pred_vs_actual(self, title="Predicted vs Actual", **kwargs):
        "shows predicted vs actual for regression"
        assert self._explainer.is_regression
        comp = PredictedVsActualComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(ResidualsComponent)
    @delegates_doc(ResidualsComponent)
    def residuals(self, title="Residuals", **kwargs):
        "shows residuals for regression"
        assert self._explainer.is_regression
        comp = ResidualsComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(ResidualsVsColComponent)
    @delegates_doc(ResidualsVsColComponent)
    def residuals_vs_col(self, title="Residuals vs col", **kwargs):
        "shows residuals vs col for regression"
        assert self._explainer.is_regression
        comp = ResidualsVsColComponent(self._explainer, **kwargs)
        self._run_component(comp, title)


class InlineDecisionTreesExplainer(InlineExplainerComponent):
    @delegates_kwargs(DecisionTreesComposite)
    @delegates_doc(DecisionTreesComposite)
    def overview(self, title="Decision Trees", **kwargs):
        """shap decision tree composite inline in notebook"""
        comp = DecisionTreesComposite(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(DecisionTreesComponent)
    @delegates_doc(DecisionTreesComponent)
    def decisiontrees(self, title='Decision Trees', **kwargs):
        """Runs decision_trees tab inline in notebook"""
        comp = DecisionTreesComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(DecisionPathTableComponent)
    @delegates_doc(DecisionPathTableComponent)
    def decisionpath_table(self, title='Decision path', **kwargs):
        """Runs decision_trees tab inline in notebook"""
        comp = DecisionPathTableComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

    @delegates_kwargs(DecisionPathTableComponent)
    @delegates_doc(DecisionPathTableComponent)
    def decisionpath_graph(self, title='Decision path', **kwargs):
        """Runs decision_trees tab inline in notebook"""
        comp = DecisionPathTableComponent(self._explainer, **kwargs)
        self._run_component(comp, title)

   

