import click
import sys
from os.path import exists
from icontext.util import get_current_env_file
from icontext.util import get_current_server_and_user
from icontext.util import get_env_file
from icontext.util import complete_servers
from icontext.util import complete_users


def show_details(server, user):
    if user is None:
        if server is None:
            env_file = get_current_env_file()
            (server, user) = get_current_server_and_user()
        else:
            msg = "Provide either both server and user or none"
            click.echo(click.style(msg, fg='red'), err=True)
            sys.exit(8)
    else:
        env_file = get_env_file(server, user)
    fmt = "server:\t{0}\nuser:\t{1}\nenv:\t{2}"
    click.echo(fmt.format("" if server is None else server,
                          "" if user is None else user,
                          env_file))
    if exists(env_file):
        click.echo('---------------------')
        with open(env_file) as fp:
            click.echo(fp.read())


@click.command()
@click.argument("server",
                type=click.STRING,
                autocompletion=complete_servers,
                required=False)
@click.argument("user",
                type=click.STRING, autocompletion=complete_users,
                required=False)
def describe(server, user):
    """
    Show details of a configuration
    """
    return show_details(server, user)
