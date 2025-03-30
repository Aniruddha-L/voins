// SPDX-License-Identifier: MIT 
pragma solidity 0.8.19;

contract Users{
    string user;
    uint hospital; 
    uint insurance;

    function setUser(string memory User, uint Hospital, uint Insurance) public {
        user = User;
        hospital = Hospital;
        insurance = Insurance;
    }
    function getUser() public view returns(string memory){
        return user;
    }
    function getHospital() public view returns(uint){
        return hospital;
    }
    function getIns() public view returns(uint){
        return insurance;
    }

}