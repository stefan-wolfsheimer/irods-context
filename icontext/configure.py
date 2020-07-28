import click
import json
from icontext.util import TEMPLATE_WITH_SSL
from icontext.util import TEMPLATE_WITHOUT_SSL
from icontext.util import get_env_file
from icontext.util import input_value
from icontext.util import complete_servers
from icontext.util import complete_users
from icontext.use import switch_context


@click.command()
@click.argument("server",
                type=click.STRING,
                autocompletion=complete_servers)
@click.argument("user",
                type=click.STRING, autocompletion=complete_users)
@click.option('-s', '--ssl', default="auto", type=click.Choice(['auto',
                                                                'yes',
                                                                'no']))
@click.option('-p', '--with-pam', default=False, is_flag=True)
@click.option('-u', '--use', default=False, is_flag=True)
def configure(server, user, ssl, with_pam, use):
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
    if scheme == "pam":
        ssl = "yes"
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
    scheme = cfg_args['irods_authentication_scheme'].lower()
    if scheme == 'pam' and ssl == "no":
        msg = "inconsistent flags: --with-ssl=no and scheme PAM"
        click.echo(click.style(msg, fg='red'))
        exit(8)
    if cfg.get("irods_client_server_policy", None) == "CS_NEG_REQUIRE":
        cfg_is_ssl = True
    else:
        cfg_is_ssl = False
    if (scheme == 'pam' or ssl == 'yes'):
        # force ssl
        if cfg_is_ssl:
            cfg.update(cfg_args)
            new_config = json.dumps(cfg, indent=4)
        else:
            new_config = TEMPLATE_WITH_SSL.format(**cfg_args)
    elif ssl == 'no':
        # force no ssl
        if cfg_is_ssl:
            new_config = TEMPLATE_WITHOUT_SSL.format(**cfg_args)
        else:
            cfg.update(cfg_args)
            new_config = json.dumps(cfg, indent=4)
    else:
        # ssl == 'auto'
        cfg.update(cfg_args)
        new_config = json.dumps(cfg, indent=4)
    click.echo('change config from:')
    click.echo(click.style(old_config, fg='red'))
    click.echo('change config to:')
    click.echo(click.style(new_config, fg='green'))
    click.echo('change? [y/n]', nl=False)
    answer = click.getchar()
    if answer == 'y':
        with open(env_file, "w") as fp:
            fp.write(new_config)
        click.echo('')
        if use:
            switch_context(server, user)
    else:
        click.echo(click.style("configuration not changed", fg='red'))
