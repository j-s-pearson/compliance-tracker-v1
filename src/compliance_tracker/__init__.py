import argparse

from compliance_tracker.commands import *
from compliance_tracker.constants import DB_CONNECTION_STRING
from compliance_tracker.db import Database
from compliance_tracker.handlers import *


def main() -> None:
    db = Database(DB_CONNECTION_STRING)

    parser = argparse.ArgumentParser(
        description="Track document expiration dates."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    register_add(subparsers, handler_add, db.add)
    register_list(subparsers, handler_list, db.list)
    register_delete(subparsers, handler_delete, db.delete)
    register_update(subparsers, handler_update, db.update)

    args = parser.parse_args()
    args.handler(args)
