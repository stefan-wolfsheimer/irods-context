import click
import os
from os.path import expanduser
from icontext.util import update_env_file_variable


@click.command()
def unuse():
    env_file = expanduser('~/.irods/irods_environment.json')
    auth_file = expanduser('~/.irods/.irodsA')
    os.environ['IRODS_ENVIRONMENT_FILE'] = env_file
    os.environ['IRODS_AUTHENTICATION_FILE'] = auth_file
    update_env_file_variable()
