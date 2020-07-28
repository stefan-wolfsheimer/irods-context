import click
from os.path import dirname
from os import makedirs
from os.path import exists
import os
from icontext.util import complete_servers
from icontext.util import complete_users_regex_server
from icontext.util import get_config_dir
from icontext.use import switch_context


@click.command()
@click.argument("server",
                required=True,
                type=click.STRING,
                autocompletion=complete_servers)
@click.argument("user",
                required=True,
                type=click.STRING, autocompletion=complete_users_regex_server)
@click.argument("new_server",
                required=True,
                type=click.STRING,
                autocompletion=complete_servers)
@click.argument("new_user",
                required=True,
                type=click.STRING, autocompletion=complete_users_regex_server)
@click.option('-u', '--use', default=False, is_flag=True)
def rename(server,
           user,
           new_server,
           new_user,
           use):
    old_dir = get_config_dir(server, user)
    new_dir = get_config_dir(new_server, new_user)
    if not exists(old_dir):
        msg = "{0} does not exist".format(old_dir)
        click.echo(click.style(msg, fg='red'))
        return exit(8)
    if exists(new_dir):
        msg = "{0} already exists".format(new_dir)
        click.echo(click.style(msg, fg='red'))
        return exit(8)
    makedirs(dirname(new_dir), exist_ok=True)
    os.rename(old_dir, new_dir)
    if use:
        switch_context(new_server, new_user)
