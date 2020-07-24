"""pca is a python package that performs the principal component analysis and to make insightful plots."""

# ----------------------------------
# Name        : pca.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# ----------------------------------


# %% Libraries
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA, SparsePCA, TruncatedSVD
from sklearn import preprocessing
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.sparse as sp
from scipy import stats
from matplotlib.patches import Ellipse
import colourmap as colourmap
import os
import wget
from sklearn.metrics.pairwise import euclidean_distances

# %% Association learning across all variables
class pca():
    def __init__(self, n_components=0.95, n_feat=25, alpha=0.05, n_std=2, onehot=False, normalize=False, random_state=None):
        """Initialize pca with user-defined parameters.

        Parameters
        ----------
        onehot : [Bool] optional, (default: False)
            Boolean: Set True if X is a sparse data set such as the output of a tfidf model. Many zeros and few numbers. Note this is different then a sparse matrix. Sparse data can be in a sparse matrix.
        n_components : [0,..,1] or [1,..number of samples-1], (default: 0.95)
            Number of TOP components to be returned. Values>0 are the number of components. Values<0 are the components that covers at least the percentage of variance.
            0.95: Take the number of components that cover at least 95% of variance.
            k: Take the top k components
        n_feat : int, default: 10
            Number of features that explain the space the most, dervied from the loadings. This parameter is used for vizualization purposes only.
        alpha : float, default: 0.05
            Alpha to set the threshold to determine the outliers based on on the Hoteling T2 test.
        n_std : int, default: 2
            Number of standard deviations to determine the outliers using SPE/DmodX method.
        random_state : int optional
            Random state
        normalize : bool (default : True)
            Normalize data, Z-score

        """
        # Store in object
        self.n_components = n_components
        self.onehot = onehot
        self.normalize = normalize
        self.random_state = random_state
        self.n_feat = n_feat
        self.alpha = alpha
        self.n_std = n_std

    # Make PCA fit_transform
    def fit_transform(self, X, row_labels=None, col_labels=None, verbose=3):
        """Fit PCA on data.

        Parameters
        ----------
        X : numpy array
            [NxM] array with columns as features and rows as samples.
        row_labels : [list of integers or strings] optional
            Used for colors.
        col_labels : [list of string] optional
            Numpy Vector of strings: Name of the features that represent the data features and loadings
        Verbose : int (default : 3)
            Print to screen. 0: None, 1: Error, 2: Warning, 3: Info, 4: Debug, 5: Trace

        Returns
        -------
        dict.
        loadings : pd.DataFrame
            Structured dataframe containing loadings for PCs
        X : array-like
            Reduced dimentionsality space, the Principal Components (PCs)
        explained_var : array-like
            Explained variance for each fo the PCs (same ordering as the PCs)
        model_pca : object
            Model to be used for further usage of the model.
        topn : int
            Top n components
        pcp : int
            pcp
        col_labels : array-like
            Name of the features
        y : array-like
            Determined class labels

        Examples
        --------
        >>> from pca import pca
        >>> # Load example data
        >>> from sklearn.datasets import load_iris
        >>> X = pd.DataFrame(data=load_iris().data, columns=load_iris().feature_names, index=load_iris().target)
        >>>
        >>> Initialize
        >>> model = pca(n_components=3)
        >>> # Fit using PCA
        >>> results = model.fit_transform(X)
        >>>
        >>> # Make plots
        >>> fig, ax = model.scatter()
        >>> fig, ax = model.plot()
        >>> fig, ax = model.biplot()
        >>> fig, ax = model.biplot(SPE=True, hotellingt2=True)
        >>>
        >>> 3D plots
        >>> fig, ax = model.scatter3d()
        >>> fig, ax = model.biplot3d()
        >>> fig, ax = model.biplot3d(SPE=True, hotellingt2=True)
        >>>
        >>> # Normalize out PCs
        >>> X_norm = pca.norm(X)

        """
        # Pre-processing
        X, row_labels, col_labels = self._preprocessing(X, row_labels, col_labels, verbose=verbose)

        if self.n_components<1:
            if verbose>=3: print('[pca] >The PCA reduction is performed to capture [%.1f%%] explained variance using the [%.d] columns of the input data.' %(self.n_components*100, X.shape[1]))
            pcp = self.n_components
            # Run with all components to get all PCs back. This is needed for the step after.
            model_pca, PC, loadings, percentExplVar = _explainedvar(X, n_components=None, onehot=self.onehot, random_state=self.random_state, verbose=verbose)
            # Take number of components with minimal [n_components] explained variance
            if percentExplVar is None:
                self.n_components = X.shape[1] - 1
                if verbose>=3: print('[pca] >n_components is set to %d' %(self.n_components))
            else:
                self.n_components = np.min(np.where(percentExplVar >= self.n_components)[0]) + 1
                if verbose>=3: print('[pca] >Number of components is [%d] that covers the [%.2f%%] explained variance.' %(self.n_components, pcp*100))
        else:
            if verbose>=3: print('[pca] >The PCA reduction is performed on the [%.d] columns of the input dataframe.' %(X.shape[1]))
            model_pca, PC, loadings, percentExplVar = _explainedvar(X, n_components=self.n_components, onehot=self.onehot, random_state=self.random_state, verbose=verbose)
            pcp = percentExplVar[np.minimum(len(percentExplVar)-1, self.n_components)]

        # Combine components relations with features.
        loadings = self._postprocessing(model_pca, loadings, col_labels, self.n_components, verbose=verbose)
        # Top scoring n_components.
        topfeat = self.compute_topfeat(loadings=loadings, verbose=verbose)
        # Detection of outliers
        outliers = self.compute_outliers(PC, verbose=verbose)
        # Store
        self.results = _store(PC, loadings, percentExplVar, model_pca, self.n_components, pcp, col_labels, row_labels, topfeat, outliers)
        # Return
        return(self.results)

    # Outlier detection
    def compute_outliers(self, PC, n_std=2, verbose=3):
        # Detection of outliers using hotelling T2 test.
        outliersHT2 = hotellingsT2(PC, alpha=self.alpha, df=1, verbose=verbose)[0]
        # Detection of outliers using elipse method.
        outliersELIPS = spe_dmodx(PC, n_std=self.n_std, verbose=verbose)[0]
        # Combine
        outliers = pd.concat([outliersHT2, outliersELIPS], axis=1)
        return outliers

    # Post processing.
    def _postprocessing(self, model_pca, loadings, col_labels, n_components, verbose=3):
        PCzip = list(zip(['PC'] * model_pca.components_.shape[0], np.arange(1,model_pca.components_.shape[0] + 1).astype(str)))
        PCnames = list(map(lambda x: ''.join(x), PCzip))
        loadings = pd.DataFrame(loadings, columns=col_labels, index=PCnames)
        # Return
        return(loadings)

    # Top scoring components
    def compute_topfeat_old(self, loadings=None, n_feat=10, verbose=3):
        if (loadings is None):
            try:
                loadings = self.results['loadings']
            except:
                raise Exception('[pca] >Error: loadings is not defined. Tip: run fit_transform() or provide the loadings yourself as input argument.') 

        n_feat = np.maximum(np.minimum(n_feat, loadings.shape[1]), 2)
        # Top scoring for 1st component
        I1 = np.argsort(np.abs(loadings.iloc[0,:]))
        I1 = I1[::-1]
        # L1_weights = loadings.iloc[0,I1]

        if loadings.shape[0]>=2:
            # Top scoring for 2nd component
            I2 = np.argsort(np.abs(loadings.iloc[1,:]))
            I2 = I2[::-1]
            # L2_weights = loadings.iloc[0,I2]
            # Take only top loadings
            I1 = I1[0:n_feat]
            I2 = I2[0:n_feat]
            I = np.append(I1, I2)
        else:
            I = I1
        # Unique without sort:
        indices = np.unique(I,return_index=True)[1]
        # feat_weights = loadings.iloc[0:1,I].T
        # topfeat = feat_weights[0:n_feat]
        I = [I[index] for index in sorted(indices)]
        topfeat = loadings.iloc[0:2,I].T
        topfeat.columns = topfeat.columns.values+'_weights'
        # topfeat = topfeat.iloc[0:n_feat,:]
        return topfeat


    # Top scoring components
    def compute_topfeat(self, loadings=None, verbose=3):
        """Compute the top-scoring features.

        Description
        -----------
        Per Principal Component, the feature with absolute maximum loading is stored.
        This can result into the detection of PCs that contain the same features. The feature that were never detected are stored as "weak".

        Parameters
        ----------
        loadings : array-like
            The array containing the loading information of the Principal Components.
        Verbose : int (default : 3)
            Print to screen. 0: None, 1: Error, 2: Warning, 3: Info, 4: Debug, 5: Trace

        Returns
        -------
        topfeat : pd.DataFrame
            Best performing features per PC.

        """
        if (loadings is None):
            try:
                # Get feature names
                initial_feature_names = self.results['loadings'].columns.values
                loadings = self.results['loadings'].values.copy()
            except:
                raise Exception('[pca] >Error: loadings is not defined. Tip: run fit_transform() or provide the loadings yourself as input argument.') 
        
        if isinstance(loadings, pd.DataFrame):
            initial_feature_names = loadings.columns.values
            loadings = loadings.values

        # number of components
        n_pcs = loadings.shape[0]
        # get the index of the most important feature on EACH component
        idx = [np.abs(loadings[i]).argmax() for i in range(n_pcs)]
        # The the loadings
        loading_best = loadings[np.arange(0,n_pcs), idx]
        # get the names
        most_important_names = [initial_feature_names[idx[i]] for i in range(len(idx))]
        # Make dict with most important features
        dic = {'PC{}'.format(i+1): most_important_names[i] for i in range(len(most_important_names))}
        # Collect the features that were never discovered. The weak features.
        idxcol = np.setdiff1d(range(loadings.shape[1]), idx)
        # get the names
        least_important_names = [initial_feature_names[idxcol[i]] for i in range(len(idxcol))]
        # Find the strongest loading across the PCs for the least important ones
        idxrow = [np.abs(loadings[:,i]).argmax() for i in idxcol]
        loading_weak = loadings[idxrow, idxcol]
        # Make dict with most important features
        # dic_weak = {'weak'.format(i+1): least_important_names[i] for i in range(len(least_important_names))}
        PC_weak = ['PC{}'.format(i+1) for i in idxrow]

        # build the dataframe
        topfeat = pd.DataFrame(dic.items(), columns=['PC','feature'])
        topfeat['loading'] = loading_best
        topfeat['type'] = 'best'
        # Weak features
        weakfeat = pd.DataFrame({'PC':PC_weak, 'feature':least_important_names, 'loading':loading_weak, 'type':'weak'})
        # weakfeat = pd.DataFrame(dic_weak.items(), columns=['PC','feature'])
        # weakfeat['loading'] = loading_weak
        # weakfeat['type'] = 'weak'

        # Combine features
        df = pd.concat([topfeat, weakfeat])
        df.reset_index(drop=True, inplace=True)
        # Return
        return df

    # Check input values
    def _preprocessing(self, X, row_labels, col_labels, verbose=3):
        if self.n_components is None:
            self.n_components = X.shape[1] - 1
            if verbose>=3: print('[pca] >n_components is set to %d' %(self.n_components))

        self.n_feat = np.min([self.n_feat, X.shape[1]])

        if (not self.onehot) and (not self.normalize) and isinstance(X, pd.DataFrame) and (str(X.values.dtype)=='bool'):
            if verbose>=2: print('[pca] >Warning: Sparse or one-hot boolean input data is detected, it is highly recommended to set onehot=True or alternatively, normalize=True')

        # if sp.issparse(X):
            # if verbose>=1: print('[PCA] Error: A sparse matrix was passed, but dense data is required for method=barnes_hut. Use X.toarray() to convert to a dense numpy array if the array is small enough for it to fit in memory.')
        if isinstance(X, pd.DataFrame):
            if verbose>=3: print('[pca] >Processing dataframe..')
            col_labels = X.columns.values
            row_labels = X.index.values
            X = X.values
        if sp.issparse(X) and self.normalize:
            if verbose>=3: print('[pca] >Can not normalize a sparse matrix. Normalize is set to [False]')
            self.normalize=False
        if col_labels is None or len(col_labels)==0 or len(col_labels)!=X.shape[1]:
            if verbose>=3: print('[pca] >Column labels are auto-completed.')
            col_labels = np.arange(1,X.shape[1] + 1).astype(str)
        if row_labels is None or len(row_labels)!=X.shape[0]:
            row_labels=np.ones(X.shape[0])
            if verbose>=3: print('[pca] >Row labels are auto-completed.')
        if isinstance(row_labels, list):
            row_labels=np.array(row_labels)
        if isinstance(col_labels, list):
            col_labels=np.array(col_labels)
        if (sp.issparse(X) is False) and (self.n_components > X.shape[1]):
            # raise Exception('[pca] >Number of components can not be more then number of features.')
            if verbose>=2: print('[pca] >Warning: >Number of components can not be more then number of features. n_components is set to %d' %(X.shape[1]-1))
            self.n_components = X.shape[1]-1

        # normalize data
        if self.normalize:
            if verbose>=3: print('[pca] >Normalizing input data per feature (zero mean and unit variance)..')
            # Plot the data distribution
            # fig,(ax1,ax2)=plt.subplots(1,2, figsize=(15,5))
            # ax1.hist(X.ravel().astype(float), bins=50)
            # ax1.set_ylabel('frequency')
            # ax1.set_xlabel('Values')
            # ax1.set_title('RAW')
            # ax1.grid(True)

            X = preprocessing.scale(X, with_mean=True, with_std=True, axis=0)

            # Plot the data distribution
            # ax2.hist(X.ravel().astype(float), bins=50)
            # ax2.set_ylabel('frequency')
            # ax2.set_xlabel('Values')
            # ax2.set_title('Zero-mean with unit variance normalized')
            # ax2.grid(True)

        return(X, row_labels, col_labels)


    # Figure pre processing
    def _fig_preprocessing(self, y, n_feat, d3):
        if hasattr(self, 'PC'): raise Exception('[pca] >Error: Principal components are not derived yet. Tip: run fit_transform() first.')
        if self.results['PC'].shape[1]<1: raise Exception('[pca] >Requires at least 1 PC to make plot.')

        if (n_feat is not None):
            topfeat = self.compute_topfeat()
            # n_feat = np.maximum(np.minimum(n_feat, self.results['loadings'].shape[0]), 2)
        else:
            topfeat = self.results['topfeat']
            n_feat = self.n_feat

        if d3:
            n_feat = np.maximum(np.minimum(n_feat, self.results['loadings'].shape[1]), 3)
        else:
            n_feat = np.maximum(np.minimum(n_feat, self.results['loadings'].shape[1]), 2)

        if (y is not None):
            if len(y)!=self.results['PC'].shape[0]: raise Exception('[pca] >Error: Input variable [y] should have some length as the number input samples: [%d].' %(self.results['PC'].shape[0]))
            y = y.astype(str)
        else:
            y = self.results['PC'].index.values.astype(str)

        if len(self.results['explained_var'])<=1:
            raise Exception('[pca] >Error: No PCs are found with explained variance..')

        return y, topfeat, n_feat

    # Scatter plot
    def scatter3d(self, y=None, label=True, legend=True, PC=[0,1,2], SPE=False, hotellingt2=False, figsize=(10, 8)):
        """Scatter 3d plot.

        Parameters
        ----------
        y : array-like, default: None
            Label for each sample. The labeling is used for coloring the samples.
        PC : list, default : [0,1,2]
            Plot the first three Principal Components. Note that counting starts from 0. PC1=0, PC2=1, PC3=2, etc
        label : Bool, default: True
            Show the labels.
        legend : Bool, default: True
            Show the legend based on the unique y-labels.
        SPE : Bool, default: False
            Show the outliers based on SPE/DmodX method.
        hotellingt2 : Bool, default: False
            Show the outliers based on the hotelling T2 test.
        figsize : (int, int), optional, default: (10,8)
            (width, height) in inches.

        Returns
        -------
        tuple containing (fig, ax)

        """
        if self.results['PC'].shape[1]>=3:
            fig, ax = self.scatter(y=y, d3=True, label=label, legend=legend, PC=PC, SPE=SPE, hotellingt2=hotellingt2, figsize=figsize)
        else:
            print('[pca] >Error: There are not enough PCs to make a 3d-plot.')
            fig, ax = None, None
        return fig, ax

    # Scatter plot
    def scatter(self, y=None, d3=False, label=True, legend=True, PC=[0, 1], SPE=False, hotellingt2=False, figsize=(10, 8)):
        """Scatter 2d plot.

        Parameters
        ----------
        y : array-like, default: None
            Label for each sample. The labeling is used for coloring the samples.
        d3 : Bool, default: False
            3d plot is created when True.
        PC : list, default : [0,1]
            Plot the first two Principal Components. Note that counting starts from 0. PC1=0, PC2=1, PC3=2, etc
        legend : Bool, default: True
            Show the legend based on the unique y-labels.
        label : Bool, default: True
            Show the labels.
        SPE : Bool, default: False
            Show the outliers based on SPE/DmodX method.
        hotellingt2 : Bool, default: False
            Show the outliers based on the hotelling T2 test.
        figsize : (int, int), optional, default: (10,8)
            (width, height) in inches.

        Returns
        -------
        tuple containing (fig, ax)

        """
        fig, ax = plt.subplots(figsize=figsize, edgecolor='k')
        Ioutlier1 = np.repeat(False, self.results['PC'].shape[0])
        Ioutlier2 = np.repeat(False, self.results['PC'].shape[0])

        if y is None:
            y, _, _ = self._fig_preprocessing(y, None, d3)

        # Get coordinates
        xs, ys, zs, ax = _get_coordinates(self.results['PC'], PC, fig, ax, d3)
        
        # Plot outliers for hotelling T2 test.
        if hotellingt2:
            Ioutlier1 = self.results['outliers']['y_bool'].values
            if d3:
                ax.scatter(xs[Ioutlier1], ys[Ioutlier1], zs[Ioutlier1], marker='x', color=[0,0,0], s=26, label='outliers (hotelling t2)')
            else:
                ax.scatter(xs[Ioutlier1], ys[Ioutlier1], marker='x', color=[0,0,0], s=26, label='outliers (hotelling t2)')

        # Plot outliers for hotelling T2 test.
        if SPE:
            Ioutlier2 = self.results['outliers']['y_bool_spe'].values
            if d3:
                ax.scatter(xs[Ioutlier2], ys[Ioutlier2], zs[Ioutlier2], marker='d', color=[0.5,0.5,0.5], s=26, label='outliers (SPE/DmodX)')
            else:
                ax.scatter(xs[Ioutlier2], ys[Ioutlier2], marker='d', color=[0.5,0.5,0.5], s=26, label='outliers (SPE/DmodX)')
                # Plot the ellipse
                g_ellipse = spe_dmodx(np.c_[xs,ys], n_std=self.n_std, color='green', calpha=0.3, verbose=0)[1]
                if g_ellipse is not None: ax.add_artist(g_ellipse)

        # Make scatter plot of all not-outliers
        Inormal = ~np.logical_or(Ioutlier1, Ioutlier2)
        uiy = np.unique(y)
        getcolors = np.array(colourmap.generate(len(uiy), cmap='Set1'))
        for i, yk in enumerate(uiy):
            Iloc_label = (yk==y)
            Iloc_sampl = np.logical_and(Iloc_label, Inormal)
            if d3:
                ax.scatter(xs[Iloc_sampl], ys[Iloc_sampl], zs[Iloc_sampl], color=getcolors[i,:], s=25, label=yk)
                # if label: ax.text(xs[Iloc_label], ys[Iloc_label], zs[Iloc_label], yk, color=getcolors[i,:], ha='center', va='center')
            else:
                ax.scatter(xs[Iloc_sampl], ys[Iloc_sampl], color=getcolors[i,:], s=25, label=yk)
                if label: ax.annotate(yk, (np.mean(xs[Iloc_label]), np.mean(ys[Iloc_label])))

        # Set y
        ax.set_xlabel('PC'+str(PC[0]+1)+' ('+ str(self.results['model'].explained_variance_ratio_[PC[0]] * 100)[0:4] + '% expl.var)')
        ax.set_ylabel('PC'+str(PC[1]+1)+' ('+ str(self.results['model'].explained_variance_ratio_[PC[1]] * 100)[0:4] + '% expl.var)')
        if d3: ax.set_zlabel('PC'+str(PC[2]+1)+' ('+ str(self.results['model'].explained_variance_ratio_[PC[2]] * 100)[0:4] + '% expl.var)')
        ax.set_title(str(self.n_components)+' Principal Components explain [' + str(self.results['pcp']*100)[0:5] + '%] of the variance')
        if legend: ax.legend()
        ax.grid(True)

        return fig, ax

    # biplot
    def biplot(self, y=None, n_feat=None, d3=False, label=True, legend=True, SPE=False, hotellingt2=False, figsize=(10, 8), verbose=3):
        """Create the Biplot.

        Description
        -----------
        Plots the PC1 vs PC2 (vs PC3) with the samples, and the best performing features.
        Per PC, The feature with absolute highest loading is gathered. This can result into features that are seen over multiple PCs, and some features may never be detected.
        For vizualization purposes we will keep only the unique feature-names and plot them with red arrows and green labels.
        The feature-names that were never discovered (described as weak) are colored yellow.

        Parameters
        ----------
        y : array-like, default: None
            Label for each sample. The labeling is used for coloring the samples.
        n_feat : int, default: 10
            Number of features that explain the space the most, dervied from the loadings. This parameter is used for vizualization purposes only.
        d3 : Bool, default: False
            3d plot is created when True.
        label : Bool, default: True
            Show the labels.
        legend : Bool, default: True
            Show the legend based on the unique y-labels.
        SPE : Bool, default: False
            Show the outliers based on SPE/DmodX method.
        hotellingt2 : Bool, default: False
            Show the outliers based on the hotelling T2 test.
        figsize : (int, int), optional, default: (10,8)
            (width, height) in inches.
        Verbose : int (default : 3)
            Print to screen. 0: None, 1: Error, 2: Warning, 3: Info, 4: Debug, 5: Trace

        Returns
        -------
        tuple containing (fig, ax)

        References
        -----------
        * https://stackoverflow.com/questions/50796024/feature-variable-importance-after-a-pca-analysis/50845697#50845697
        * https://towardsdatascience.com/pca-clearly-explained-how-when-why-to-use-it-and-feature-importance-a-guide-in-python-7c274582c37e

        """
        if self.results['PC'].shape[1]<2:
            print('[pca] >Requires 2 PCs to make 2d plot.')
            return None, None

        # Pre-processing
        y, topfeat, n_feat = self._fig_preprocessing(y, n_feat, d3)
        # coeff = self.results['loadings'][topfeat['feature'].values].iloc[0:n_feat,:]
        coeff = self.results['loadings'].iloc[0:n_feat, :]
        # Use the PCs only for scaling purposes
        mean_x = np.mean(self.results['PC'].iloc[:, 0].values)
        mean_y = np.mean(self.results['PC'].iloc[:, 1].values)

        # Plot and scale values for arrows and text
        # Take the absolute minimum range of the x-axis and y-axis
        # max_axis = np.min(np.abs(self.results['PC'].iloc[:,0:2]).max())
        max_axis = np.max(np.abs(self.results['PC'].iloc[:, 0:2]).min(axis=1))
        max_arrow = np.abs(coeff).max().max()
        scale = (np.max([1, np.round(max_axis / max_arrow, 2)])) * 0.93

        # Include additional parameters if 3d-plot is desired.
        if d3:
            if self.results['PC'].shape[1]<3:
                if verbose>=2: print('[pca] >Warning: requires 3 PCs to make 3d plot.')
                return None, None
            mean_z = np.mean(self.results['PC'].iloc[:, 2].values)
            # zs = self.results['PC'].iloc[:,2].values
            fig, ax = self.scatter3d(y=y, label=label, legend=legend, SPE=SPE, hotellingt2=hotellingt2, figsize=figsize)
        else:
            fig, ax = self.scatter(y=y, label=label, legend=legend, SPE=SPE, hotellingt2=hotellingt2, figsize=figsize)

        # For vizualization purposes we will keep only the unique feature-names
        topfeat = topfeat.drop_duplicates(subset=['feature'])
        if topfeat.shape[0]<n_feat:
            n_feat = topfeat.shape[0]
            if verbose>=2: print('[pca] >Warning: n_feat can not be reached because of the limitation of n_components (=%d). n_feat is reduced to %d.' %(self.n_components, n_feat))

        # Plot arrows and text
        for i in range(0, n_feat):
            getfeat = topfeat['feature'].iloc[i]
            label = getfeat + ' (' + ('%.2f' %topfeat['loading'].iloc[i]) + ')'
            getcoef = coeff[getfeat].values
            # Set PC1 vs PC2 direction. Note that these are not neccarily the best loading.
            xarrow = getcoef[0] * scale  # PC1 direction (aka the x-axis)
            yarrow = getcoef[1] * scale  # PC2 direction (aka the y-axis)
            txtcolor = 'y' if topfeat['type'].iloc[i] == 'weak' else 'g'

            if d3:
                # zarrow = getcoef[np.minimum(2,len(getcoef))] * scale
                zarrow = getcoef[2] * scale
                ax.quiver(mean_x, mean_y, mean_z, xarrow - mean_x, yarrow - mean_y, zarrow - mean_z, color='red', alpha=0.8, lw=2)
                ax.text(xarrow * 1.11, yarrow * 1.11, zarrow * 1.11, label, color=txtcolor, ha='center', va='center')
            else:
                ax.arrow(mean_x, mean_y, xarrow - mean_x, yarrow - mean_y, color='r', width=0.005, head_width=0.01 * scale, alpha=0.8)
                ax.text(xarrow * 1.11, yarrow * 1.11, label, color=txtcolor, ha='center', va='center')

        plt.show()
        return(fig, ax)

    # biplot3d
    def biplot3d(self, y=None, n_feat=None, label=True, legend=True, SPE=False, hotellingt2=False, figsize=(10, 8)):
        """Make biplot in 3d.

        Parameters
        ----------
        y : array-like, default: None
            Label for each sample. The labeling is used for coloring the samples.
        n_feat : int, default: 10
            Number of features that explain the space the most, dervied from the loadings. This parameter is used for vizualization purposes only.
        label : Bool, default: True
            Show the labels.
        legend : Bool, default: True
            Show the legend based on the unique y-labels.
        SPE : Bool, default: False
            Show the outliers based on SPE/DmodX method.
        hotellingt2 : Bool, default: False
            Show the outliers based on the hotelling T2 test.
        figsize : (int, int), optional, default: (10,8)
            (width, height) in inches.

        Returns
        -------
        tuple containing (fig, ax)

        """

        if self.results['PC'].shape[1]<3:
            print('[pca] >Requires 3 PCs to make 3d plot. Try to use biplot() instead.')
            return None, None

        fig, ax = self.biplot(y=y, n_feat=n_feat, d3=True, label=label, legend=legend, SPE=SPE, hotellingt2=hotellingt2, figsize=figsize)

        return(fig, ax)

    # Show explained variance plot
    def plot(self, n_components=None, figsize=(10, 8), xsteps=None):
        """Make plot.

        Parameters
        ----------
        model : dict
            model created by the fit() function.
        figsize : (float, float), optional, default: None
            (width, height) in inches. If not provided, defaults to rcParams["figure.figsize"] = (10,8)

        Returns
        -------
        tuple containing (fig, ax)

        """
        if n_components is not None:
            explvarCum = self.results['explained_var'][0:n_components]
            explvar = self.results['model'].explained_variance_ratio_[0:n_components]
        else:
            explvarCum = self.results['explained_var']
            explvar = self.results['model'].explained_variance_ratio_
        xtick_idx = np.arange(1, len(explvar) + 1)

        # Make figure
        fig, ax = plt.subplots(figsize=figsize, edgecolor='k')
        plt.plot(xtick_idx, explvarCum, 'o-', color='k', linewidth=1, label='Cumulative explained variance')

        # Set xticks if less then 100 datapoints
        if len(explvar)<100:
            ax.set_xticks(xtick_idx)
            xticklabel=xtick_idx.astype(str)
            if xsteps is not None:
                xticklabel[np.arange(1, len(xticklabel), xsteps)] = ''
            ax.set_xticklabels(xticklabel, rotation=90, ha='left', va='top')

        plt.ylabel('Percentage explained variance')
        plt.xlabel('Principle Component')
        plt.ylim([0, 1.05])
        plt.xlim([0, len(explvar) + 1])
        titletxt = 'Cumulative explained variance\n ' + str(self.n_components) + ' Principal Components explain [' + str(self.results['pcp'] * 100)[0:5] + '%] of the variance.'
        plt.title(titletxt)
        plt.grid(True)

        # Plot vertical line To stress the cut-off point
        ax.axvline(self.n_components, linewidth=0.8, color='r')
        ax.axhline(y=self.results['pcp'], xmin=0, xmax=1, linewidth=0.8, color='r')
        if len(xtick_idx)<100:
            plt.bar(xtick_idx, explvar, color='#3182bd', alpha=0.8, label='Explained variance')
        plt.show()
        plt.draw()
        return(fig, ax)

    # Top scoring components
    def norm(self, X, n_components=None, pcexclude=[1]):
        """Normalize out PCs.

        Description
        -----------
        Normalize your data using the principal components.
        As an example, suppose there is (technical) variation in the fist
        component and you want that out. This function transforms the data using
        the components that you want, e.g., starting from the 2nd pc, up to the
        pc that contains at least 95% of the explained variance

        Parameters
        ----------
        X : numpy array
            Data set.
        n_components : float [0..1], optional
            Number of PCs to keep based on the explained variance. The default is 1 (keeping all)
        pcexclude : list of int, optional
            The PCs to exclude. The default is [1].

        Returns
        -------
        Normalized numpy array.

        """
        if n_components is None:
            self.n_components = X.shape[1]
        else:
            self.n_components = n_components

        if not isinstance(pcexclude, list): pcexclude=[pcexclude]

        # Fit using PCA
        _ = self.fit_transform(X)
        coeff = self.results['loadings'].values
        score = self.results['PC']
        # Compute explained percentage of variance
        q = self.results['explained_var']
        ndims = np.where(q<=self.n_components)[0]
        ndims = (np.setdiff1d(ndims + 1, pcexclude)) - 1
        # Transform data
        out = np.repeat(np.mean(X.values, axis=1).reshape(-1, 1), X.shape[1], axis=1) + np.dot(score.values[:, ndims], coeff[:, ndims].T)
        # Return
        return(out)

    # Import example
    def import_example(self, data='titanic', verbose=3):
        """Import example dataset from github source.

        Parameters
        ----------
        data : str, optional
            Name of the dataset 'sprinkler' or 'titanic' or 'student'.
        verbose : int, optional
            Print message to screen. The default is 3.

        Returns
        -------
        pd.DataFrame()
            Dataset containing mixed features.

        """
        return import_example(data=data, verbose=verbose)

