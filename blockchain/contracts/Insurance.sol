// SPDX-License-Identifier: UNLICENSED 
pragma solidity 0.8.19;

contract Insurance{
    string public insurance;
    string [] public insuranceSet;
    function setIns(string memory ins) public{
        insurance = ins;
    }
    function getIns() public view returns(string memory){
        return insurance;
    }

    function setInsS(string[] memory ins) public{
        insuranceSet = ins;
    }
    function getInsS() public view returns(string[] memory){
        return insuranceSet;
    }
}