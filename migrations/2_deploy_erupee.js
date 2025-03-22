const ERupee = artifacts.require("ERupee");

module.exports = function (deployer) {
  deployer.deploy(ERupee, 1000000); // Initial supply: 1,000,000 eINR
};