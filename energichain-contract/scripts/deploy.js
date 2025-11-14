const fs = require('fs');
const path = require('path');

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  const EnergyOffer = await ethers.getContractFactory("EnergyOffer");
  const contract = await EnergyOffer.deploy();
  await contract.waitForDeployment();
  const address = await contract.getAddress();

  console.log("Deployed to:", address);

  // ABSOLUTE PATH — NO CHANCE OF ERROR
  const ROOT = path.resolve(__dirname, ".."); // D:\final\Decentralized-Edge-AI-Energy-Marketplace
  const configPath = path.join(ROOT, "energichain_backend", "public", "config", "contract-address.json");

  console.log("Saving to:", configPath);

  // Create config folder if not exists
  const configDir = path.dirname(configPath);
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
    console.log("Created folder:", configDir);
  }

  // Read or create config
  let config = {};
  if (fs.existsSync(configPath)) {
    try {
      config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    } catch (e) {
      console.log("Config file corrupted, resetting...");
    }
  }

  // Save address for Ganache (chainId 1337)
  config["1337"] = address;
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));

  console.log("contract-address.json updated successfully!");
  console.log("Open dashboard: http://localhost:5000/dashboard.html");
}

main().catch((error) => {
  console.error("Deployment failed:", error);
  process.exit(1);
});