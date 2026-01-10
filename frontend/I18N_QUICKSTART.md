# 🌍 Hướng dẫn Sử dụng i18n Nhanh - FESEE

## ✅ Đã Hoàn thành

### 1. **Cài đặt Packages**
```bash
npm install react-i18next i18next i18next-browser-languagedetector
```

### 2. **Cấu trúc Files**
```
frontend/
├── lib/i18n.js              # ⚙️ Cấu hình i18n
├── locales/
│   ├── en.json              # 🇺🇸 Tiếng Anh
│   ├── vi.json              # 🇻🇳 Tiếng Việt  
│   └── ko.json              # 🇰🇷 Tiếng Hàn
├── components/
│   └── LanguageSwitcher.js  # 🔄 Component chuyển đổi ngôn ngữ
└── app/
    ├── providers.js         # 🎁 I18nextProvider wrapper
    └── demo.jsx             # 📱 Đã tích hợp useTranslation
```

---

## 🚀 Cách Sử dụng

### Bước 1: Import Hook
```jsx
import { useTranslation } from 'react-i18next';
```

### Bước 2: Sử dụng trong Component
```jsx
function MyComponent() {
  const { t } = useTranslation();

  return (
    <div>
      <h1>{t('app.title')}</h1>
      <button>{t('wallet.connect')}</button>
    </div>
  );
}
```

### Bước 3: Translation Keys có sẵn
```javascript
// Ví dụ các keys phổ biến:
t('nav.overview')              // "Overview" / "Tổng quan" / "개요"
t('wallet.connect')            // "Connect Wallet" / "Kết nối Ví" / "지갑 연결"
t('creditCheck.title')         // "ZK Credit Verification"
t('borrow.submitBorrow')       // "Submit Borrow Request"
t('collateral.mint')           // "Mint New Collateral"
t('collateral.types.realEstate') // "Real Estate" / "Bất động sản" / "부동산"
t('common.loading')            // "Loading..." / "Đang tải..." / "로딩 중..."
t('errors.walletNotConnected') // Error messages
```

---

## 🎨 LanguageSwitcher Component

Component này đã được tích hợp vào Navbar! Tính năng:

✅ Dropdown menu với cờ quốc gia  
✅ Lưu vào localStorage tự động  
✅ Responsive design  
✅ Click outside để đóng  
✅ Hiển thị ngôn ngữ hiện tại

### Sử dụng:
```jsx
import LanguageSwitcher from '../components/LanguageSwitcher';

<nav>
  <LanguageSwitcher />
</nav>
```

---

## 📝 Thêm Translations Mới

### 1. Thêm vào tất cả 3 files:

**en.json:**
```json
{
  "myFeature": {
    "title": "My New Feature",
    "button": "Click Me"
  }
}
```

**vi.json:**
```json
{
  "myFeature": {
    "title": "Tính năng Mới của Tôi",
    "button": "Nhấn vào đây"
  }
}
```

**ko.json:**
```json
{
  "myFeature": {
    "title": "내 새로운 기능",
    "button": "클릭하세요"
  }
}
```

### 2. Sử dụng trong component:
```jsx
const { t } = useTranslation();

<h2>{t('myFeature.title')}</h2>
<button>{t('myFeature.button')}</button>
```

---

## 🔥 Tính năng Nâng cao

### 1. Đổi ngôn ngữ động:
```jsx
const { i18n } = useTranslation();

<button onClick={() => i18n.changeLanguage('vi')}>
  Tiếng Việt
</button>
```

### 2. Kiểm tra ngôn ngữ hiện tại:
```jsx
const { i18n } = useTranslation();

if (i18n.language === 'vi') {
  console.log('Đang dùng Tiếng Việt');
}
```

### 3. Interpolation (biến động):
```json
// en.json
{
  "welcome": "Welcome back, {{username}}!"
}
```

```jsx
t('welcome', { username: 'John' })
// Output: "Welcome back, John!"
```

---

## 🌐 Ngôn ngữ hỗ trợ

| Code | Language | Native Name |
|------|----------|-------------|
| `en` | English  | English     |
| `vi` | Vietnamese | Tiếng Việt |
| `ko` | Korean   | 한국어      |

---

## 🎯 Test Ngay!

1. Truy cập: **https://zk-gamma.vercel.app**
2. Tìm **LanguageSwitcher** button ở góc trên phải (cờ 🇺🇸/🇻🇳/🇰🇷)
3. Click để chuyển đổi ngôn ngữ
4. Reload trang → Ngôn ngữ được lưu!

---

## 📚 Tài liệu Chi tiết

Xem file: **`I18N_GUIDE.md`** để biết:
- Best practices
- Troubleshooting
- Advanced features
- Migration examples
- Full API reference

---

## ✨ Deployment Status

- ✅ Deployed to Vercel: https://zk-gamma.vercel.app
- ✅ Ngôn ngữ mặc định: English
- ✅ Auto-detect browser language
- ✅ Persist với localStorage

---

**Chúc bạn code vui! 🚀**
