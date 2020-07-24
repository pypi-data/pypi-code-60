# -*- coding: utf-8 -*-
# Apache Software License 2.0
#
# Copyright (c) 2018, Christophe Duong
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
CLI module for Jupyter related commands.
"""
import logging
import os
import sys
from subprocess import PIPE  # nosec
from subprocess import Popen
from subprocess import TimeoutExpired
from threading import Thread

import click

from aiscalator import __version__
from aiscalator.core.config import AiscalatorConfig
from aiscalator.jupyter import command


@click.group()
@click.version_option(version=__version__)
def jupyter():
    """Notebook environment to explore and handle data."""


@jupyter.command()
@click.version_option(version=__version__)
def setup():
    """Setup the current docker image to run notebooks."""
    update_aiscalator()
    # TODO to implement
    logging.error("Not implemented yet")


@jupyter.command()
@click.version_option(version=__version__)
def update():
    """
    Checks and tries to update the current docker image
    to run notebooks to a newer version.

    Initiates a docker pull of the latest images we are depending on
    and build the next aiscalator images from there.
    Before replacing the version tags in the Dockerfile, we make sure
    to do a maximum in the background while still having a working
    image in the meantime.

    """
    update_aiscalator()
    # TODO to implement
    logging.error("Not implemented yet")


@jupyter.command()
@click.option('--name', prompt='What is the name of your step?',
              help="Name of the new step to create",
              metavar='<STEP>')
@click.option('-f', '--format', 'output_format',
              help="format of the configuration file (default is hocon)",
              type=click.Choice(['json', 'hocon']),
              default='hocon')
# TODO: import an existing notebook and create a new aiscalate step from it
@click.argument('path', type=click.Path())
@click.version_option(version=__version__)
def new(name, output_format, path):
    """Create a new notebook associated with a new aiscalate step config."""
    update_aiscalator()
    file_conf = os.path.join(path, name, name) + '.conf'
    file_json = os.path.join(path, name, name) + '.json'
    if os.path.exists(file_conf):
        prompt_edit(file_conf)
    elif os.path.exists(file_json):
        prompt_edit(file_json)
    else:
        click.echo(command.jupyter_new(name, path,
                                       output_format=output_format))


def prompt_edit(file):
    """
    When creating a new step, if it is already defined,
    ask to edit instead

    Parameters
    ----------
    file : str
        existing configuration file

    """
    msg = file + ' already exists. Did you mean to run:\n'
    for i in sys.argv:
        if i != "new":
            msg += i + ' '
        else:
            break
    msg += "edit " + file + " instead?"
    if click.confirm(msg, abort=True):
        conf = AiscalatorConfig(config=file)
        click.echo(command.jupyter_edit(conf))


@jupyter.command()
@click.argument('conf', type=click.Path(exists=True))
@click.argument('notebook', nargs=-1)
@click.option('-p', '--param', type=(str, str), multiple=True)
@click.option('-r', '--param_raw', type=(str, str), multiple=True)
@click.version_option(version=__version__)
# TODO add parameters override from CLI
def edit(conf, notebook, param, param_raw):
    """Edit the notebook from an aiscalate config with JupyterLab."""
    update_aiscalator()
    if len(notebook) < 2:
        notebook = notebook[0] if notebook else None
        app_config = AiscalatorConfig(config=conf,
                                      step_selection=notebook)
        click.echo(command.jupyter_edit(app_config,
                                        param=param, param_raw=param_raw))
    else:
        raise click.BadArgumentUsage("Expecting one or less notebook names")


@jupyter.command()
@click.argument('conf', type=click.Path(exists=True))
@click.argument('notebook', nargs=-1)
@click.option('-p', '--param', type=(str, str), multiple=True)
@click.option('-r', '--param_raw', type=(str, str), multiple=True)
@click.version_option(version=__version__)
# TODO add parameters override from CLI
def run(conf, notebook, param, param_raw):
    """Run the notebook from an aiscalate config without GUI."""
    update_aiscalator()
    if notebook:
        for note in notebook:
            app_config = AiscalatorConfig(config=conf,
                                          step_selection=note)
            click.echo(command.jupyter_run(app_config,
                                           param=param, param_raw=param_raw))
    else:
        app_config = AiscalatorConfig(config=conf)
        click.echo(command.jupyter_run(app_config,
                                       param=param, param_raw=param_raw))


def update_aiscalator():
    """
    Create and run Thread to execute auto update in the background
    """
    worker = Thread(name='autoUpdate', target=run_auto_update)
    worker.start()


def run_auto_update():
    """
    Checks and tries to update Aiscalator itself from Pypi if necessary
    """
    version = pip_list = grep = sed = pip_install = None
    try:
        cmd = ["pip", "list", "--outdated"]
        pip_list = Popen(cmd, stdout=PIPE)
        pip_list_out, _ = pip_list.communicate(timeout=60)

        cmd = ["grep", "aiscalator"]
        grep = Popen(cmd, stdin=PIPE, stdout=PIPE)
        grep_out, _ = grep.communicate(pip_list_out, timeout=15)

        cmd = ["sed", "-E", "s/aiscalator[ \\t]+([0-9.]+)/\\1/"]
        sed = Popen(cmd, stdin=PIPE, stdout=PIPE)
        version, _ = sed.communicate(grep_out, timeout=15)
        if version:
            version = version.decode("utf-8")
    except TimeoutExpired:
        if pip_list:
            pip_list.kill()
        if grep:
            grep.kill()
        if sed:
            sed.kill()
    if version and version < __version__:
        msg = "A new update of AIscalator (v" + version.strip("\n")
        msg += ") is now available!\nShould we upgrade? Current is v"
        msg += __version__
        try:
            cmd = ["pip", "install", "--upgrade", "aiscalator"]
            pip_install = Popen(cmd)
            pip_install.communicate(timeout=120)
        except TimeoutExpired:
            if pip_install:
                pip_install.kill()
