const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  
  console.log("\n" + "=".repeat(60));
  console.log("Account Information");
  console.log("=".repeat(60));
  console.log("Address:", deployer.address);
  
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  const balanceEth = hre.ethers.formatEther(balance);
  console.log("Balance:", balanceEth, "ETH");
  
  // Get network info
  const network = await hre.ethers.provider.getNetwork();
  console.log("Network:", network.name);
  console.log("Chain ID:", network.chainId);
  
  // Check if enough balance
  if (parseFloat(balanceEth) < 0.01) {
    console.log("\n⚠️  WARNING: Balance too low!");
    console.log("Need at least 0.01 ETH for deployment");
    console.log("\nGet Sepolia ETH from:");
    console.log("- https://www.alchemy.com/faucets/ethereum-sepolia");
    console.log("- https://sepolia-faucet.pk910.de/");
  } else {
    console.log("\n✅ Balance sufficient for deployment");
  }
  
  console.log("=".repeat(60) + "\n");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
