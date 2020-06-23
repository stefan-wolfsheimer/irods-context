import click
from os.path import join
from os import putenv
from os.path import isfile
from os.path import exists
from icontext.util import get_config_dir
from icontext.util import get_config_file
from icontext.util import complete_servers
from icontext.util import complete_users


@click.command()
@click.argument("server",
                type=click.STRING,
                autocompletion=complete_servers)
@click.argument("user",
                type=click.STRING, autocompletion=complete_users)
def use(server, user):
    cfg_dir = get_config_dir(server, user)
    env_file = get_config_file(server, user)
    auth_file = join(cfg_dir, '.irodsA')
    putenv('IRODS_ENVIRONMENT_FILE', env_file)
    putenv('IRODS_AUTHENTICATION_FILE', auth_file)
    if exists(env_file) and isfile(env_file):
        msg = "switched to server {0} {1} not configured for user {1}"
        click.echo(click.style(msg.format(server, user), fg='green'))
        with open(env_file) as fp:
            click.echo(fp.read())
    else:
        msg = "server {0} {1} not configured for user {1}".format(server,
                                                                  user)
        click.echo(click.style(msg, fg='red'), err=True)
        click.echo("type 'icontext create --help' for more", err=True)
        return 8
