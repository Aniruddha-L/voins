const Terms = artifacts.require('Terms.sol');

module.exports = function(deployer){
    deployer.deploy(Terms);
}