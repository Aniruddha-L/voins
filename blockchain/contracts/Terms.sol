// SPDX-License-Identifier: MIT 
pragma solidity 0.8.19;

contract Terms{
    string public terms;
    function setTerms(string memory rules) public{
        terms = rules;
    }

    function getTerms() public view returns (string memory) {
        return terms;
    }
}