// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IOracle {
    function getReserveValue() external view returns (uint256);
}

contract Stablecoin{
    string public name = "KR Stablecoin";
    string public symbol = "KRSC";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    address public owner;
    address public oracleAddress;

    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Mint(address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    constructor(uint256 _initialSupply, address _oracleAddress) {
        totalSupply = _initialSupply * 10 ** uint256(decimals);
        balanceOf[owner] = totalSupply;
        owner = msg.sender;
        oracleAddress = _oracleAddress;
        emit Transfer(address(0), owner, totalSupply);
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function mint(address _to, uint256 _value) public onlyOwner returns (bool success) {
        balanceOf[_to] += _value;
        totalSupply += _value;
        emit Mint(_to, _value);
        emit Transfer(address(0), _to, _value);
        return true;
    }

    function burn(address _from, uint256 _value) public onlyOwner returns (bool success) {
        require(balanceOf[_from] >= _value, "Insufficient balance");
        balanceOf[_from] -= _value;
        totalSupply -= _value;
        emit Burn(_from, _value);
        emit Transfer(_from, address(0), _value);
        return true;
    }

    function verifyCollateral() public view returns (bool) {
        IOracle oracle = IOracle(oracleAddress);
        uint256 reserveValue = oracle.getReserveValue();
        uint256 requiredReserveValue = totalSupply / (10 ** uint256(decimals));
        return reserveValue >= requiredReserveValue;
    }
}