// SPDX-License-Identifier: MIT 
pragma solidity 0.8.19;

contract Disease{
    string public disease;
    function setDisease(string memory dis) public{
        disease = dis;
    }

    function getDisease() public view returns (string memory){
        return disease;
    }
}