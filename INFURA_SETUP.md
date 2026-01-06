# 🌐 Lấy Sepolia RPC URL từ Infura

## Bước 1: Đăng ký/Đăng nhập Infura

1. Truy cập: **https://infura.io/**
2. Click **"Sign Up"** (hoặc "Login" nếu đã có tài khoản)
3. Đăng ký với email hoặc GitHub

---

## Bước 2: Tạo Project Mới

1. Sau khi login, click **"Create New API Key"** hoặc **"Create New Project"**
2. Điền thông tin:
   - **Project Name:** `StreamCredit`
   - **Network:** Chọn **Web3 API (Formerly Ethereum)**
3. Click **"Create"**

---

## Bước 3: Lấy Sepolia Endpoint

### Cách 1: Từ Dashboard

1. Vào project **"StreamCredit"** vừa tạo
2. Trong phần **"API Keys"**, tìm **"Project ID"**
3. Scroll xuống phần **"Endpoints"**
4. Chọn network **"Sepolia"**
5. Copy URL **HTTPS** endpoint

**URL có dạng:**
```
https://sepolia.infura.io/v3/abc123def456ghi789jkl012mno345pq
```

### Cách 2: Tự tạo URL

**Format:**
```
https://sepolia.infura.io/v3/YOUR_PROJECT_ID
```

**Ví dụ:**
- Project ID: `abc123def456ghi789jkl012mno345pq`
- RPC URL: `https://sepolia.infura.io/v3/abc123def456ghi789jkl012mno345pq`

---

## Bước 4: Tạo file .env

**Trong thư mục `contracts`, tạo file `.env`:**

### Windows:
```bash
cd E:\fese_main\contracts
copy .env.example .env
notepad .env
```

### Hoặc tạo trực tiếp:
```bash
cd E:\fese_main\contracts
echo. > .env
```

---

## Bước 5: Điền thông tin vào .env

**Nội dung file `contracts/.env`:**

```env
# Infura Sepolia RPC URL
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID_HERE

# Private Key từ MetaMask (64 ký tự, KHÔNG có 0x)
PRIVATE_KEY=your_private_key_here

# Etherscan API Key (Optional)
ETHERSCAN_API_KEY=your_etherscan_key_here
```

**Ví dụ thực tế:**
```env
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/abc123def456ghi789jkl012mno345pq
PRIVATE_KEY=202fab1eea7f2cdd10b8b0aab091804c1fbd9c622f31dc7d8cced7de0aff474b
ETHERSCAN_API_KEY=ABC123XYZ789
```

---

## ✅ Verify Setup

### Test connection:

```bash
cd contracts
npx hardhat run scripts/check-balance.js --network sepolia
```

**Nếu thành công, sẽ hiện:**
```
Address: 0x...
Balance: 0.5 ETH
Network: sepolia
Chain ID: 11155111
✅ Balance sufficient for deployment
```

---

## 🔍 So sánh Infura vs Alchemy

| Feature | Infura | Alchemy |
|---------|--------|---------|
| Free Tier | 100k requests/day | 300M compute units/month |
| Setup | Đơn giản hơn | Nhiều features |
| Dashboard | Basic | Advanced analytics |
| Speed | Nhanh | Rất nhanh |
| URL Format | `sepolia.infura.io/v3/ID` | `eth-sepolia.g.alchemy.com/v2/KEY` |

**Khuyến nghị:**
- **Infura**: Đơn giản, dễ setup, đủ cho hầu hết use cases
- **Alchemy**: Advanced features, dashboard tốt hơn

---

## 📸 Screenshots Hướng dẫn

### 1. Infura Dashboard
```
Dashboard → Create New API Key
    ↓
Chọn Web3 API (Ethereum)
    ↓
Đặt tên: StreamCredit
    ↓
Create
```

### 2. Lấy Endpoint
```
Project → API Keys
    ↓
Scroll to "Endpoints"
    ↓
Select "Sepolia"
    ↓
Copy HTTPS URL
```

---

## 🐛 Troubleshooting

### "Invalid project ID"
→ Check URL format: `https://sepolia.infura.io/v3/YOUR_ID`

### "Rate limit exceeded"
→ Free tier: 100k requests/day. Nếu vượt, upgrade plan.

### "Network not supported"
→ Đảm bảo chọn đúng network "Sepolia" trong Infura dashboard

---

## 🔐 Bảo mật

⚠️ **QUAN TRỌNG:**

1. **File .env KHÔNG được commit vào Git**
   - Đã có trong `.gitignore`
   - Kiểm tra: `git status` không thấy `.env`

2. **Chỉ chia sẻ .env.example**
   - Template không chứa thông tin thật
   - Safe để commit

3. **Infura Project ID**
   - Coi như API key
   - Không chia sẻ công khai
   - Rate limit áp dụng

---

## 🚀 Next Steps

Sau khi có RPC URL:

```bash
# 1. Deploy contracts
cd contracts
npx hardhat run scripts/deploy-mock.js --network sepolia

# 2. Verify trên Etherscan
npx hardhat verify --network sepolia CONTRACT_ADDRESS

# 3. Update frontend config
# Copy addresses vào frontend/config/constants.js

# 4. Test!
cd ../frontend
npm run dev
```

---

## 🔗 Links

- **Infura Dashboard:** https://infura.io/dashboard
- **Infura Docs:** https://docs.infura.io/
- **Sepolia Faucet:** https://www.infura.io/faucet/sepolia
- **Infura Status:** https://status.infura.io/

---

**Xong! Bây giờ bạn có thể deploy lên Sepolia với Infura! 🎉**
