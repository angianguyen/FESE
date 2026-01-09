# 🚀 Deployment Guide

## Quick Deployment Checklist

- [ ] MongoDB Atlas setup
- [ ] Thirdweb API key
- [ ] Alchemy/Infura RPC URL
- [ ] Deploy smart contracts
- [ ] Update contract addresses
- [ ] Configure environment variables
- [ ] Test on localhost
- [ ] Deploy to production

---

## 1. MongoDB Atlas Setup

### Step 1: Create Account
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up (free tier available)
3. Create new project: "FESEE"

### Step 2: Create Cluster
1. Click "Build a Database"
2. Choose **FREE** tier (M0)
3. Select region closest to users
4. Name cluster: "fesee-cluster"

### Step 3: Setup Access
```
1. Database Access -> Add New Database User
   Username: fesee_admin
   Password: <generate strong password>
   
2. Network Access -> Add IP Address
   IP: 0.0.0.0/0 (for development)
   or your server IP (for production)
```

### Step 4: Get Connection String
```
1. Click "Connect" on your cluster
2. Choose "Connect your application"
3. Copy connection string:
   mongodb+srv://fesee_admin:<password>@fesee-cluster.xxxxx.mongodb.net/fesee?retryWrites=true&w=majority
4. Replace <password> with actual password
5. Add to frontend/.env.local as MONGODB_URI
```

---

## 2. Thirdweb IPFS Setup

### Get Client ID
1. Go to https://thirdweb.com/dashboard
2. Login with wallet
3. Navigate to Settings -> API Keys
4. Create new API key: "FESEE IPFS"
5. Copy **Client ID** (not secret key)
6. Add to `frontend/.env.local`:
   ```
   NEXT_PUBLIC_THIRDWEB_CLIENT_ID=your_client_id_here
   ```

---

## 3. Alchemy RPC Setup

### Get Sepolia RPC URL
1. Go to https://www.alchemy.com/
2. Sign up / Login
3. Create new app:
   - Name: "FESEE Sepolia"
   - Chain: Ethereum
   - Network: Sepolia
4. Copy HTTPS URL
5. Add to `contracts/.env`:
   ```
   SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
   ```

---

## 4. Deploy Smart Contracts

### Prepare Wallet
```bash
# Ensure wallet has Sepolia ETH
# Get from: https://sepoliafaucet.com/
```

### Deploy
```bash
cd contracts

# Compile
npx hardhat compile

# Deploy to Sepolia
npx hardhat run scripts/deploy-mock.js --network sepolia

# Output will show contract addresses:
# MockVerifier: 0x...
# MockUSDC: 0x...
# StreamCredit: 0x...
# CollateralNFT: 0x...
```

### Update Addresses
Copy addresses to `frontend/.env.local`:
```env
NEXT_PUBLIC_STREAM_CREDIT_ADDRESS=0x...
NEXT_PUBLIC_COLLATERAL_NFT_ADDRESS=0x...
NEXT_PUBLIC_MOCK_USDC_ADDRESS=0x...
NEXT_PUBLIC_MOCK_VERIFIER_ADDRESS=0x...
```

---

## 5. Test Locally

```bash
cd frontend
npm run dev
```

Open `http://localhost:3000`:
- ✅ Connect wallet
- ✅ Mint test NFT
- ✅ Generate ZK proof
- ✅ Borrow & repay

---

## 6. Deploy to Vercel (Production)

### Prepare
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login
```

### Deploy
```bash
cd frontend

# Deploy
vercel

# Set environment variables in Vercel dashboard:
vercel env add MONGODB_URI
vercel env add NEXT_PUBLIC_THIRDWEB_CLIENT_ID
vercel env add NEXT_PUBLIC_STREAM_CREDIT_ADDRESS
# ... (all other env vars)

# Production deploy
vercel --prod
```

---

## 7. Post-Deployment Checklist

- [ ] Test wallet connection on production URL
- [ ] Test NFT minting
- [ ] Test ZK proof generation
- [ ] Test borrow/repay flow
- [ ] Check MongoDB data persistence
- [ ] Verify IPFS images load
- [ ] Test on mobile devices

---

## Troubleshooting

### MongoDB Connection Failed
```
Error: MongoServerError: bad auth
Solution: Check username/password in connection string
```

### IPFS Upload Failed
```
Error: Thirdweb Storage not initialized
Solution: Verify NEXT_PUBLIC_THIRDWEB_CLIENT_ID is set
```

### Contract Call Failed
```
Error: Contract not deployed
Solution: Redeploy contracts and update addresses in .env.local
```

---

## Environment Variables Summary

### Frontend (.env.local)
```
MONGODB_URI=mongodb+srv://...
NEXT_PUBLIC_THIRDWEB_CLIENT_ID=...
NEXT_PUBLIC_STREAM_CREDIT_ADDRESS=0x...
NEXT_PUBLIC_COLLATERAL_NFT_ADDRESS=0x...
NEXT_PUBLIC_MOCK_USDC_ADDRESS=0x...
NEXT_PUBLIC_MOCK_VERIFIER_ADDRESS=0x...
NEXT_PUBLIC_API_URL=http://localhost:3000
```

### Contracts (.env)
```
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/...
PRIVATE_KEY=...
ETHERSCAN_API_KEY=...
```

---

**Deployment Complete! 🎉**
