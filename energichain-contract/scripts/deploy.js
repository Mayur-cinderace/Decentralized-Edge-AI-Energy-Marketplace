const fs = require('fs');
const path = require('path');

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  const EnergyOffer = await ethers.getContractFactory("EnergyOffer");
  const contract = await EnergyOffer.deploy();
  try {
    await contract.waitForDeployment();
    const address = await contract.getAddress();
    console.log("Deployed to:", address);

    const ROOT = path.resolve(__dirname, "..");
    const configPath = path.join(ROOT, "energichain_backend", "public", "config", "contract-address.json");
    console.log("Saving to:", configPath);

    const configDir = path.dirname(configPath);
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true });
      console.log("Created folder:", configDir);
    }

    let config = {};
    if (fs.existsSync(configPath)) {
      try {
        config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      } catch (e) {
        console.log("Config file corrupted, resetting...");
      }
    }

    const network = await ethers.provider.getNetwork();
    const chainId = network.chainId;
    config[chainId] = address;
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));

    console.log("contract-address.json updated successfully!");
    console.log("Open dashboard: http://localhost:5000/dashboard.html");
  } catch (error) {
    console.error("Deployment failed:", error);
    throw error;
  }
}

main().catch((error) => {
  console.error("Deployment failed:", error);
  process.exit(1);
});