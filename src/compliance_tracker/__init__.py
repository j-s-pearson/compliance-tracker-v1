import argparse

from compliance_tracker.commands import register_add, register_list
from compliance_tracker.constants import DB_CONNECTION_STRING
from compliance_tracker.db import Database
from compliance_tracker.handlers import handler_add, handler_list


def main() -> None:
    db = Database(DB_CONNECTION_STRING)

    parser = argparse.ArgumentParser(
        description="Track document expiration dates."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    register_add(subparsers, handler_add, db.add)
    register_list(subparsers, handler_list, db.list)

    args = parser.parse_args()
    args.handler(args)
