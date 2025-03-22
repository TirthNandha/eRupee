// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ERupee {
    string public name = "e-Rupee";
    string public symbol = "eINR";
    uint8 public decimals = 2; // 2 decimal places like INR
    uint256 public totalSupply;
    address public rbi; // Simulated RBI admin
    mapping(address => uint256) public balanceOf;
    mapping(address => uint256) public transactionCount; // Track tx for cashback

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Cashback(address indexed user, uint256 amount);

    constructor(uint256 initialSupply) {
        rbi = msg.sender;
        totalSupply = initialSupply * 10 ** decimals; // Convert to smallest unit
        balanceOf[rbi] = totalSupply;
    }

    modifier onlyRBI() {
        require(msg.sender == rbi, "Only RBI can call this");
        _;
    }

    function transfer(address to, uint256 value) public returns (bool) {
        require(to != address(0), "Invalid address");
        require(balanceOf[msg.sender] >= value, "Insufficient balance");

        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        transactionCount[msg.sender] += 1;

        // Cashback: 2% for first 10 transactions (simplified for demo)
        if (transactionCount[msg.sender] <= 10) {
            uint256 cashback = (value * 2) / 100;
            balanceOf[msg.sender] += cashback;
            emit Cashback(msg.sender, cashback);
        }

        emit Transfer(msg.sender, to, value);
        return true;
    }

    function mint(address to, uint256 value) public onlyRBI {
        balanceOf[to] += value;
        totalSupply += value;
        emit Transfer(address(0), to, value);
    }

    function getBalance(address account) public view returns (uint256) {
        return balanceOf[account];
    }
}