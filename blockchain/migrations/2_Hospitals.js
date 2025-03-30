const Hospital = artifacts.require('Hospitals.sol');

module.exports = function(deployer){
    deployer.deploy(Hospital);
}