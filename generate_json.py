import json
import random
from random import randint,choice
from datetime import date, timedelta
from faker import Faker
import boto3

fake = Faker()

transactions_per_day = 106
# dictionary to put transactions and descriptions together
banking_transactions = {
    "Withdrawals": ["Cash Withdrawal", "ATM Withdrawal", "Check Withdrawal"],
    "Deposits": ["Cash Deposit", "Check Deposit", "Direct Deposit"],
    "Transfers": ["Internal Transfer", "External Transfer"],
    "Payments": ["Bill Payment", "ACH Payment", "Wire Transfer", "Credit Card Payment"],
    "Purchases": ["Debit Card Purchase", "Credit Card Purchase"],
    "Loans and Advances": ["Loan Disbursement", "Loan Repayment"],
    "Standing Orders and Direct Debits": ["Standing Order", "Direct Debit"],
    "Electronic Transactions": ["Online Banking", "Mobile Banking"],
    "Investment Transactions": ["Buying and Selling Securities", "Dividends"],
    "Fees and Charges": ["Service Fees", "ATM Fees", "Overdraft Fees"],
    "Interest and Adjustments": ["Interest Credit", "Interest Debit", "Adjustments"]
}

# print(banking_transactions)
def find_transaction(description):
    for transaction, descriptions in banking_transactions.items():
        if description in descriptions:
            return transaction
    return None

# Example usage:
all_values = [value for sublist in banking_transactions.values() for value in sublist]
# print(all_values)
value = random.choice(all_values)
key = find_transaction(value)
# if key:
#     print(f"The key for '{value}' is '{key}'")
# else:
#     print("Value Not Found!")

transaction_ids = []
for _ in range(transactions_per_day):
    ids = fake.unique.bothify(text='T######')
    transaction_ids.append(ids)
assert len(set(transaction_ids)) == len(transaction_ids)
# print(transaction_ids[:5])

account_ids = []
for _ in range(50):
    acc_ids = fake.bothify(text='A#####')
    account_ids.append(acc_ids)
# print(account_ids[:5])

transaction_information = {}

def generate_one_transaction(account_id, current_date):
    if account_id not in transaction_information:
        # generate information needed
        transaction_information[account_id] = {
            "transaction_id" : choice(transaction_ids)
        }
    transaction_data = transaction_information[account_id].copy()
    transaction_data["account_id"] = choice(account_ids)
    transaction_date = str(current_date)
    transaction_data["date"] = transaction_date
    transaction_data["amount"] = round(random.uniform(10, 10000), 2)
    transaction_data["description"] = random.choice(all_values)
    transaction_data["transaction_type"] = find_transaction(transaction_data["description"])
    transaction_data["branch_id"] = fake.bothify("B#")

    return transaction_data

def generate_transactions(num_transactions, current_date):
    transactions = []
    for _ in range(num_transactions):
        transactions.append(generate_one_transaction(choice(account_ids), current_date))
    return transactions

bucket = "json-test-mock"
key = "mock_data.json"
s3 = boto3.client('s3')
response = s3.get_object(Bucket=bucket, Key=key)
def write_to_json(data, filename):
    with open(filename, 'r') as file:
        json_data = json.load(response['Body'])

        updated_data = json_data + data

    with open(filename, 'w') as file:
        json.dump(updated_data, file, indent=4)

def generate_data(current_date, date_str):
    transactions = generate_transactions(transactions_per_day, current_date)
    # write_to_json(transactions, f"transactions_{date_str}.json")
    write_to_json(transactions, f"/tmp/transactions_{date_str}.json")
    print(f"Generated mock transaction data transactions_{date_str}.json and saved in json files")
    return


# start_date = date(2024, 6, 26)  # Adjust start date
# end_date = date.today()
#
# for current_date in range((end_date - start_date).days + 1):
#     # Generate Date
#     current_date = start_date + timedelta(days=current_date)
#     date_str = str(current_date)
#
# generate_data(current_date, date_str)
# # print(generate_transactions(2, date_str))
