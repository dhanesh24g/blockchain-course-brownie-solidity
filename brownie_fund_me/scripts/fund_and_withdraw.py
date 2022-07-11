from brownie import FundMe
from scripts.supporting_script import get_account

fund_me = FundMe[-1]
account = get_account()


def fund():
    entrance_fee = fund_me.getEntranceFee()
    print(f"The entry fee is {entrance_fee}")
    print("Funding..")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    print("Withdrawing funds..")
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
