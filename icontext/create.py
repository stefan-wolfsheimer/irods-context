import click
from os.path import dirname
from os import makedirs
from getpass import getpass
from icontext.util import complete_servers
from icontext.util import complete_users_regex_server
from icontext.util import get_env_file
from icontext.util import get_auth_file
from icontext.util import input_value
from icontext.util import TEMPLATE_WITH_SSL
from icontext.util import TEMPLATE_WITHOUT_SSL
import irods.password_obfuscation as password_obfuscation


@click.command()
@click.argument("server",
                required=False,
                type=click.STRING,
                autocompletion=complete_servers)
@click.argument("user",
                required=False,
                type=click.STRING, autocompletion=complete_users_regex_server)
@click.option('-s', '--with-ssl', default=False, is_flag=True)
@click.option('-p', '--with-pam', default=False, is_flag=True)
@click.option('--port', default=1247, type=int, required=False)
@click.option('--host', required=False)
@click.option('--zone', required=False, default="tempZone")
def create(server,
           user,
           with_ssl, with_pam, port, host, zone):
    if server is None:
        server = input_value("server name", "")
    if user is None:
        user = input_value("user", "")
    if not server:
        raise RuntimeError("missing value: server")
    if not user:
        raise RuntimeError("missing value: user")
    host = input_value("host", host)
    port = int(input_value("port", port))
    zone = input_value("zone", zone)
    cfg_args = {"irods_host": host,
                "irods_port": port,
                "irods_user_name": user,
                "irods_zone_name": zone}
    if with_pam or with_ssl:
        scheme = "PAM" if with_pam else "native"
        cfg_args['irods_authentication_scheme'] = scheme
        cfg = TEMPLATE_WITH_SSL.format(**cfg_args)
    else:
        cfg = TEMPLATE_WITHOUT_SSL.format(**cfg_args)
    env_file = get_env_file(server, user)
    auth_file = get_auth_file(server, user)
    makedirs(dirname(env_file), exist_ok=True)
    with open(env_file, "w") as fp:
        fp.write(cfg)
    msg = "iRODS configuration {0} for user {1}: {2}"
    click.echo(click.style(msg.format(server,
                                      user,
                                      env_file),
                           fg='green'))
    click.echo(cfg)
    passwd = getpass("password:")
    with open(auth_file, "w") as fp:
        pw = password_obfuscation.encode(passwd)
        fp.write(pw)
    msg = "auth file written to {0}"
    click.echo(click.style(msg.format(auth_file),
                           fg='green'))
