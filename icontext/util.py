import re
from os.path import expanduser
from os.path import isdir
from os.path import join
from os import listdir
from typing import Pattern


TEMPLATE_WITHOUT_SSL = """
{{
    "irods_host": "{irods_host}",
    "irods_port": {irods_port},
    "irods_user_name": "{irods_user_name}",
    "irods_zone_name": "{irods_zone_name}"
}}
"""

TEMPLATE_WITH_SSL = """
{{
    "irods_host": "{irods_host}",
    "irods_port": {irods_port},
    "irods_user_name": "{irods_user_name}",
    "irods_zone_name": "{irods_zone_name}",
    "irods_authentication_scheme": "{irods_authentication_scheme}",
    "irods_encryption_num_hash_rounds": 16,
    "irods_client_server_policy": "CS_NEG_REQUIRE",
    "irods_encryption_algorithm": "AES-256-CBC",
    "irods_encryption_salt_size": 8,
    "irods_ssl_verify_server": "none",
    "irods_encryption_key_size": 32
}}
"""


def get_config_dir(server=None, user=None):
    if server is None:
        return expanduser('~/.irods/icontext')
    else:
        ret = join(expanduser('~/.irods/icontext'), server)
        if user is None:
            return ret
        return join(ret, user)


def get_config_file(server, user):
    return join(get_config_dir(server, user), 'irods_environment.json')


def get_auth_file(server, user):
    return join(get_config_dir(server, user), '.irodsA')


def string_starts_with(s, pattern):
    m = pattern.search(s)
    if m is None:
        return False
    else:
        return m.span()[0] == 0 and m.span()[1] > 0


def get_servers(pattern=None):
    context_dir = get_config_dir()
    pattern = compile_pattern(pattern)
    if isdir(context_dir):
        for d in listdir(context_dir):
            if string_starts_with(d, pattern) and isdir(join(context_dir, d)):
                yield d
    raise StopIteration


def get_users(server, pattern=None):
    context_dir = get_config_dir()
    dirname = join(context_dir, server)
    pattern = compile_pattern(pattern)
    if isdir(dirname):
        for d1 in listdir(dirname):
            if string_starts_with(d1, pattern) and isdir(join(dirname, d1)):
                yield d1
    raise StopIteration


def compile_pattern(pattern=None):
    if pattern is None:
        return re.compile(".*")
    elif isinstance(pattern, Pattern):
        return pattern
    else:
        try:
            return re.compile(pattern)
        except Exception:
            return re.compile(re.escape(pattern))


def complete_servers(ctx, args, incomplete):
    ret = [s
           for s in get_servers()
           if s.startswith(incomplete)]
    ret.sort()
    return ret


def complete_users_regex_server(ctx, args, incomplete):
    server_pattern = args[-1]
    users = {}
    for s in get_servers(pattern=server_pattern):
        for u in get_users(s):
            if u.startswith(incomplete):
                users[u] = True
    users = list(users.keys())
    users.sort()
    return users


def complete_users(ctx, args, incomplete):
    server_pattern = re.compile(re.escape(args[-1]))
    users = {}
    for s in get_servers(pattern=server_pattern):
        for u in get_users(s):
            if u.startswith(incomplete):
                users[u] = True
    users = list(users.keys())
    users.sort()
    return users


def input_value(prompt, value):
    if value is None:
        ret = input("{0}:".format(prompt))
    else:
        ret = input("{0} [{1}]:".format(prompt, value))
    if value and not ret:
        return value
    else:
        return ret