# %%
def _get_coordinates(PCs, PC, fig, ax, d3):
    xs = PCs.iloc[:,PC[0]].values
    ys = np.zeros(len(xs))
    zs = None

    # Get y-axis
    if PCs.shape[1]>1:
        ys = PCs.iloc[:,PC[1]].values

    # Get Z-axis
    if d3:
        zs = PCs.iloc[:,PC[2]].values
        ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

    return xs, ys, zs, ax

# %%
def _eigsorted(cov, n_std):
    vals, vecs = np.linalg.eigh(cov)
    # vecs = vecs * np.sqrt(scipy.stats.chi2.ppf(0.95, n_std))
    order = vals.argsort()[::-1]
    return vals[order], vecs[:, order]


def spe_dmodx(X, n_std=2, calpha=0.3, color='green', showfig=False, verbose=3):
    """Compute SPE/distance to model (DmodX).

    Description
    -----------
    Outlier can be detected using SPE/DmodX (distance to model) based on the mean and covariance of the first 2 dimensions of X.
    On the model plane (SPE ≈ 0). Note that the SPE or Hotelling’s T2 are complementary to each other.

    Parameters
    ----------
    X : Array-like
        Input data, in this case the Principal components.
    n_std : int, (default: 2)
        Standard deviation. The default is 2.
    calpha : float, (default: 0.3)
        transperancy color.
    color : String, (default: 'green')
        Color of the ellipse.
    showfig : bool, (default: False)
        Scatter the points with the ellipse and mark the outliers.

    Returns
    -------
    outliers : pd.DataFrame()
        column with boolean outliers and euclidean distance of each sample to the center of the ellipse.
    ax : object
        Figure axis.

    """

    if verbose>=3: print('[pca] >Outlier detection using SPE/DmodX with n_std=[%d]' %(n_std))
    # The 2x2 covariance matrix to base the ellipse on the location of the center of the ellipse. Expects a 2-element sequence of [x0, y0].
    n_components = np.minimum(2, X.shape[1])
    X = X[:, 0:n_components]

    if X.shape[1]>=2:
        # Compute mean and covariance
        g_ell_center = X.mean(axis=0)
        cov = np.cov(X, rowvar=False)
        # Width and height are "full" widths, not radius
        vals, vecs = _eigsorted(cov, n_std)
        angle = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
        width, height = 2 * n_std * np.sqrt(vals)
        # Compute angles of ellipse
        cos_angle = np.cos(np.radians(180. - angle))
        sin_angle = np.sin(np.radians(180. - angle))
        # Determine the elipse range
        xc = X[:, 0] - g_ell_center[0]
        yc = X[:, 1] - g_ell_center[1]
        xct = xc * cos_angle - yc * sin_angle
        yct = xc * sin_angle + yc * cos_angle
        rad_cc = (xct**2 / (width / 2.)**2) + (yct**2 / (height / 2.)**2)

        # Mark the samples outside the ellipse
        outliers = rad_cc>1

        # Plot the raw points.
        g_ellipse = Ellipse(xy=g_ell_center, width=width, height=height, angle=angle, color=color, alpha=calpha)
        y_score = list(map(lambda x: euclidean_distances([g_ell_center], x.reshape(1, -1))[0][0], X))

        if showfig:
            ax = plt.gca()
            ax.add_artist(g_ellipse)
            ax.scatter(X[~outliers, 0], X[~outliers, 1], c='black', linewidths=0.3, label='normal')
            ax.scatter(X[outliers, 0], X[outliers, 1], c='red', linewidths=0.3, label='outlier')
            ax.legend()
    else:
        outliers = np.repeat(False, X.shape[1])
        y_score = np.repeat(None, X.shape[1])

    out = pd.DataFrame()
    out['y_bool_spe'] = outliers
    out['y_score_spe'] = y_score

    return out, g_ellipse


