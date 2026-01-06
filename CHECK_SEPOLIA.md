# 🔍 Verify Contract Addresses trên Sepolia

## Các địa chỉ hiện tại trong code:

### StreamCredit Contract:
**Address:** `0xCF2a831E6D389974992F9b4fc20f9B45fDd95475`

**Check trên Etherscan:**
https://sepolia.etherscan.io/address/0xCF2a831E6D389974992F9b4fc20f9B45fDd95475

---

### MockUSDC Contract:
**Address:** `0x25117A7cd454E8C285553f0629696a28bAB3356c`

**Check trên Etherscan:**
https://sepolia.etherscan.io/address/0x25117A7cd454E8C285553f0629696a28bAB3356c

---

### MockVerifier Contract:
**Address:** `0x1e1247d2458FDb5E82CA7e2dd7A30360E7c399BF`

**Check trên Etherscan:**
https://sepolia.etherscan.io/address/0x1e1247d2458FDb5E82CA7e2dd7A30360E7c399BF

---

## ✅ Nếu các địa chỉ TỒN TẠI trên Etherscan:

→ **Contracts đã được deploy thành công!**
→ Frontend đang dùng đúng addresses
→ Chỉ cần đảm bảo MetaMask connect đúng network

---

## ❌ Nếu các địa chỉ KHÔNG TỒN TẠI:

→ Cần deploy lại contracts lên Sepolia
→ Làm theo hướng dẫn trong `SEPOLIA_QUICKSTART.md`

---

## 🦊 Để connect với Sepolia:

### Bước 1: Switch MetaMask sang Sepolia

1. Mở MetaMask
2. Click network dropdown (ở trên cùng)
3. Chọn "Sepolia test network"
4. Nếu không thấy, add network:
   - Network Name: Sepolia
   - RPC URL: https://rpc.sepolia.org
   - Chain ID: 11155111
   - Currency: ETH
   - Explorer: https://sepolia.etherscan.io

### Bước 2: Đảm bảo có Sepolia ETH

- Nếu chưa có, lấy từ faucet: https://www.alchemy.com/faucets/ethereum-sepolia

### Bước 3: Connect trên Frontend

1. Mở http://localhost:3000
2. Click "Connect Wallet"
3. MetaMask sẽ hiện (phải đang ở Sepolia network)
4. Approve connection

---

## 🔧 Fix nếu không connect được:

### Reset MetaMask:
```
Settings → Advanced → Reset Account
```

### Check Frontend Console (F12):
- Xem có lỗi gì không
- Check network ID có đúng 11155111 không

### Verify Contract Addresses:
- Mở links Etherscan ở trên
- Nếu không tồn tại → deploy lại

---

## 📊 Hiểu về localhost:3000

**localhost:3000 = Frontend Development Server**
- Đây là server local để chạy giao diện
- Frontend connect đến Sepolia testnet thông qua MetaMask
- Transactions sẽ được gửi lên Sepolia (không phải localhost)

**Flow:**
```
Browser (localhost:3000)
    ↓ (UI)
MetaMask 
    ↓ (Sepolia Network)
Smart Contracts on Sepolia
    ↓
Etherscan (View transactions)
```

---

## ✅ Checklist để chạy đúng:

- [ ] Addresses có trên Sepolia Etherscan
- [ ] MetaMask đang ở Sepolia network
- [ ] Có Sepolia ETH trong wallet
- [ ] Frontend running (localhost:3000)
- [ ] Connect wallet thành công
- [ ] Khi submit transaction → MetaMask popup xác nhận

**Nếu tất cả đúng → Bạn đang chạy trên Sepolia testnet! 🎉**

---

## 🚀 Nếu muốn deploy contracts MỚI:

1. Setup `.env` file (xem `SEPOLIA_QUICKSTART.md`)
2. Run: `deploy-sepolia.bat`
3. Copy addresses mới
4. Update `frontend/config/constants.js`
5. Restart frontend
