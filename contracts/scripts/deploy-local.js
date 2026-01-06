const hre = require("hardhat");
const fs = require('fs');
const path = require('path');

async function main() {
  console.log("\n" + "=".repeat(60));
  console.log("🚀 STREAMCREDIT - LOCAL DEPLOYMENT (Hardhat Network)");
  console.log("=".repeat(60) + "\n");

  const [deployer] = await hre.ethers.getSigners();
  console.log("📍 Deploying with account:", deployer.address);
  
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("💰 Account balance:", hre.ethers.formatEther(balance), "ETH\n");

  // Deploy MockUSDC
  console.log("1️⃣ Deploying MockUSDC...");
  const MockUSDC = await hre.ethers.getContractFactory("MockUSDC");
  const usdc = await MockUSDC.deploy();
  await usdc.waitForDeployment();
  const usdcAddress = await usdc.getAddress();
  console.log("✅ MockUSDC deployed to:", usdcAddress);

  // Deploy MockVerifier (for testing)
  console.log("\n2️⃣ Deploying MockVerifier (Testing Only)...");
  const MockVerifier = await hre.ethers.getContractFactory("MockVerifier");
  const verifier = await MockVerifier.deploy();
  await verifier.waitForDeployment();
  const verifierAddress = await verifier.getAddress();
  console.log("✅ MockVerifier deployed to:", verifierAddress);
  console.log("⚠️  WARNING: MockVerifier always returns TRUE - FOR TESTING ONLY!");

  // Deploy StreamCredit
  console.log("\n3️⃣ Deploying StreamCredit...");
  const StreamCredit = await hre.ethers.getContractFactory("StreamCredit");
  const streamCredit = await StreamCredit.deploy(verifierAddress, usdcAddress);
  await streamCredit.waitForDeployment();
  const streamCreditAddress = await streamCredit.getAddress();
  console.log("✅ StreamCredit deployed to:", streamCreditAddress);

  // Add initial liquidity to StreamCredit
  console.log("\n4️⃣ Setting up initial liquidity...");
  const liquidityAmount = hre.ethers.parseUnits("100000", 6); // 100k USDC
  
  // Mint USDC to deployer
  await usdc.faucet(liquidityAmount);
  console.log("✅ Minted 100,000 USDC to deployer");
  
  // Approve StreamCredit to spend USDC
  await usdc.approve(streamCreditAddress, liquidityAmount);
  console.log("✅ Approved StreamCredit to spend USDC");
  
  // Add liquidity
  await streamCredit.addLiquidity(liquidityAmount);
  console.log("✅ Added 100,000 USDC liquidity to pool");

  // Summary
  console.log("\n" + "=".repeat(60));
  console.log("📋 DEPLOYMENT SUMMARY");
  console.log("=".repeat(60));
  console.log("Network:         Hardhat Local (chainId: 31337)");
  console.log("MockUSDC:        ", usdcAddress);
  console.log("MockVerifier:    ", verifierAddress);
  console.log("StreamCredit:    ", streamCreditAddress);
  console.log("Initial Liquidity: 100,000 USDC");
  console.log("=".repeat(60));

  // Save addresses to JSON
  const addresses = {
    network: "localhost",
    chainId: 31337,
    mockUSDC: usdcAddress,
    mockVerifier: verifierAddress,
    streamCredit: streamCreditAddress,
    deployer: deployer.address,
    deployedAt: new Date().toISOString()
  };

  const addressesPath = path.join(__dirname, '..', 'deployed-addresses-local.json');
  fs.writeFileSync(addressesPath, JSON.stringify(addresses, null, 2));
  console.log("\n💾 Addresses saved to:", addressesPath);

  // Generate frontend config
  const frontendConfigPath = path.join(__dirname, '..', '..', 'frontend', 'config', 'constants.js');
  const configContent = `// Auto-generated contract addresses
// Last updated: ${new Date().toISOString()}

export const CONTRACTS = {
  streamCredit: '${streamCreditAddress}',
  mockUSDC: '${usdcAddress}',
  mockVerifier: '${verifierAddress}',
};

export const NETWORK = {
  chainId: 31337,
  name: 'Hardhat Local',
  rpcUrl: 'http://localhost:8545',
};

export const SEPOLIA_NETWORK = {
  chainId: 11155111,
  name: 'Sepolia Testnet',
  rpcUrl: 'https://eth-sepolia.g.alchemy.com/v2/your-api-key',
};
`;

  try {
    fs.writeFileSync(frontendConfigPath, configContent);
    console.log("✅ Frontend config updated:", frontendConfigPath);
  } catch (err) {
    console.log("⚠️  Could not update frontend config:", err.message);
  }

  console.log("\n" + "=".repeat(60));
  console.log("✅ DEPLOYMENT COMPLETE!");
  console.log("=".repeat(60));
  console.log("\n💡 Next steps:");
  console.log("1. Start Hardhat node: npx hardhat node");
  console.log("2. Deploy to local network: npx hardhat run scripts/deploy-local.js --network localhost");
  console.log("3. Update MetaMask to connect to localhost:8545");
  console.log("4. Import deployer account to MetaMask");
  console.log("5. Run frontend: cd ../frontend && npm run dev\n");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
