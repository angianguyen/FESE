# 🔐 SETUP SEPOLIA TESTNET - Chi tiết từng bước

## 📋 THÔNG TIN SEPOLIA NETWORK:

### Chain ID: 
```
11155111
(hex: 0xaa36a7)
```

### RPC URLs (Public - Free):
```
https://rpc.sepolia.org
https://rpc2.sepolia.org
https://ethereum-sepolia-rpc.publicnode.com
```

### Block Explorer:
```
https://sepolia.etherscan.io
```

### Native Currency:
```
Sepolia ETH (SepoliaETH)
Symbol: ETH
Decimals: 18
```

---

## 📁 CÁC FILE SETUP:

### 1️⃣ `contracts/hardhat.config.js` - Cấu hình Hardhat

```javascript
networks: {
  sepolia: {
    url: process.env.SEPOLIA_RPC_URL || "https://eth-sepolia.g.alchemy.com/v2/your-api-key",
    accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    chainId: 11155111  // ← Sepolia Chain ID
  }
}
```

**Giải thích:**
- `url`: RPC endpoint để connect đến Sepolia
- `accounts`: Array chứa private keys (từ .env file)
- `chainId`: ID của Sepolia network (11155111)

---

### 2️⃣ `contracts/.env.example` - Template cho Environment Variables

**File này là TEMPLATE, cần tạo file `.env` thật:**

```bash
cd contracts
copy .env.example .env
```

**Sau đó điền thông tin vào file `.env`:**

```env
# 1. RPC URL (Lấy từ Alchemy hoặc Infura)
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY

# 2. Private Key (Lấy từ MetaMask)
PRIVATE_KEY=your_64_character_private_key

# 3. Etherscan API Key (Optional - để verify contracts)
ETHERSCAN_API_KEY=your_etherscan_key
```

---

### 3️⃣ `frontend/config/constants.js` - Frontend Config

```javascript
export const SEPOLIA_CHAIN = {
  id: 11155111,          // ← Chain ID
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
    }
  },
  blockExplorers: {
    default: { 
      name: 'Etherscan', 
      url: 'https://sepolia.etherscan.io' 
    },
  },
  testnet: true,
}
```

---

## 🔑 CÁCH LẤY PRIVATE KEY:

### ⚠️ CẢNH BÁO:
- **KHÔNG BAO GIỜ** chia sẻ private key
- **CHỈ DÙNG** wallet test, không dùng wallet chính
- **KHÔNG COMMIT** file .env vào Git

### Bước 1: Tạo/Chọn Test Wallet

**Option A: Tạo wallet mới (Khuyến nghị)**
1. Mở MetaMask
2. Click avatar → "Create Account" hoặc "Add account"
3. Đặt tên: "Sepolia Test"
4. Wallet mới được tạo

**Option B: Dùng wallet có sẵn**
- Đảm bảo wallet này CHỈ dùng cho testnet
- Không chứa tiền thật

### Bước 2: Export Private Key

1. **Mở MetaMask**
2. **Click vào account bạn muốn dùng**
3. **Click ⋮ (menu 3 chấm)** → "Account details"
4. **Click "Show private key"**
5. **Nhập password MetaMask**
6. **Click "Confirm"**
7. **Copy private key** (chuỗi 64 ký tự hex)

**Private key sẽ có dạng:**
```
abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567890abcdef12
```

### Bước 3: Lưu vào .env

**Tạo file `contracts/.env`:**

```env
PRIVATE_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567890abcdef12
```

**LƯU Ý:**
- KHÔNG thêm "0x" ở đầu
- Chỉ copy 64 ký tự hex
- KHÔNG có dấu space hoặc newline

---

## 🌐 CÁCH LẤY RPC URL:

### Option 1: Alchemy (Khuyến nghị)

**Ưu điểm:**
- ✅ Free tier rộng rãi
- ✅ Reliable và nhanh
- ✅ Dashboard để monitor

**Các bước:**

1. **Truy cập:** https://www.alchemy.com/
2. **Sign up/Login** (dùng email hoặc GitHub)
3. **Click "Create new app"**
4. **Điền thông tin:**
   - Name: `StreamCredit`
   - Chain: `Ethereum`
   - Network: `Sepolia`
