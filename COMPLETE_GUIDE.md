# 🚀 StreamCredit - Hướng dẫn Chạy Đầy đủ

## Tổng quan

Hệ thống StreamCredit bao gồm 3 phần chính:
1. **Frontend** (Next.js) - Port 3000
2. **Mock API** (Express) - Port 3001  
3. **Smart Contracts** (Hardhat) - Sepolia Testnet

## ⚡ Chạy Nhanh (Quick Start)

### Cách 1: Sử dụng Script Tự động

```bash
# Windows
start-all.bat

# Linux/Mac
chmod +x start-all.sh
./start-all.sh
```

Script sẽ tự động:
- ✅ Install dependencies cho tất cả modules
- ✅ Start Mock API server (port 3001)
- ✅ Start Frontend (port 3000)
- ✅ Mở browser tại http://localhost:3000

### Cách 2: Chạy Thủ công

#### Bước 1: Start Mock API

```bash
cd mock-api
npm install
npm start
```

Server chạy tại: `http://localhost:3001`

#### Bước 2: Start Frontend

Mở terminal mới:

```bash
cd frontend
npm install
npm run dev
```

Frontend chạy tại: `http://localhost:3000`

## 🎮 Demo Flow

### 1. Mở Ứng dụng

- Truy cập: `http://localhost:3000`
- Click "Launch App" hoặc "Mở Demo App"

### 2. Connect Wallet

- Click "Connect Wallet" ở góc phải
- Chọn MetaMask
- Approve connection
- **Lưu ý**: Chuyển MetaMask sang **Sepolia Testnet**

### 3. Scenario 1: Honest Merchant ✅

a. **Chọn Honest Merchant**
   - Click vào card "Honest Merchant" (icon xanh)
   - Hệ thống fetch 100 đơn hàng từ Mock API
   
b. **Phân tích Tự động**
   - Doanh thu: ~$50,000
   - Benford Score: ~8% (thấp = tốt)
   - Status: LOW RISK
   
c. **Generate ZK Proof**
   - Click "Generate ZK Proof"
   - Chờ 2-3 giây để tạo proof
   - Console log hiển thị: "✓ ZK Proof generated successfully"

d. **Submit On-Chain** (Cần wallet connect)
   - Click "Submit On-Chain"
   - Confirm transaction trong MetaMask
   - Chờ transaction được confirm
   - Credit Limit cập nhật: $0 → $15,000

e. **Borrow Funds**
   - Credit limit hiện tại: $15,000
   - Available: $15,000
   - Click "Borrow" để vay $5,000
   - Confirm trong MetaMask
   - Available giảm xuống: $10,000

f. **Repay**
   - Click "Repay"
   - Confirm transaction
   - Available tăng lên: $15,000

### 4. Scenario 2: Wash Trader ❌

a. **Chọn Wash Trader**
   - Click vào card "Wash Trader" (icon đỏ)
   - Hệ thống fetch dữ liệu wash trading

b. **Phân tích Tự động**
   - Doanh thu: ~$100,000
   - Benford Score: ~45% (cao = nguy hiểm)
   - Status: HIGH RISK

c. **Cảnh báo Gian lận**
   - Hệ thống hiển thị cảnh báo: "Điều khiển thao túng volume"
   - Console log: "⚠ Benford Score = 45% (High risk - Wash Trading detected)"

d. **Submit bị từ chối**
   - Button "Submit On-Chain" bị disable
   - Không thể submit do risk cao
   - Console log: "✗ Transaction rejected: High fraud risk detected"

## 🔍 Console Logs Giải thích

### Log Colors:
- **Trắng/Gray** (info): Thông tin chung
- **Xanh lá** (success): Thao tác thành công
- **Đỏ** (error): Lỗi hoặc từ chối
- **Vàng** (warning): Cảnh báo
- **Cyan** (system): Thông tin hệ thống

### Log Examples:

```
[11:06:04 AM] Console initialized. Waiting for user input...
[11:06:15 AM] Selected scenario: honest
[11:06:15 AM] Fetching order data from Mock API...
[11:06:17 AM] ✓ Data analysis complete: Revenue = $50,000
[11:06:17 AM] ✓ Benford Score = 8% (Low risk)
[11:06:25 AM] Generating Zero-Knowledge Proof...
[11:06:25 AM] Using Groth16 proving system (SnarkJS)
[11:06:27 AM] ✓ ZK Proof generated successfully
[11:06:27 AM] Proof hash: 0x7f3a...c8d2
[11:06:35 AM] Submitting verification to Smart Contract...
[11:06:35 AM] Contract: StreamCredit.sol (Sepolia)
[11:06:38 AM] ✓ Transaction confirmed!
[11:06:38 AM] ✓ Credit Limit updated: $5,000 → $15,000
[11:06:38 AM] Gas used: 0.0024 ETH
```

