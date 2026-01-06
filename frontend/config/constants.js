// Contract addresses (MockVerifier - FOR TESTING ONLY!)
export const CONTRACTS = {
  streamCredit: '0xCF2a831E6D389974992F9b4fc20f9B45fDd95475',
  mockUSDC: '0x25117A7cd454E8C285553f0629696a28bAB3356c',
  groth16Verifier: '0x1e1247d2458FDb5E82CA7e2dd7A30360E7c399BF'  // MockVerifier - always returns true
}

// Mock API endpoint
export const API_BASE_URL = 'http://localhost:3001'

// API Endpoints
export const API_ENDPOINTS = {
  // Data endpoints
  HONEST_DATA: '/api/user/honest',
  FRAUD_DATA: '/api/user/fraud',
  
  // Analysis endpoints
  BENFORD_ANALYZE: '/api/analyze/benford',
  QUICK_CHECK: '/api/analyze/quick-check',
  
  // Credit endpoints
  CREDIT_EVALUATE: '/api/credit/evaluate',
  CREDIT_QUICK_SCORE: '/api/credit/quick-score',
  CREDIT_DEMO: '/api/credit/demo',
  
  // Wallet endpoints
  WALLET_POSITION: '/api/wallet',
  WALLET_BORROW: '/api/wallet/borrow',
  WALLET_REPAY: '/api/wallet/repay',
  WALLET_UPDATE_CREDIT: '/api/wallet/update-credit',
  
  // ZK endpoints
  ZK_GENERATE_PROOF: '/api/zk/generate-proof',
  ZK_VERIFY_PROOF: '/api/zk/verify-proof'
}

// Sepolia chain config
export const SEPOLIA_CHAIN = {
  id: 11155111,
  name: 'Sepolia',
  network: 'sepolia',
  nativeCurrency: {
    decimals: 18,
    name: 'Sepolia ETH',
    symbol: 'ETH',
  },
  rpcUrls: {
    default: {
      http: ['https://rpc2.sepolia.org'],
    },
    public: {
      http: ['https://rpc.sepolia.org'],
    },
  },
  blockExplorers: {
    default: { name: 'Etherscan', url: 'https://sepolia.etherscan.io' },
  },
  testnet: true,
}

// Demo scenarios
export const SCENARIOS = {
  HONEST: {
    name: 'Honest Seller',
    description: 'Shop online với doanh thu tự nhiên, tuân theo Benford\'s Law',
    endpoint: '/api/user/honest',
    expectedResult: 'success',
    icon: '✅'
  },
  FRAUD: {
    name: 'Wash Trader',
    description: 'Tài khoản gian lận với dấu hiệu wash trading',
    endpoint: '/api/user/fraud',
    expectedResult: 'failed',
    icon: '⚠️'
  }
}

// Lending parameters
export const LENDING_PARAMS = {
  CREDIT_RATIO: 30, // 30% of revenue
  REVENUE_THRESHOLD: 1000, // $1k minimum
  FRAUD_THRESHOLD: 20, // 20 Benford score threshold (chi-square divergence)
  INTEREST_RATE: 12, // 12% APR
}
