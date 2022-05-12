import argparse
import json
import logging

import requests

from cmclient.api.basics import (CompManConfig,
                                 PLAYERS, GAMES, HISTORY, CONFIG, ValidationException, TABLES)
from cmclient.api.compman_api import CompManHandler
from cmclient.api.rest import RestAdapter

RC_FILE = ".compmanrc"


def main():
    parser = argparse.ArgumentParser(description="Compman CLI client")

    # Context
    parser.add_argument(dest='context', help="The command context",
                        choices=[
                            PLAYERS, GAMES, TABLES, HISTORY, CONFIG])

    # Actions
    parser.add_argument("-l", "--list", help="list the items", required=False, action='store_true')
    parser.add_argument("-r", "--register", help="-r <name> register a new player", required=False, type=str)
    parser.add_argument("--clear", help="Clear all items", required=False, action='store_true')
    parser.add_argument("--propose", help="Propose a game", required=False, action='store_true')
    parser.add_argument("-g", "--get", help="Retrieve the item given by --id", action='store_true')
    parser.add_argument("--play", help="Play a game.", action='store_true')
    parser.add_argument("-j", "--join", help="-j <table_id>. Join a table", type=str, required=False)

    # Details
    parser.add_argument("-H", "--host", help="CompMan server host", type=str, required=False)
    parser.add_argument("-d", "--discipline", help="What kind of game?", choices=["gomoku"], required=False)
    parser.add_argument("--params", help="any parameters.", type=str)
    parser.add_argument("-s", "--size", help="table size", type=int)
    parser.add_argument("-i", "--id", help="The item's unique id", type=str)
    parser.add_argument("-R", "--rcfile", help="The resource file", type=str)

    args = parser.parse_args()
    config = get_config(args)
    adapter = RestAdapter(requests, config.host)

    res = CompManHandler(adapter, config).handle(args)

    if args.register:
        config.player = res
        write_config(config, args)
    if args.propose:
        config.table = res
        write_config(config, args)
    if args.join is not None:
        config.table = args.join
        write_config(config, args)

    print(res)


def write_config(config: CompManConfig, args):
    rc_file = args.rcfile if args.rcfile is not None else RC_FILE
    with open(rc_file, 'w') as rc:
        json.dump(config.__dict__, rc)


def get_config(args) -> CompManConfig:
    # create if it doesn't exist yet
    rc_file = args.rcfile if args.rcfile is not None else RC_FILE
    with open(rc_file, 'a+'):
        pass

    with open(rc_file, 'r+') as rc:
        content = rc.read()
        config = json.loads(content) if content else {}

    # override if provided else verify if in rc file
    if args.host is not None:
        config['host'] = args.host
    elif config.get('host') is None:
        raise ValidationException("No host in args nor .compmanrc")

    with open(rc_file, 'w') as rc:
        json.dump(config, rc)

    default_context = CompManConfig(**config)
    return default_context


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(e)
