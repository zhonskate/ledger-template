import csv
from pathlib import Path

from common import ledger_format
from common import get_account_types
from common import amount_to_str

from mappings import CONCEPT_MAPPING_REVOLUT

PATH = Path(__file__).parent.parent / "reports/revolut.csv"

DUPLICATED_CONCEPTS = [
    "Apple Pay Top-Up by *9447",
    "Plan Cashback",
    "Top-Up by *2808",
]

ACCOUNT = "revolut"


def parse_date(date):
    return "/".join(list(date.split(" ")[0].split("-")))


def parse_file(file_path):
    parsed = []
    with open(file_path) as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            formatted_data = {
                "date": parse_date(row[2]),
                "concept": row[4],
                "amount": float(row[5]) - float(row[6]),
                "status": row[8],
                "total_after": row[9],
            }
            parsed.append(formatted_data)
    return parsed


def get_known_account_concept(concept):
    for key in CONCEPT_MAPPING_REVOLUT:
        if key in concept:
            return CONCEPT_MAPPING_REVOLUT[key]


if __name__ == "__main__":
    entries = parse_file(PATH)
    for entry in entries:
        if entry["concept"] in DUPLICATED_CONCEPTS:
            continue
        if entry["amount"] == 0:
            continue
        if entry["status"] == "REVERTED":
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
