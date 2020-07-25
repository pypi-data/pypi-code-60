#!/usr/bin/env python3
import typer
from pprint import pprint
from enum import Enum

from alembic.config import Config
from alembic import command

alembic_cfg = Config("./alembic.ini")

cli = typer.Typer()


@cli.command()
def init():
    """Initialize db"""

    typer.echo(typer.style("fetching data from", fg="green"))

    f = open("guru99.txt", "w+")
    f.close()
    command.init(alembic_cfg, "alembic", template="generic", package=True)
    return


@cli.command()
def makemigrations():
    """make db migrations"""

    command.revision(alembic_cfg, autogenerate=True)
    return


@cli.command()
def migrate():
    """migrate db"""

    command.upgrade(alembic_cfg, "head")
    return


if __name__ == "__main__":
    cli()
