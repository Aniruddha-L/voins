// SPDX-License-Identifier: MIT 
pragma solidity 0.8.19;

contract Terms{
    string public terms;
    uint insBlk;
    function setTerms(string memory rules, uint ins) public{
        terms = rules;
        insBlk = ins;
    }

    function getTerms() public view returns (string memory) {
        return terms;
    }
    function getInsBlk() public view returns (uint) {
        return insBlk;
    }
}