# %% Outlier detection
def hotellingsT2(X, alpha=0.05, df=1, n_components=5, verbose=3):
    """Test for outlier using hotelling T2 test.

    Description
    -----------
    Test for outliers using chi-square tests for each of the n_components.
    The resulting P-value matrix is then combined using fishers method per sample.
    The results can be used to priortize outliers as those samples that are an outlier
    across multiple dimensions will be more significant then others.

    Parameters
    ----------
    X : numpy-array.
        Principal Components.
    alpha : float, (default: 0.05)
        Alpha level threshold to determine outliers.
    df : int, (default: 1)
        Degrees of freedom.
    n_components : int, (default: 5)
        Number of PC components to be used to compute the Pvalue.
    Verbose : int (default : 3)
        Print to screen. 0: None, 1: Error, 2: Warning, 3: Info, 4: Debug, 5: Trace

    Returns
    -------
    outliers : pd.DataFrame
        dataframe containing probability, test-statistics and boolean value.
    y_bools : array-like
        boolean value when significant per PC.

    """
    n_components = np.minimum(n_components, X.shape[1])
    X = X[:, 0:n_components]
    y = X

    if verbose>=3: print('[pca] >Outlier detection using Hotelling T2 test with alpha=[%.2f] and n_components=[%d]' %(alpha, n_components))
    y_score = (y - np.mean(X)) ** 2 / np.var(X)
    # Compute probability per PC whether datapoints are outside the boundary
    y_proba = 1 - stats.chi2.cdf(y_score, df=df)
    # Set probabilities at a very small value when 0. This is required for the Fishers method. Otherwise inf values will occur.
    y_proba[y_proba==0]=1e-300

    # Compute the anomaly threshold
    anomaly_score_threshold = stats.chi2.ppf(q=(1 - alpha), df=df)
    # Determine for each samples and per principal component the outliers
    y_bools = y_score >= anomaly_score_threshold

    # Combine Pvalues across the components
    Pcomb = []
    # weights = np.arange(0, 1, (1/n_components) )[::-1] + (1/n_components)
    for i in range(0, y_proba.shape[0]):
        # Pcomb.append(stats.combine_pvalues(y_proba[i, :], method='stouffer', weights=weights))
        Pcomb.append(stats.combine_pvalues(y_proba[i, :], method='fisher'))

    Pcomb = np.array(Pcomb)
    outliers = pd.DataFrame()
    outliers['y_proba']= Pcomb[:, 1]
    outliers['y_score'] = Pcomb[:, 0]
    outliers['y_bool'] = Pcomb[:, 1] <= alpha
    # Return
    return outliers, y_bools


