import argparse

from compliance_tracker.commands import register_add
from compliance_tracker.constants import DB_CONNECTION_STRING
from compliance_tracker.db import Database
from compliance_tracker.handlers import handler_add


def main() -> None:
    db = Database(DB_CONNECTION_STRING)

    parser = argparse.ArgumentParser(
        description="Track document expiration dates."
    )

    subparsers = parser.add_subparsers(required=True)
