import click
from os.path import dirname
from os import makedirs
from os.path import exists
from shutil import copyfile
from icontext.util import complete_servers
from icontext.util import complete_users_regex_server
from icontext.util import get_env_file
from icontext.util import get_auth_file
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
@click.option('-f', '--force', default=False, is_flag=True)
@click.option('-u', '--use', default=False, is_flag=True)
def clone(server,
          user,
          new_server,
          new_user,
          force,
          use):
    old_env_file = get_env_file(server, user)
    old_auth_file = get_auth_file(server, user)
    err = ["{0} does not exist".format(f)
           for f in [old_env_file, old_auth_file]
           if not exists(f)]
    if len(err) > 0:
        fmt = "Cannot clone configuration {0} for user {1}:\n{2}"
        msg = fmt.format(server,
                         user,
                         "\n".join(err))
        click.echo(click.style(msg, fg='red'))
        return exit(8)
    new_env_file = get_env_file(new_server, new_user)
    new_auth_file = get_auth_file(new_server, new_user)
    if exists(new_env_file) and not force:
        fmt = ("Target configuration configuration {0} for user {1} exists.\n"
               "use --force to overwrite")
        msg = fmt.format(new_server, new_user)
        click.echo(click.style(msg, fg='red'))
        return exit(8)
    makedirs(dirname(new_env_file), exist_ok=True)
    copyfile(old_env_file, new_env_file)
    copyfile(old_auth_file, new_auth_file)
    if use:
        switch_context(new_server, new_user)
