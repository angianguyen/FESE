# 🏗️ StreamCredit Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│                      http://localhost:3000                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND (Next.js)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Landing Page │  │   Console    │  │  Team Page   │         │
│  │              │  │              │  │              │         │
│  │  - Features  │  │ - Scenarios  │  │  - Members   │         │
│  │  - How Works │  │ - Analytics  │  │  - Socials   │         │
│  │  - Roadmap   │  │ - ZK Proof   │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  Components:                                                    │
│  - Web3Context (Wagmi)                                         │
│  - ProtocolConsole                                             │
│  - BenfordChart                                                │
└──────────────┬────────────────────────────┬─────────────────────┘
               │                            │
               │                            │
               ▼                            ▼
┌──────────────────────────┐   ┌───────────────────────────────┐
│   MOCK API SERVER        │   │    BLOCKCHAIN NETWORK         │
│   http://localhost:3001  │   │    (Hardhat/Sepolia)          │
│                          │   │                               │
│  Endpoints:              │   │  Smart Contracts:             │
│  - /api/user/honest      │   │  ┌─────────────────────────┐  │
│  - /api/user/fraud       │   │  │   StreamCredit.sol      │  │
│  - /api/credit/demo      │   │  │  - verifyAndUpdate      │  │
│  - /api/zk/generate      │   │  │  - borrow()             │  │
│  - /api/analyze/benford  │   │  │  - repay()              │  │
│                          │   │  │  - addLiquidity()       │  │
│  Data:                   │   │  └─────────────────────────┘  │
│  - honest-data.csv       │   │                               │
│  - fraud-data.csv        │   │  ┌─────────────────────────┐  │
│  - Benford analysis      │   │  │   MockUSDC.sol          │  │
│                          │   │  │  - faucet()             │  │
│  ZK Proof:               │   │  │  - transfer()           │  │
│  - SnarkJS               │   │  └─────────────────────────┘  │
│  - Groth16               │   │                               │
│                          │   │  ┌─────────────────────────┐  │
│                          │   │  │   MockVerifier.sol      │  │
│                          │   │  │  - verifyProof()        │  │
│                          │   │  │    (always returns true)│  │
│                          │   │  └─────────────────────────┘  │
└──────────────────────────┘   └──────────┬────────────────────┘
                                          │
                                          ▼
                              ┌───────────────────────┐
                              │   MetaMask Wallet     │
                              │                       │
                              │  - Account #0         │
                              │  - Private Key        │
                              │  - Sign Transactions  │
                              └───────────────────────┘
```

## 📊 Data Flow

### Scenario: Honest Merchant

```
1. User clicks "Honest Merchant"
   └→ Frontend → Mock API: GET /api/credit/demo/HONEST

2. Mock API responds:
   └→ {
       revenue: "$50,000",
       benfordScore: 8%,
       creditLimit: "$15,000"
      }

3. User clicks "Generate ZK Proof"
   └→ Frontend → Mock API: POST /api/zk/generate-proof
   └→ Mock API → SnarkJS: Generate Groth16 proof
   └→ Returns: { proof, publicSignals }

4. User clicks "Submit On-Chain"
   └→ Frontend → MetaMask: Request signature
   └→ MetaMask → User: Confirm transaction
   └→ User → MetaMask: Approve
   └→ MetaMask → Blockchain: Send transaction
   └→ Blockchain → StreamCredit.verifyAndUpdateCredit()
   └→ StreamCredit → MockVerifier.verifyProof()
   └→ MockVerifier: Returns true (mock)
   └→ StreamCredit: Update creditLimit[user] = $15,000
   └→ Blockchain → Frontend: Transaction confirmed
   └→ Frontend: Update UI

5. User clicks "Borrow"
   └→ Frontend → MetaMask: Request signature
   └→ MetaMask → Blockchain: streamCredit.borrow(5000)
   └→ StreamCredit: Transfer 5000 USDC to user
   └→ Frontend: Update available credit
```

## 🔐 Security Model

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: Benford's Law Analysis                           │
│  ├─ Client-side validation                                 │
│  ├─ Statistical fraud detection                            │
│  └─ Risk scoring: 0-100%                                   │
│                                                             │
│  Layer 2: Zero-Knowledge Proofs                            │
│  ├─ Privacy-preserving verification                        │
│  ├─ Prove: revenue > threshold AND benford < max          │
│  └─ Without revealing: actual revenue, customer list       │
│                                                             │
│  Layer 3: Smart Contract                                   │
│  ├─ On-chain verification (verifyProof)                    │
│  ├─ Access control (Ownable)                              │
│  ├─ Reentrancy protection (ReentrancyGuard)               │
│  └─ Credit limit enforcement                               │
│                                                             │
│  Layer 4: Wallet Security                                  │
│  ├─ MetaMask transaction signing                           │
│  ├─ User approval required                                 │
│  └─ Private key never exposed                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 💾 State Management

### Frontend State:
- `selectedScenario`: 'honest' | 'fraud' | null
- `revenueData`: string
- `riskStatus`: { level, score, message }
- `creditLimit`: number
- `availableCredit`: number
- `consoleLog`: array of log entries

### Blockchain State:
- `creditLimit[address]`: uint256
- `borrowed[address]`: uint256
- `totalLiquidity`: uint256
- `liquidityProvided[address]`: uint256

## 🎯 Key Components

### ProtocolConsole.jsx
- Main UI component
- Handles user interactions
- Manages state and API calls
- Displays logs and analytics

### Web3Context.js
- Wagmi hooks wrapper
- Wallet connection logic
- Contract interaction functions
- Network management

### StreamCredit.sol
- Core lending logic
- ZK proof verification
- Credit limit management
- Borrow/repay functions

### MockVerifier.sol
- ZK proof verifier (mock)
- Always returns true (testing only)
- Replace with real Verifier.sol in production

## 📈 Transaction Flow

```
User Action → Frontend → MetaMask → Blockchain → Smart Contract
     ↓           ↓           ↓           ↓            ↓
  Button     State      Sign TX    Broadcast     Execute
   Click     Update    Request     to Network    Function
     ↓           ↓           ↓           ↓            ↓
   Logs      Loading    Confirm     Mining      Update State
     ↓           ↓           ↓           ↓            ↓
  Console    Spinner     ✅/❌      Receipt      Event Emit
     ↓           ↓           ↓           ↓            ↓
  Display    Success    Status    Confirmed    Frontend Update
```

---

**Architecture Design Principles:**
- 🔐 Security First
- 🎨 User Experience Focused
- ⚡ Performance Optimized
- 🧩 Modular & Maintainable
- 🚀 Scalable Infrastructure
