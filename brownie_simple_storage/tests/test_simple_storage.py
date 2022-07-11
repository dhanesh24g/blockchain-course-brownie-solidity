from brownie import firstContractSimpleStorage, accounts


def test_deploy():
    # Arrange
    account = accounts[0]
    simple_storage = firstContractSimpleStorage.deploy({"from": account})
    # Act
    starting_value = simple_storage.retrieve()
    expected = 25
    # Assert
    assert starting_value == expected, f"Values do not match"


def test_updated_age():
    # Arrange
    account = accounts[0]
    simple_storage = firstContractSimpleStorage.deploy({"from": account})
    # Act
    my_age = 27
    simple_storage.changeVal(my_age, {"from": account})
    # Assert
    assert my_age == simple_storage.retrieve(), "Values do not match"