# %% Explained variance
def _explainedvar(X, n_components=None, onehot=False, random_state=None, n_jobs=-1, verbose=3):
    # Create the model
    if sp.issparse(X):
        if verbose>=3: print('[pca] >Fitting using Truncated SVD..')
        model = TruncatedSVD(n_components=n_components, random_state=random_state)
    elif onehot:
        if verbose>=3: print('[pca] >Fitting using Sparse PCA..')
        model = SparsePCA(n_components=n_components, random_state=random_state, n_jobs=n_jobs)
    else:
        if verbose>=3: print('[pca] >Fitting using PCA..')
        model = PCA(n_components=n_components, random_state=random_state)

    # Fit model
    model.fit(X)
    # Do the reduction
    if verbose>=3: print('[pca] >Computing loadings and PCs..')
    loadings = model.components_ # Ook wel de coeeficienten genoemd: coefs!
    PC = model.transform(X)
    if not onehot:
        # Compute explained variance, top 95% variance
        if verbose>=3: print('[pca] >Computing explained variance..')
        percentExplVar = model.explained_variance_ratio_.cumsum()
    else:
        percentExplVar = None
    # Return
    return(model, PC, loadings, percentExplVar)


# %% Store results
def _store(PC, loadings, percentExplVar, model_pca, n_components, pcp, col_labels, row_labels, topfeat, outliers):
    outliers.index = row_labels
    
    out = {}
    out['loadings'] = loadings
    out['PC'] = pd.DataFrame(data=PC[:,0:n_components], index=row_labels, columns=loadings.index.values[0:n_components])
    out['explained_var'] = percentExplVar
    out['model'] = model_pca
    out['pcp'] = pcp
    out['topfeat'] = topfeat
    out['outliers'] = outliers
    return out


# %% Import example dataset from github.
def import_example(data='titanic', verbose=3):
    """Import example dataset from github source.

    Parameters
    ----------
    data : str, optional
        Name of the dataset 'sprinkler' or 'titanic' or 'student'.
    verbose : int, optional
        Print message to screen. The default is 3.

    Returns
    -------
    pd.DataFrame()
        Dataset containing mixed features.

    """
    if data=='sprinkler':
        url='https://erdogant.github.io/datasets/sprinkler.zip'
    elif data=='titanic':
        url='https://erdogant.github.io/datasets/titanic_train.zip'
    elif data=='student':
        url='https://erdogant.github.io/datasets/student_train.zip'

    curpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    PATH_TO_DATA = os.path.join(curpath, wget.filename_from_url(url))
    if not os.path.isdir(curpath):
        os.mkdir(curpath)

    # Check file exists.
    if not os.path.isfile(PATH_TO_DATA):
        if verbose>=3: print('[pca] >Downloading example dataset from github source..')
        wget.download(url, curpath)

    # Import local dataset
    if verbose>=3: print('[pca] >Import dataset [%s]' %(data))
    df = pd.read_csv(PATH_TO_DATA)
    # Return
    return df
