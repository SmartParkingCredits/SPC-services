pragma solidity ^0.8.0;

contract ParkingLot {
    address public owner;
    mapping(address => uint256) public entryTimes;
    uint256 public constant hourlyRate = 0.00001 ether; // Adjust as needed

    event CarEntered(address indexed car, uint256 entryTime);
    event CarExited(address indexed car, uint256 exitTime, uint256 fee);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    function enter() external payable {
        require(msg.value >= hourlyRate, "Insufficient payment");
        entryTimes[msg.sender] = block.timestamp;
        emit CarEntered(msg.sender, block.timestamp);
    }

    function exit() external {
        require(entryTimes[msg.sender] > 0, "Car not registered");
        uint256 parkedHours = (block.timestamp - entryTimes[msg.sender]) / 3600; // Calculating parked hours
        uint256 parkingFee = parkedHours * hourlyRate;
        payable(msg.sender).transfer(parkingFee); // Refund any excess payment
        delete entryTimes[msg.sender];
        emit CarExited(msg.sender, block.timestamp, parkingFee);
    }

    function withdrawFunds() external onlyOwner {
        payable(owner).transfer(address(this).balance);
    }
}