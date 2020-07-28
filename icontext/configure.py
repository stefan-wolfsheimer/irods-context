import click
import json
from icontext.util import TEMPLATE_WITH_SSL
from icontext.util import TEMPLATE_WITHOUT_SSL
from icontext.util import get_env_file
from icontext.util import input_value
from icontext.util import complete_servers
from icontext.util import complete_users


@click.command()
@click.argument("server",
                type=click.STRING,
                autocompletion=complete_servers)
@click.argument("user",
                type=click.STRING, autocompletion=complete_users)
@click.option('-s', '--with-ssl', default=False, is_flag=True)
@click.option('-p', '--with-pam', default=False, is_flag=True)
def configure(server, user, with_ssl, with_pam):
    env_file = get_env_file(server, user)
    with open(env_file) as fp:
        old_config = fp.read()
    try:
        cfg = json.loads(old_config)
    except Exception:
        msg = "failed to load config file {0}".format(env_file)
        click.echo(click.style(msg, fg='red'))
        with open(env_file) as fp:
            click.echo(fp.read())
        raise
    if with_pam:
        scheme = "pam"
    else:
        scheme = cfg.get("irods_authentication_scheme", "native")
    cfg_args = {"irods_host": input_value("host",
                                          cfg.get("irods_host")),
                "irods_port": int(input_value("port",
                                              cfg.get("irods_port"))),
                "irods_user_name": input_value("user",
                                               cfg.get("irods_user_name")),
                "irods_zone_name": input_value("zone",
                                               cfg.get("irods_zone_name")),
                "irods_authentication_scheme": input_value("auth scheme",
                                                           scheme)}
    if with_pam or with_ssl:
        template = TEMPLATE_WITH_SSL
    else:
        template = TEMPLATE_WITHOUT_SSL
    new_config = template.format(**cfg_args)
    click.echo('change config from:')
    click.echo(click.style(old_config, fg='red'))
    click.echo('change config to:')
    click.echo(click.style(new_config, fg='green'))
    click.echo('change? [y/n]', nl=False)
    answer = click.getchar()
    if answer == 'y':
        with open(env_file, "w") as fp:
            fp.write(new_config)
    else:
        click.echo(click.style("configuration not changed", fg='red'))
