from brownie import firstContractSimpleStorage, accounts


def read_contract():
    # firstContractSimpleStorage array will have addresses stored (For Rinkeby network)
    # Index 0 will fetch first compiled code, whereas -1 will fetch the latest
    simple_storage = firstContractSimpleStorage[-1]

    # We need Address & ABI to make function call
    print(simple_storage.retrieve())


def main():
    read_contract()
