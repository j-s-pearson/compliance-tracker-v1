import sqlite3
from argparse import Namespace

from compliance_tracker.date_helpers import date_to_iso, get_now_iso, is_before_now
from compliance_tracker.db import Database


def handler_add(args: Namespace, db: Database) -> None:
    try:
        args.expires = date_to_iso(args.expires)
    except ValueError as e:
        print(e)
        return

    status = "expired" if is_before_now(args.expires) else "valid"
    now = get_now_iso()

    try:
        db.add(args.title, args.expires, args.notify, status, now)
    except sqlite3.Error as e:
        print(f"Error adding document: {e.sqlite_errorname}")
        return
