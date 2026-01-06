# StreamCredit Frontend Setup Guide

## 🎨 Giao diện Protocol Console

Frontend này được xây dựng với **Next.js 14** và **Tailwind CSS**, bao gồm:

### Các trang chính:
1. **Landing Page** - Trang giới thiệu dự án
2. **Protocol Console** - Giao diện tương tác với Smart Contract (như trong ảnh demo)
3. **Team Page** - Giới thiệu đội ngũ

### Protocol Console Features:
- ✅ Chọn nguồn dữ liệu (Honest Merchant / Wash Trader)
- ✅ Phân tích Benford's Law score
- ✅ Generate ZK Proof
- ✅ Submit on-chain verification
- ✅ Credit limit tracking
- ✅ Borrow/Repay functionality
- ✅ Real-time console logs

## 📦 Installation

```bash
# Di chuyển vào thư mục frontend
cd frontend

# Cài đặt dependencies
npm install

# Hoặc sử dụng yarn
yarn install
```

## 🔧 Configuration

### 1. Cấu hình Contract Addresses

Mở file `config/constants.js` và cập nhật địa chỉ contract sau khi deploy:

```javascript
export const CONTRACTS = {
  streamCredit: '0xYourStreamCreditAddress',
  mockUSDC: '0xYourMockUSDCAddress',
  mockVerifier: '0xYourVerifierAddress',
}
```

### 2. Cấu hình Mock API URL

Mặc định Mock API chạy tại `http://localhost:3001`. Nếu thay đổi port, cập nhật trong `utils/api.js`.

## 🚀 Running Development Server

```bash
# Chạy development server
npm run dev

# Server sẽ khởi động tại
# http://localhost:3000
```

### Truy cập Protocol Console:
1. Mở browser tại `http://localhost:3000`
2. Click "Launch App" hoặc "Mở Demo App"
3. Connect MetaMask wallet
4. Bắt đầu tương tác!

## 🎮 Sử dụng Protocol Console

### Flow cơ bản:

1. **Chọn Scenario**
   - Click vào "Honest Merchant" hoặc "Wash Trader"
   - Hệ thống sẽ tự động fetch data và phân tích

2. **Phân tích & Tạo Proof**
   - Xem doanh thu phát hiện
   - Xem Benford score (risk status)
   - Click "Generate ZK Proof" để tạo proof
   - Click "Submit On-Chain" để gửi lên contract

3. **Borrow/Repay**
   - Sau khi verify thành công, credit limit được cập nhật
   - Click "Borrow" để vay tiền
   - Click "Repay" để trả nợ

4. **Console Logs**
   - Theo dõi toàn bộ quá trình trong console log phía dưới
   - Các loại log: info (trắng), success (xanh), error (đỏ), warning (vàng), system (cyan)

## 📁 Cấu trúc thư mục

```
frontend/
├── app/
│   ├── demo.jsx           # Main app với landing page & team page
│   ├── page.js            # Entry point
│   ├── layout.js          # Root layout với providers
│   ├── globals.css        # Global styles
│   └── providers.js       # Web3 provider wrapper
├── components/
│   ├── ProtocolConsole.jsx  # Protocol Console component chính
│   ├── BenfordChart.js      # Benford chart visualization
│   └── ZKScripts.js         # ZK proof scripts
├── config/
│   ├── abi.js              # Contract ABIs
│   └── constants.js        # Contract addresses & constants
├── context/
│   └── Web3Context.js      # Web3 context provider
├── utils/
│   ├── api.js              # API utilities
│   └── zkProver.js         # ZK proof generation
└── public/
    └── zk/
        └── verification_key.json
```

## 🎨 Customization

### Thay đổi màu sắc:

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: '#3B82F6',      // Blue
      secondary: '#8B5CF6',    // Purple
      success: '#10B981',      // Green
      danger: '#EF4444',       // Red
      warning: '#F59E0B',      // Amber
    },
  },
}
```

### Thay đổi font:

Edit `globals.css`:

```css
@import url('https://fonts.googleapis.com/css2?family=Your+Font:wght@300;400;500;600;700&display=swap');

body {
  font-family: 'Your Font', sans-serif;
}
```

## 🔗 Integration với Backend

### Mock API Endpoints:

```javascript
// Lấy dữ liệu demo
GET /api/credit/demo/:scenario  // scenario: HONEST | FRAUD

// Lấy raw orders
GET /api/user/honest
GET /api/user/fraud

// Generate ZK Proof
POST /api/zk/generate-proof
{
  "amounts": [100, 200, 300, ...],
  "revenueThreshold": 10000,
  "fraudThreshold": 15
}
```

## 🐛 Troubleshooting

### MetaMask không connect được:
- Đảm bảo đang dùng Sepolia Testnet
- Xóa cache MetaMask: Settings > Advanced > Reset Account

### Console logs không hiển thị:
- Check console trong DevTools (F12) xem có lỗi không
- Đảm bảo state `consoleLog` đang được update

### Contract interaction fail:
- Verify contract addresses trong `config/constants.js`
- Đảm bảo đã approve USDC trước khi borrow
- Check gas limit và balance

## 📱 Responsive Design

Giao diện đã được optimize cho:
- 📱 Mobile (< 768px)
- 💻 Tablet (768px - 1024px)
- 🖥️ Desktop (> 1024px)

## 🚢 Production Build

```bash
# Build for production
npm run build

# Start production server
npm start

# Export static site (optional)
npm run build && npm run export
```

## 🌐 Deployment

### Vercel (Recommended):

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Netlify:

```bash
# Build command
npm run build

# Publish directory
.next
```

## 📊 Performance Tips

1. **Images**: Sử dụng Next.js Image component
2. **Fonts**: Preload critical fonts
3. **Code Splitting**: Lazy load heavy components
4. **Caching**: Configure browser caching headers

## 🔐 Security Notes

- ⚠️ **NEVER** commit private keys
- ⚠️ Environment variables phải bắt đầu với `NEXT_PUBLIC_` để exposed to browser
- ⚠️ Validate tất cả inputs từ users
- ⚠️ Sử dụng HTTPS trong production

## 📖 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Wagmi Documentation](https://wagmi.sh)
- [Ethers.js Docs](https://docs.ethers.org)

## 💬 Support

Nếu gặp vấn đề, tạo issue tại GitHub repository hoặc liên hệ team.

---

**Built with ❤️ by StreamCredit Team**
