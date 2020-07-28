import click
import os
from os.path import isfile
from os.path import exists
from icontext.util import get_env_file
from icontext.util import get_auth_file
from icontext.util import complete_servers
from icontext.util import complete_users
from icontext.util import update_env_file_variable


@click.command()
@click.argument("server",
                type=click.STRING,
                autocompletion=complete_servers)
@click.argument("user",
                type=click.STRING, autocompletion=complete_users)
def use(server, user):
    os.environ['IRODS_ENVIRONMENT_FILE'] = get_env_file(server, user)
    os.environ['IRODS_AUTHENTICATION_FILE'] = get_auth_file(server, user)
    env_file = os.environ['IRODS_ENVIRONMENT_FILE']
    if exists(env_file) and isfile(env_file):
        msg = "switched to server {0} {1} (env_file {2})"
        click.echo(click.style(msg.format(server, user, env_file), fg='green'))
        with open(os.environ['IRODS_ENVIRONMENT_FILE']) as fp:
            click.echo(fp.read())
        update_env_file_variable()
    else:
        msg = "server {0} not configured for user {1} ({2})".format(server,
                                                                    user,
                                                                    env_file)
        click.echo(click.style(msg, fg='red'), err=True)
        click.echo("type 'icontext create --help' for more", err=True)
        click.echo("type 'icontext clone --help' for more", err=True)
        return 8
