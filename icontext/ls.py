import click
from icontext.util import complete_servers
from icontext.util import complete_users_regex_server
from icontext.util import get_servers
from icontext.util import get_users


def print_table(header, items):
    lengths = [len(h) for h in header]
    for item in items:
        for i in range(0, len(item)):
            if len(item[i]) > lengths[i]:
                lengths[i] = len(item[i])
    fmt = '| ' + ' | '.join(['{:>' + str(l) + '}' for l in lengths]) + ' |'
    headline = "+-" + "-+-".join(["-" * l for l in lengths]) + "-+"
    click.echo(headline)
    click.echo(fmt.format(*header))
    click.echo(headline)
    for item in items:
        click.echo(fmt.format(*item))
    click.echo(headline)


@click.command()
@click.argument("server",
                required=False,
                type=click.STRING,
                autocompletion=complete_servers)
@click.argument("user",
                required=False,
                type=click.STRING, autocompletion=complete_users_regex_server)
def ls(server, user):
    "List contexts."
    data = []
    for s in get_servers(pattern=server):
        for u in get_users(s, pattern=user):
            data.append((s, u))
    if len(data) > 0:
        data.sort()
        print_table(("Server", "User"),
                    data)
