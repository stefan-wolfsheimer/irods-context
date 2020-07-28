import click
import sys
from os import getenv
from os.path import exists
from os.path import dirname
from os.path import realpath
from os.path import join
from icontext.ls import ls
from icontext.which import which
from icontext.describe import describe
from icontext.use import use
from icontext.unuse import unuse
from icontext.create import create
from icontext.clone import clone
from icontext.configure import configure
from icontext.edit import edit
from icontext.rename import rename
from icontext.delete import delete


@click.group()
def cli():
    pass


cli.add_command(ls)
cli.add_command(which)
cli.add_command(describe)

cli.add_command(use)
cli.add_command(unuse)

cli.add_command(create)
cli.add_command(clone)
cli.add_command(configure)
cli.add_command(edit)
cli.add_command(rename)
cli.add_command(delete)


def main(argv=sys.argv[1:]):
    complete_mode = getenv('_ICONTEXT_COMPLETE', None)
    if complete_mode is not None and complete_mode.startswith("source_"):
        script_name = join(dirname(realpath(__file__)), complete_mode + ".sh")
        if exists(script_name):
            with open(script_name, "r") as fp:
                print(fp.read())
        else:
            fmt = "{0} not supported"
            raise NotImplementedError(fmt.format(complete_mode))
    cli()
