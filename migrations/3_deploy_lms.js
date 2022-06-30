const lms = artifacts.require("lms");

module.exports = function (deployer) {
  deployer.deploy(lms);
};
