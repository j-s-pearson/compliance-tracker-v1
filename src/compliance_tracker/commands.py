from argparse import ArgumentParser, _SubParsersAction


def register_add(parser: _SubParsersAction,  handler):
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
    add_parser.set_defaults(handler=handler)
