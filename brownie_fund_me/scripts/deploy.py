from brownie import FundMe, MockV3Aggregator, network, config
from scripts.supporting_script import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    deploy_mocks,
)


def deploy_fund_me():
    account = get_account()

    print(f"Account address is {account.address} and balance is {account.balance()}")

    # If using persistent network like Rinkeby then use associated address, ELSE use Mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        print(f"Active network is {network.show_active()}")
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    # Pass priceFeed address to FundMe contract & will be initialized in constructor
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        # publish_source=(network.show_active() != "development"),
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
