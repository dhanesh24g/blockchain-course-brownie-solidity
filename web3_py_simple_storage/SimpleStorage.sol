// SPDX-License-Identifier: Dhanesh

pragma solidity ^0.6.0;

contract firstContractSimpleStorage {
    // unit will be initialized to 0, if value is not specified
    uint8 currentAge = 25;
    bool isSuccess = true;
    //address val = 0xb794f5ea0ba39494ce839613fffba74279579268;

    struct People {
        string name;
        uint8 age;
    }

    People[] public people;
    mapping(string => uint8) public nameToAge;

    // Function to change value of currentAge
    function changeVal(uint8 _newAge) public returns (uint8) {
        currentAge = _newAge;
        return currentAge;
    }

    // Function to view the value of currentAge
    function retrieve() public view returns (uint8) {
        return currentAge;
    }

    // Function to add person to People array
    function addPerson(string memory _name, uint8 _age) public {
        people.push(People({age: _age, name: _name}));
        //Adding mapping here
        nameToAge[_name] = _age;
    }

    /*function viewPerson () public view returns (People) {
        return (people);        
    }*/
}
