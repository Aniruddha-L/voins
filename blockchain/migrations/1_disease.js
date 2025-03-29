const disease = artifacts.require('Disease.sol');
const Hospital = artifacts.require('Hospitals.sol');
const Ins = artifacts.require('Insurance.sol');
const terms = artifacts.require('Terms.sol')

module.exports = function(deployer){
    deployer.deploy(disease);
    deployer.deploy(Hospital);
    deployer.deploy(Ins);
    deployer.deploy(terms);
}