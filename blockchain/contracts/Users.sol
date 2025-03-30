// SPDX-License-Identifier: MIT 
pragma solidity 0.8.19;

contract Users{
    uint user;
    uint hospital; 
    uint insurance;

    function setUser(uint User, uint Hospital, uint Insurance) public {
        user = User;
        hospital = Hospital;
        insurance = Insurance;
    }
    function getUser() public view returns(uint){
        return user;
    }
    function getHospital() public view returns(uint){
        return hospital;
    }
    function getIns() public view returns(uint){
        return insurance;
    }

}