import argparse

from compliance_tracker.commands import register_add
from compliance_tracker.constants import DB_CONNECTION_STRING
from compliance_tracker.date_helpers import *
from compliance_tracker.db import Database
from compliance_tracker.handlers import handler_add


def main() -> None:
    db = Database(DB_CONNECTION_STRING)

    parser = argparse.ArgumentParser(
        description="Track document expiration dates."
    )

    subparsers = parser.add_subparsers(required=True)

    register_add(subparsers, handler_add)

    print(get_now_iso())
    print(date_to_iso("05/02/2026"))
    print(is_before_now(date_to_iso("05/02/2026")))
