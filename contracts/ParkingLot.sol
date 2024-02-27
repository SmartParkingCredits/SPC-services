pragma solidity ^0.8.0;

contract ParkingLot {
    address public owner;
    mapping(address => uint256) public entryTimes;
    mapping(address => uint256) public etherCredit;
    uint256 public hourlyRate = 0.1 gwei;
    uint256 public totalCarsEntered = 0;
    uint256 public totalCarsLeft = 0;

    event CarEntered(address indexed car, uint256 entryTime, uint256 ethCredit);
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
        etherCredit[msg.sender] = msg.value;
        totalCarsEntered++;
        emit CarEntered(msg.sender, block.timestamp, msg.value);
    }

    function exit() external {
        require(entryTimes[msg.sender] > 0, "Car not registered");
        uint256 parkedSeconds = block.timestamp - entryTimes[msg.sender];
        uint256 parkedHours = parkedSeconds / 3600;
        uint256 parkingFee = parkedHours * hourlyRate;

        require(etherCredit[msg.sender] >= parkingFee, "Insufficient funds to cover parking fee");
        uint256 refundAmount = etherCredit[msg.sender] - parkingFee;

        (bool sent, ) = payable(msg.sender).call{value: refundAmount}("");
        require(sent, "Failed to send Ether");

        totalCarsLeft++;
        delete entryTimes[msg.sender];
        delete etherCredit[msg.sender];

        emit CarExited(msg.sender, block.timestamp, parkingFee);
    }

    function exit2() external {
        totalCarsLeft++;
        emit CarExited(msg.sender, block.timestamp, 0);
    }

    function setHourlyRate(uint256 newRate) external onlyOwner {
        hourlyRate = newRate;
    }

    function withdrawFunds() external onlyOwner {
        (bool sent, ) = payable(owner).call{value: address(this).balance}("");
        require(sent, "Failed to send Ether");
    }
}
