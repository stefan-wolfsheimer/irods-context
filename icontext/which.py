import click
from icontext.util import get_current_env_file
from icontext.util import get_current_server_and_user


@click.command()
def which():
    "Display current context (server, user, irods enviornment file)."
    (server, user) = get_current_server_and_user()
    cfg_file = get_current_env_file()
    fmt = "server:\t{0}\nuser:\t{1}\nenv:\t{2}"
    click.echo(fmt.format("" if server is None else server,
                          "" if user is None else user,
                          cfg_file))
