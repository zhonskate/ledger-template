EXPENSES_ACCOUNT = "Expenses:ToType"
INCOME_ACCOUNT = "Income:ToType"


def ledger_format(
    date, completed, description, destination_account, currency, amount, origin_account
):
    status = "*" if completed else "?"
    formatted = f"{date} {status} {description}\n\
\t{destination_account}\t{currency}{amount}\n\
\t{origin_account}"
    return formatted


def get_account_types(amount, account):
    if amount > 0:
        return INCOME_ACCOUNT, account
    else:
        return account, EXPENSES_ACCOUNT


def amount_to_float(amount):
    return float(amount.replace(".", "").replace(",", "."))


def amount_to_str(amount):
    if amount < 0:
        amount *= -1
    return str(amount).replace(".", ",")
