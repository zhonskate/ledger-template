import csv
from pathlib import Path

from common import ledger_format
from common import get_account_types
from common import amount_to_float
from common import amount_to_str

from mappings import CONCEPT_MAPPING_OPENBANK


PATH = Path(__file__).parent.parent / "reports/openbank.csv"

ACCOUNT = "openbank"


def flip_date(date):
    return "/".join(list(reversed(date.split("/"))))


def parse_file(file_path):
    parsed = []
    with open(file_path) as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            formatted_data = {
                "date": flip_date(row[1]),
                "concept": row[5],
                "amount": amount_to_float(row[7]),
                "total_after": row[9],
            }
            parsed.append(formatted_data)
    return parsed


def get_known_account_concept(concept):
    for key in CONCEPT_MAPPING_OPENBANK:
        if key in concept:
            return CONCEPT_MAPPING_OPENBANK[key]


if __name__ == "__main__":
    entries = parse_file(PATH)
    for entry in reversed(entries):
        if entry["amount"] == 0:
            continue
        origin_account, destination_account = get_account_types(
            entry["amount"], ACCOUNT
        )

        if known_account := get_known_account_concept(entry["concept"]):
            destination_account = known_account

        formatted_entry = ledger_format(
            entry["date"],
            True,
            entry["concept"],
            destination_account,
            "€",
            amount_to_str(entry["amount"]),
            origin_account,
        )
        print(formatted_entry)
        print("\n")
