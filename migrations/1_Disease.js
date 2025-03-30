const disease = artifacts.require('Disease.sol');

module.exports = function(deployer){
    deployer.deploy(disease);
}