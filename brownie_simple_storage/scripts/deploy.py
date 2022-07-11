from brownie import accounts, config, firstContractSimpleStorage, network

# import os


def deploy_simple_storage():
    # Use Ganache specific local accounts
    account = get_account()
    # print(simple_storage)

    # Use newly created, password protected account
    # account = accounts.load("dhanesh-test-account")

    # Use .env file as account details storage
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # account = accounts.add(config["wallets"]["from_key"])
    simple_storage = firstContractSimpleStorage.deploy({"from": account})
    initial_age = simple_storage.retrieve()
    print("Initial age:", initial_age)
    transaction = simple_storage.changeVal(29, {"from": account})
    transaction.wait(1)
    print("Updated age:", simple_storage.retrieve())


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    print("Active network:", network.show_active())
    deploy_simple_storage()