## 📊 Giao diện Components

### Main Layout:

```
┌─────────────────────────────────────────────────────────┐
│ Header: StreamCredit Logo | Connect Wallet             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Protocol Console                          v0.1.0 beta │
│  Tương tác trực tiếp với Smart Contract & ZK Verifier  │
│                                                         │
├──────────────────────────────┬──────────────────────────┤
│                              │   YOUR POSITION          │
│  1️⃣ Chọn nguồn dữ liệu        │                          │
│                              │   Credit Limit: $15,000  │
│  [Honest Merchant]           │   Available: $10,000     │
│  [Wash Trader]               │                          │
│                              │   ████████░░░░  76%      │
│  2️⃣ Phân tích & Tạo Proof     │                          │
│                              │   [Borrow] [Repay]       │
│  Doanh thu: $50,000          │                          │
│  Rủi ro: 8%                  │                          │
│                              │                          │
│  [Generate ZK Proof]         │                          │
│  [Submit On-Chain]           │                          │
│                              │                          │
├──────────────────────────────┴──────────────────────────┤
│  🟢🟡🔴 console.log                                       │
│  ─────────────────────────────────────────────────────  │
│  [11:06:04 AM] Console initialized...                   │
│  [11:06:15 AM] Selected scenario: honest                │
│  [11:06:17 AM] ✓ Data analysis complete                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🎨 UI Features

### Cards với Hover Effects:
- Glass morphism design
- Smooth transitions
- Border glow khi hover
- Shadow effects

### Progress Bar:
- Dynamic width dựa trên available credit
- Gradient color (cyan to blue)
- Smooth animations

### Buttons:
- Primary: Gradient cyan-blue
- Secondary: Slate with border
- Disabled: Opacity 50%
- Loading states với spinner

### Console Log:
- Monospace font (JetBrains Mono)
- Auto-scroll to bottom
- Color-coded messages
- Timestamp cho mỗi entry
- macOS-style window controls

## 🔧 Troubleshooting

### Mock API không start được:

```bash
cd mock-api
rm -rf node_modules package-lock.json
npm install
npm start
```

### Frontend không build được:

```bash
cd frontend
rm -rf node_modules .next package-lock.json
npm install
npm run dev
```

### MetaMask không connect:

1. Mở MetaMask
2. Settings > Advanced > Reset Account
3. Refresh trang web
4. Thử connect lại

### Không thấy credit limit update:

1. Check MetaMask đang ở Sepolia Testnet
2. Verify contract addresses trong `frontend/config/constants.js`
3. Check console (F12) xem có lỗi không
4. Thử reload lại trang

### Transaction fail:

**Nguyên nhân thường gặp:**
- Không đủ Sepolia ETH → Get từ faucet
- Wrong network → Switch sang Sepolia
- Contract address sai → Verify trong constants.js
- Nonce stuck → Reset account trong MetaMask

## 📱 Keyboard Shortcuts

- `Ctrl + K`: Open console search (khi có nhiều logs)
- `Ctrl + R`: Refresh page
- `F12`: Open DevTools
- `Esc`: Close modals

## 🌐 URLs Quan trọng

- Frontend: `http://localhost:3000`
- Mock API: `http://localhost:3001`
- API Health: `http://localhost:3001/health`
- Sepolia Faucet: `https://sepoliafaucet.com`
- Sepolia Explorer: `https://sepolia.etherscan.io`

## 📖 Next Steps

1. ✅ Chạy demo local
2. 📝 Deploy contracts lên Sepolia
3. 🔗 Update contract addresses
4. 🚀 Deploy frontend lên Vercel
5. 🎉 Share demo link!

## 💡 Pro Tips

1. **Testing**: Tạo nhiều tài khoản MetaMask để test các kịch bản khác nhau
2. **Development**: Sử dụng React DevTools để debug state
3. **Performance**: Check Network tab xem API response time
4. **Debugging**: Luôn mở Console (F12) để xem detailed logs

## 🤝 Support

Gặp vấn đề? Check:
1. Console logs trong browser (F12)
2. Terminal logs của Mock API
3. Terminal logs của Frontend
4. MetaMask transaction history

---

**Happy Hacking! 🚀**
