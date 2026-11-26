import sqlite3
from argparse import Namespace

from compliance_tracker.date_helpers import date_to_iso, get_now_iso, is_before_now


def handler_add(args: Namespace, callback) -> None:
    try:
        args.expires = date_to_iso(args.expires)
    except ValueError as e:
        print(e)
        return

    status = "expired" if is_before_now(args.expires) else "valid"
    now = get_now_iso()

    try:
        callback(args.title, args.expires, args.notify, status, now)
    except sqlite3.Error as e:
        print(f"problem when adding document: {e}")
        return

def handler_list(args: Namespace, callback) -> None:
    documents = callback()

    if len(documents) == 0:
        print("no documents...")
        return

    print(f"{'id':^3} | {'title':^25} | {'expires at':^10} | {'notify at':^10} | {'status':^10}")
    print("-" * 70)

    for doc in documents:
        print(f"{doc[0]:^3} | {doc[1]:<25} | {doc[2]:^10} | {doc[3]:^10} | {doc[4]:^10}")
    print("-" * 70)
