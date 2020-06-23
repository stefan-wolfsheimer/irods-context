import click
import sys
from icontext.ls import ls
from icontext.use import use
from icontext.create import create
from icontext.configure import configure


@click.group()
def cli():
    pass


@click.command()
def describe():
    click.echo('DESCRIBE')


@click.command()
def note():
    click.echo('NOTE')


@click.command()
def clone():
    click.echo('CLONE')


cli.add_command(ls)
cli.add_command(use)
cli.add_command(describe)
cli.add_command(note)
cli.add_command(create)
cli.add_command(clone)
cli.add_command(configure)


def main(argv=sys.argv[1:]):
    cli()