5. **Click "Create app"**
6. **Vào app vừa tạo** → Click "View key"
7. **Copy "HTTPS" URL**

**URL có dạng:**
```
https://eth-sepolia.g.alchemy.com/v2/abc123def456ghi789
```

8. **Paste vào .env:**
```env
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/abc123def456ghi789
```

---

### Option 2: Infura

1. **Truy cập:** https://infura.io/
2. **Sign up/Login**
3. **Create new project**
4. **Chọn:** Ethereum → Sepolia
5. **Copy HTTPS endpoint**

**URL có dạng:**
```
https://sepolia.infura.io/v3/YOUR_PROJECT_ID
```

---

### Option 3: Public RPC (Không cần đăng ký)

**KHÔNG khuyến nghị cho production vì:**
- Rate limits thấp
- Có thể bị down
- Chậm hơn

**Nhưng có thể dùng cho test:**

```env
SEPOLIA_RPC_URL=https://rpc2.sepolia.org
```

hoặc

```env
SEPOLIA_RPC_URL=https://ethereum-sepolia-rpc.publicnode.com
```

---

## 🔐 CÁCH LẤY ETHERSCAN API KEY (Optional):

**Dùng để verify contracts trên Etherscan**

1. **Truy cập:** https://etherscan.io/
2. **Sign up/Login**
3. **My Profile** → **API Keys**
4. **Click "Add"** → Đặt tên: "StreamCredit"
5. **Copy API key**

**Paste vào .env:**
```env
ETHERSCAN_API_KEY=ABC123XYZ456
```

---

## 📝 FILE .env HOÀN CHỈNH:

**Tạo file `contracts/.env` với nội dung:**

```env
# Alchemy RPC URL
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/your_alchemy_api_key_here

# MetaMask Private Key (64 ký tự, KHÔNG có 0x)
PRIVATE_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567890abcdef12

# Etherscan API Key (Optional)
ETHERSCAN_API_KEY=ABC123XYZ789
```

---

## ✅ VERIFY SETUP:

### Test 1: Check Balance

```bash
cd contracts
npx hardhat run scripts/check-balance.js --network sepolia
```

**Nếu thành công, sẽ hiện:**
```
Address: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0
Balance: 0.5 ETH
Network: sepolia
Chain ID: 11155111
✅ Balance sufficient for deployment
```

### Test 2: Get Network Info

```bash
npx hardhat console --network sepolia
```

Trong console:
```javascript
await ethers.provider.getNetwork()
// Sẽ hiện: { name: 'sepolia', chainId: 11155111 }
```

---

## 🚀 SAU KHI SETUP XONG:

### Deploy Contracts:

```bash
cd contracts

# Compile
npx hardhat compile

# Deploy
npx hardhat run scripts/deploy-mock.js --network sepolia
```

### Update Frontend:

Copy addresses từ `deployed-addresses-mock.json` vào `frontend/config/constants.js`

### Test:

1. MetaMask → Switch sang Sepolia
2. Connect wallet
3. Test transactions!

---

## 🐛 TROUBLESHOOTING:

### "Invalid API key"
→ Check SEPOLIA_RPC_URL có đúng không

### "Insufficient funds"
→ Lấy Sepolia ETH từ faucet: https://www.alchemy.com/faucets/ethereum-sepolia

### "Network not found"
→ Verify chainId trong hardhat.config.js là 11155111

### "Invalid private key"
→ Check private key:
- Đúng 64 ký tự
- Không có 0x ở đầu
- Không có space/newline

---

## 📊 SUMMARY:

| Item | Value | Where to Get |
|------|-------|--------------|
| Chain ID | 11155111 | Built-in constant |
| RPC URL | https://eth-sepolia.g.alchemy.com/v2/... | Alchemy.com |
| Private Key | 64 hex chars | MetaMask Export |
| Etherscan Key | API key | Etherscan.io |
| Test ETH | Free | Faucet |

---

**Sau khi có đủ 3 thông tin trên, bạn có thể deploy lên Sepolia! 🚀**
