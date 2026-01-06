# ✅ GIẢI THÍCH: Làm sao để chạy trên Sepolia?

## 🎯 TÓM TẮT:

**Frontend (localhost:3000) ≠ Blockchain Network**

- `localhost:3000` = **Giao diện website** (chạy local)
- `Sepolia` = **Blockchain network** (nơi chạy smart contracts)

---

## 📍 CÁC ĐỊA CHỈ CONTRACT HIỆN TẠI:

Từ file `deployed-addresses-mock.json`:

```
StreamCredit:  0xCF2a831E6D389974992F9b4fc20f9B45fDd95475
MockUSDC:      0x25117A7cd454E8C285553f0629696a28bAB3356c
MockVerifier:  0x1e1247d2458FDb5E82CA7e2dd7A30360E7c399BF
```

**Kiểm tra trên Etherscan:**
- StreamCredit: https://sepolia.etherscan.io/address/0xCF2a831E6D389974992F9b4fc20f9B45fDd95475
- MockUSDC: https://sepolia.etherscan.io/address/0x25117A7cd454E8C285553f0629696a28bAB3356c
- MockVerifier: https://sepolia.etherscan.io/address/0x1e1247d2458FDb5E82CA7e2dd7A30360E7c399BF

---

## ❓ CÂU HỎI: Tại sao localhost:3000?

### Trả lời:

**localhost:3000 = Frontend Development Server**
- Đây là server web local để hiển thị giao diện
- Code Next.js chạy trên máy bạn
- CHỈ phục vụ HTML/CSS/JavaScript

**Sepolia = Blockchain Network**
- Smart contracts chạy ở đây
- Transactions được ghi nhận trên blockchain
- Public, ai cũng có thể verify

---

## 🔗 CÁCH HOẠT ĐỘNG:

```
┌─────────────────────┐
│  Browser            │
│  localhost:3000     │  ← Giao diện (local)
└──────────┬──────────┘
           │
           ↓ Connect wallet
┌─────────────────────┐
│  MetaMask           │  ← Quản lý private key
└──────────┬──────────┘
           │
           ↓ Send transaction
┌─────────────────────┐
│  Sepolia Network    │  ← Smart contracts ở đây
│  Chain ID: 11155111 │
└─────────────────────┘
           │
           ↓ View on
┌─────────────────────┐
│  Etherscan          │  ← Xem transactions
│  sepolia.etherscan  │
└─────────────────────┘
```

---

## ✅ CÁCH CHẠY ĐÚNG:

### Bước 1: Mở Frontend
```bash
cd frontend
npm run dev
# → http://localhost:3000
```

### Bước 2: Setup MetaMask

1. **Mở MetaMask**
2. **Switch network** → Chọn "Sepolia test network"
3. **Đảm bảo có Sepolia ETH** (nếu chưa có, lấy từ faucet)

### Bước 3: Connect Wallet

1. Trên website (localhost:3000)
2. Click **"Connect Wallet"**
3. MetaMask popup → Click **"Connect"**
4. Approve connection

### Bước 4: Test

1. Click **"Launch App"**
2. Chọn scenario (Honest/Fraud)
3. Click **"Generate ZK Proof"**
4. Click **"Submit On-Chain"**
5. MetaMask popup → Confirm transaction
6. ✅ Transaction sẽ được gửi lên **Sepolia**!

---

## 🔍 VERIFY TRANSACTION:

Sau khi submit:
1. Copy transaction hash từ MetaMask hoặc console log
2. Mở: https://sepolia.etherscan.io/tx/YOUR_TX_HASH
3. Xem chi tiết transaction trên blockchain

---

## 💡 HIỂU RÕ HƠN:

### Frontend (localhost:3000):
- ✅ Chạy local trên máy bạn
- ✅ Chỉ là giao diện UI
- ❌ KHÔNG chứa smart contracts
- ❌ KHÔNG lưu trữ blockchain data

### Smart Contracts (Sepolia):
- ✅ Deploy trên Sepolia testnet
- ✅ Addresses cố định (không đổi)
- ✅ Public, ai cũng truy cập được
- ✅ Transactions ghi vĩnh viễn

---

## 🆚 SO SÁNH:

### Nếu dùng Hardhat Local:
```
Frontend: localhost:3000
Blockchain: localhost:8545 (Hardhat node)
Addresses: Thay đổi mỗi lần restart
Etherscan: Không có
```

### Nếu dùng Sepolia (HIỆN TẠI):
```
Frontend: localhost:3000
Blockchain: Sepolia testnet (public)
Addresses: Cố định (0xCF2a831E6D38...)
Etherscan: ✅ Có (sepolia.etherscan.io)
```

---

## ✅ CHECKLIST ĐỂ CHẠY ĐÚNG:

- [ ] Frontend chạy tại localhost:3000
- [ ] MetaMask đã cài đặt
- [ ] MetaMask đang ở Sepolia network (Chain ID: 11155111)
- [ ] Có Sepolia ETH trong wallet
- [ ] Connect wallet thành công
- [ ] Khi submit → MetaMask popup hiện ra

**Nếu tất cả đúng → Bạn đang chạy trên Sepolia! 🎉**

---

## 🚀 DEMO CHO INVESTOR:

### Ưu điểm:
- ✅ Share link Etherscan để verify transactions
- ✅ Không cần chạy local blockchain
- ✅ Mọi người đều có thể test
- ✅ Giống production (mainnet)

### Ví dụ demo:
```
Investor: "Cho tôi xem contract address?"
You: "0xCF2a831E6D389974992F9b4fc20f9B45fDd95475"
      "Verify tại: sepolia.etherscan.io"

Investor: "Tôi có thể test không?"
You: "Có! Chỉ cần:
      1. Cài MetaMask
      2. Switch sang Sepolia
      3. Lấy test ETH từ faucet
      4. Vào localhost:3000 (hoặc deployed URL)
      5. Connect & test!"
```

---

## 🎯 KẾT LUẬN:

**localhost:3000 là ĐÚNG!**
- Frontend development server
- Connect đến Sepolia thông qua MetaMask
- Smart contracts chạy trên Sepolia (public)
- Transactions có thể verify trên Etherscan

**Không cần deploy frontend lên Sepolia!**
- Sepolia chỉ chứa smart contracts
- Frontend có thể chạy local hoặc deploy lên Vercel/Netlify

---

## 📱 NEXT STEPS (Optional):

### Deploy Frontend lên Public:

1. **Deploy lên Vercel:**
   ```bash
   # Push code lên GitHub
   git push origin main
   
   # Import vào Vercel
   # → Auto deploy
   # → Get public URL: streamcredit.vercel.app
   ```

2. **Users có thể truy cập:**
   - Public URL: https://streamcredit.vercel.app
   - Connect MetaMask → Sepolia
   - Test như bình thường

**Lúc đó:**
- Frontend: streamcredit.vercel.app (public)
- Smart Contracts: Sepolia (public)
- ✅ Hoàn toàn public, không cần localhost!

---

**TÓM LẠI: Bạn ĐANG chạy đúng! Chỉ cần MetaMask connect Sepolia là OK! 🚀**
