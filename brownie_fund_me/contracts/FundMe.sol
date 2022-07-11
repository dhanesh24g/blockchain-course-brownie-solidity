// SPDX-License-Identifier: Dhanesh

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

// Oracles import works like above

contract FundMe {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountMapping;
    address public owner;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    // Creating function to accept Payment
    function fund() public payable {
        // Check for $50
        uint256 minimumUSD = 50 * 10**18;
        require(
            getCovertedAmount(msg.value) >= minimumUSD,
            "You need to spend more ETH !"
        );
        addressToAmountMapping[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    // To enable multiple contracts to use this Owner feature (Make it reusable, instead of function specific)
    modifier onlyOwner() {
        require(
            msg.sender == owner,
            "You do not have permission to execute this function !"
        );
        _;
    }

    function withdraw() public payable onlyOwner {
        // Only contract admin/owner should use this, in this case I am
        //require(msg.sender == owner, "You do not have permission to execute this function !");
        payable(msg.sender).transfer(address(this).balance);
        // Alter the balance of the funders
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountMapping[funder] = 0;
        }
        // Reset funders Array
        funders = new address[](0);
    }

    function getPrice() public view returns (uint256) {
        /* (uint80 roundId,
         int256 answer,
         uint256 startedAt,
         uint256 updatedAt,
         uint80 answeredInRound) = priceFeed.latestRoundData();
         return uint256(answer); */

        // Above 4 unused variables can be avoided by below syntax
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10**10);
        //ETH to USD = 122036033153 ($ 1220.36033153)
    }

    function getCovertedAmount(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountUSD = (ethAmount * ethPrice) / 10**18;
        // Dividing by 18(wei) ZEROES
        return ethAmountUSD;
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;

        return (minUSD * precision) / price;
    }
}
