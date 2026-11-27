import sqlite3
from _collections_abc import Callable
from argparse import Namespace
from typing import Any

from compliance_tracker.date_helpers import date_to_iso, get_now_iso, is_before_now


def handler_add(args: Namespace, callback: Callable[..., Any]) -> None:
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

def handler_list(args: Namespace, callback: Callable[..., Any]) -> None:
    documents: list[Any] = callback()

    if len(documents) == 0:
        print("no documents...")
        return

    print(f"{'id':^3} | {'title':^25} | {'expires at':^10} | {'notify at':^10} | {'status':^10}")
    print("-" * 70)

    for doc in documents:
        print(f"{doc[0]:^3} | {doc[1]:<25} | {doc[2]:^10} | {doc[3]:^10} | {doc[4]:^10}")
    print("-" * 70)

def handler_update(args: Namespace, callback: Callable[..., Any]) -> None:
    if args.title == None and args.expires == None and args.notify == None:
        print("nothing specified to update, expected at least a title, expiration date, or notification period")
        return

    if args.title != None:
        args.title = args.title.strip()
        if args.title == "":
            print("title can't be updated to empty")

    if args.expires != None:
        try:
            args.expires = date_to_iso(args.expires)
        except ValueError as e:
            print(e)
            return
        args.status = "expired" if is_before_now(args.expires) else "valid"

    if args.notify != None and args.notify < 1:
        print("can't have a notification period less than 1 day")
        return

    updated_at = get_now_iso()

    callback(args.id, args.title, args.expires, args.notify, args.status, updated_at)
