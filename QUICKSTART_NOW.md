# ⚡ QUICK START - StreamCredit

## Chạy ngay trong 3 bước:

### 1️⃣ Cài đặt Dependencies

Mở PowerShell/CMD tại thư mục dự án:

```bash
# Contracts
cd contracts
npm install

# Mock API (đã cài rồi)
cd ..\mock-api
npm install

# Frontend (đã cài rồi)
cd ..\frontend
npm install
```

### 2️⃣ Deploy Contracts Local

**Mở Terminal 1:**
```bash
cd contracts
npx hardhat node
```
→ Giữ terminal này chạy!
→ Copy private key của Account #0 (để import vào MetaMask)

**Mở Terminal 2:**
```bash
cd contracts
npx hardhat run scripts/deploy-local.js --network localhost
```
→ Xem contract addresses được in ra

### 3️⃣ Chạy Frontend

Mock API đã chạy rồi. Chỉ cần start frontend:

**Mở Terminal 3:**
```bash
cd frontend
npm run dev
```

Mở browser: http://localhost:3000

---

## 🦊 Setup MetaMask (1 lần)

1. **Add Hardhat Network:**
   - Network Name: `Hardhat Local`
   - RPC URL: `http://localhost:8545`
   - Chain ID: `31337`
   - Currency: `ETH`

2. **Import Test Account:**
   - Copy private key từ Terminal 1 (Hardhat node)
   - MetaMask → Import Account → Paste private key

3. **Connect:**
   - Trên website click "Connect Wallet"
   - Chọn MetaMask
   - Approve

---

## ✅ Done!

Giờ bạn có thể:
- ✨ Chọn scenario (Honest/Fraud)
- 🔐 Generate ZK Proof
- 📝 Submit on-chain (cần confirm MetaMask)
- 💰 Borrow/Repay

---

## 🔄 Nếu muốn reset/restart:

**Stop tất cả (Ctrl+C trong mỗi terminal)**

**Restart theo thứ tự:**
1. Hardhat node (Terminal 1)
2. Deploy contracts (Terminal 2)
3. Frontend (Terminal 3)

---

## 📱 Services Running:

- Hardhat: http://localhost:8545
- Mock API: http://localhost:3001 ✅
- Frontend: http://localhost:3000

---

**Gặp lỗi? Xem SETUP_GUIDE.md để troubleshoot**
