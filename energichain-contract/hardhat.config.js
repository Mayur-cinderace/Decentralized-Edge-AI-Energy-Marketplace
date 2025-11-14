require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.0",

  networks: {
    // <-- MATCH THE PORT FROM YOUR WORKSPACE
    localhost: {
      url: "http://127.0.0.1:7545"   // ← change if your workspace uses another port
    },
    // optional alias
    ganache: {
      url: "http://127.0.0.1:7545"
    }
  }
};