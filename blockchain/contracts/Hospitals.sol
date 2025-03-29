// SPDX-License-Identifier: MIT 
pragma solidity 0.8.19;

contract Hospitals{
    string[] HospitalList;
    string Hospital;

    function addHospital(string[] memory hospital) public{
        uint length = hospital.length;
        for (uint i=0;i<length;i++){
            HospitalList.push(hospital[i]);
        }
    }
    function getHospitals() public view returns (string[] memory){
        return HospitalList;
    }

    function setHospital(string memory hospital) public{
        Hospital = hospital;
    }
    function getHospital() public view returns (string memory){
        return Hospital;
    }
}