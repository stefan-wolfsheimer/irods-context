import click
import sys
from os import makedirs
from os.path import dirname
import editor
from icontext.util import get_current_env_file
from icontext.util import get_current_server_and_user
from icontext.util import get_env_file
from icontext.util import complete_servers
from icontext.util import complete_users
from icontext.use import switch_context


@click.command()
@click.argument("server",
                type=click.STRING,
                autocompletion=complete_servers,
                required=False)
@click.argument("user",
                type=click.STRING, autocompletion=complete_users,
                required=False)
@click.option('-u', '--use', default=False, is_flag=True)
def edit(server, user, use):
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
    makedirs(dirname(env_file), exist_ok=True)
    editor.edit(filename=env_file)
    if use and server is not None:
        switch_context(server, user)
