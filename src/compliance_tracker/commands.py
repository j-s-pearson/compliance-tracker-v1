from _collections_abc import Callable
from argparse import ArgumentParser, _SubParsersAction
from functools import partial
from typing import Any


def register_add(parser: _SubParsersAction,  handler: Callable[..., Any], callback: Callable[..., Any]) -> None:
    add_parser: ArgumentParser = parser.add_parser("add", help="adds a document")
    add_parser.add_argument(
        "-t", "--title",
        type=str,
        required=True,
        help="The name of the document"
    )
    add_parser.add_argument(
        "-e", "--expires",
        type=str,
        required=True,
        help="The date the document expires."
    )
    add_parser.add_argument(
        "-n", "--notify",
        default=30,
        type=int,
        help="The number of days you want to be notified before expiration. Default to 30 days.")

    add_parser.set_defaults(handler = partial(handler, callback=callback), status = None)

def register_list(parser: _SubParsersAction, handler: Callable[..., Any], callback: Callable[..., Any]) -> None:
    list_parser: ArgumentParser = parser.add_parser("list", help="list all documents")

    list_parser.set_defaults(handler = partial(handler, callback=callback))


def register_update(parser: _SubParsersAction, handler: Callable[..., Any], callback: Callable[..., Any]) -> None:
    update_parser: ArgumentParser = parser.add_parser("update", help="update a document specified by it's id")
    update_parser.add_argument(
        "-i", "--id",
        type = int,
        required = True,
        help = "the document ID, use the list command if you need to get the ID"
    )
    update_parser.add_argument(
        "-t", "--title",
        type = str,
        default = None,
        help = "updates the document title"
    )
    update_parser.add_argument(
        "-e", "--expires",
        type = str,
        default = None,
        help = "updates the document expiration date"
    )
    update_parser.add_argument(
        "-n", "--notify",
        type = int,
        default = None,
        help = "updates how many days to notify you before expiration"
    )

    update_parser.set_defaults(handler = partial(handler, callback=callback), status=None)


def register_delete(parser: _SubParsersAction, handler: Callable[..., Any], callback: Callable[..., Any]) -> None:
    del_parser: ArgumentParser = parser.add_parser("del", help = "delete a document by ID")
    del_parser.add_argument(
        "-i", "--id",
        required = True,
        type = int,
        help = "the document ID, use the list command if you need to get the ID"
    )

    del_parser.set_defaults(handler = partial(handler, callback=callback))
