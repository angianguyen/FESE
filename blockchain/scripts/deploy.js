/**
 * Deployment script for FESE smart contracts
 */
const hre = require("hardhat");

async function main() {
  console.log("Deploying FESE Token...");
  
  // Get deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);
  
  // Deploy FESE Token
  const FESEToken = await hre.ethers.getContractFactory("FESEToken");
  const fese = await FESEToken.deploy();
  await fese.waitForDeployment();
  
  const address = await fese.getAddress();
  console.log("FESE Token deployed to:", address);
  
  // Save deployment info
  const fs = require("fs");
  const deploymentInfo = {
    network: hre.network.name,
    contractAddress: address,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
  };
  
  fs.writeFileSync(
    "./deployments.json",
    JSON.stringify(deploymentInfo, null, 2)
  );
  
  console.log("Deployment info saved to deployments.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
