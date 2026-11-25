from compliance_tracker.constants import DB_CONNECTION_STRING
from compliance_tracker.db import Database


def main() -> None:
    print("Hello from compliance-tracker!")
    db = Database(DB_CONNECTION_STRING)
