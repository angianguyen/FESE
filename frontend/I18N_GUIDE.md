# i18n Implementation Guide for FESEE

## 🎯 Overview

This project now supports **multilingual internationalization (i18n)** with the following languages:
- 🇺🇸 English (en)
- 🇻🇳 Tiếng Việt (vi)
- 🇰🇷 한국어 (ko)

Language selection is automatically saved to `localStorage` and persists across sessions.

---

## 📁 File Structure

```
frontend/
├── lib/
│   └── i18n.js                 # i18n configuration
├── locales/
│   ├── en.json                 # English translations
│   ├── vi.json                 # Vietnamese translations
│   └── ko.json                 # Korean translations
├── components/
│   └── LanguageSwitcher.js     # Language switcher component
└── app/
    ├── providers.js            # I18nextProvider wrapper
    └── demo.jsx                # Updated with useTranslation
```

---

## 🚀 Quick Start

### 1. Using Translations in Components

```jsx
'use client';

import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();

  return (
    <div>
      <h1>{t('app.title')}</h1>
      <p>{t('app.subtitle')}</p>
      <button>{t('wallet.connect')}</button>
    </div>
  );
}
```

### 2. Translation Keys Reference

All translation keys are organized by feature area:

```javascript
// Navigation
t('nav.overview')       // "Overview" / "Tổng quan" / "개요"
t('nav.creditCheck')    // "Credit Check" / "Kiểm tra Tín dụng" / "신용 확인"

// Wallet
t('wallet.connect')     // "Connect Wallet" / "Kết nối Ví" / "지갑 연결"
t('wallet.disconnect')  // "Disconnect" / "Ngắt kết nối" / "연결 해제"

// Credit Check
t('creditCheck.title')           // "ZK Credit Verification"
t('creditCheck.generateProof')   // "Generate Proof"
t('creditCheck.submitOnChain')   // "Submit On-Chain"

// Borrow
t('borrow.title')                // "Borrow USDC"
t('borrow.submitBorrow')         // "Submit Borrow Request"

// Collateral
t('collateral.title')            // "Collateral NFT Management"
t('collateral.mint')             // "Mint New Collateral"
t('collateral.types.realEstate') // "Real Estate"

// Common
t('common.loading')    // "Loading..." / "Đang tải..." / "로딩 중..."
t('common.success')    // "Success" / "Thành công" / "성공"
t('common.error')      // "Error" / "Lỗi" / "오류"

// Errors
t('errors.walletNotConnected')   // "Please connect your wallet first"
t('errors.wrongNetwork')         // "Please switch to Sepolia network"
```

### 3. Using with Placeholders (Interpolation)

```jsx
// Add to your translation files:
// en.json: "welcome": "Welcome, {{name}}!"
// vi.json: "welcome": "Chào mừng, {{name}}!"
// ko.json: "welcome": "환영합니다, {{name}}!"

function WelcomeMessage({ username }) {
  const { t } = useTranslation();
  
  return <h1>{t('welcome', { name: username })}</h1>;
}
```

### 4. Changing Language Programmatically

```jsx
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { i18n } = useTranslation();

  const changeToVietnamese = () => {
    i18n.changeLanguage('vi');
  };

  return (
    <button onClick={changeToVietnamese}>
      Đổi sang Tiếng Việt
    </button>
  );
}
```

### 5. Getting Current Language

```jsx
function LanguageDisplay() {
  const { i18n } = useTranslation();
  
  return <p>Current language: {i18n.language}</p>;
}
```

---

## 🎨 LanguageSwitcher Component

Already integrated into the Navbar! The component features:

✅ Dropdown menu with flag icons  
✅ Shows current language with checkmark  
✅ Auto-saves to localStorage  
✅ Click-outside to close  
✅ Responsive design  
✅ Accessible (ARIA labels)

### Usage

```jsx
import LanguageSwitcher from '../components/LanguageSwitcher';

function Navigation() {
  return (
    <nav>
      <div>Logo</div>
      <LanguageSwitcher />
    </nav>
  );
}
```

---

## 📝 Adding New Translations

### Step 1: Add to all language files

```json
// locales/en.json
{
  "newFeature": {
    "title": "New Feature",
    "description": "This is a new feature"
  }
}

// locales/vi.json
{
  "newFeature": {
    "title": "Tính năng Mới",
    "description": "Đây là tính năng mới"
  }
}

// locales/ko.json
{
  "newFeature": {
    "title": "새로운 기능",
    "description": "이것은 새로운 기능입니다"
  }
}
```

### Step 2: Use in component

```jsx
function NewFeature() {
  const { t } = useTranslation();
  
  return (
    <div>
      <h2>{t('newFeature.title')}</h2>
      <p>{t('newFeature.description')}</p>
    </div>
  );
}
```

---

## 🔧 Advanced Features

### Pluralization

```json
// en.json
{
  "itemCount": "{{count}} item",
  "itemCount_plural": "{{count}} items"
}

// vi.json
{
  "itemCount": "{{count}} mục"
}
```

```jsx
t('itemCount', { count: 1 })  // "1 item" / "1 mục"
t('itemCount', { count: 5 })  // "5 items" / "5 mục"
```

### Conditional Translations

```jsx
function StatusMessage({ isSuccess }) {
  const { t } = useTranslation();
  
  return (
    <p className={isSuccess ? 'text-green-500' : 'text-red-500'}>
      {t(isSuccess ? 'common.success' : 'common.error')}
    </p>
  );
}
```

### Namespaces (for large apps)

```javascript
// lib/i18n.js - Add namespaces
const resources = {
  en: {
    common: enCommon,
    dashboard: enDashboard,
    settings: enSettings
  }
};

// Component usage
const { t } = useTranslation('dashboard');
t('title'); // from dashboard namespace
```

---

## 🌍 Adding New Languages

### Step 1: Create translation file

```bash
# Create new language file
touch locales/fr.json  # French
touch locales/es.json  # Spanish
```

### Step 2: Update i18n config

```javascript
// lib/i18n.js
import fr from '../locales/fr.json';
import es from '../locales/es.json';

const resources = {
  en: { translation: en },
  vi: { translation: vi },
  ko: { translation: ko },
  fr: { translation: fr },
  es: { translation: es }
};

export const languages = [
  { code: 'en', name: 'English', nativeName: 'English', flag: '🇺🇸' },
  { code: 'vi', name: 'Vietnamese', nativeName: 'Tiếng Việt', flag: '🇻🇳' },
  { code: 'ko', name: 'Korean', nativeName: '한국어', flag: '🇰🇷' },
  { code: 'fr', name: 'French', nativeName: 'Français', flag: '🇫🇷' },
  { code: 'es', name: 'Spanish', nativeName: 'Español', flag: '🇪🇸' }
];

i18n.init({
  supportedLngs: ['en', 'vi', 'ko', 'fr', 'es'],
  // ... rest of config
});
```

---

## 🐛 Troubleshooting

### Issue: Translations not showing

**Solution:**
```javascript
// Check if i18n is initialized
console.log(i18n.isInitialized);

// Check current language
console.log(i18n.language);

// Check if key exists
console.log(i18n.exists('app.title'));
```

### Issue: Language not persisting

**Solution:**
```javascript
// Check localStorage
console.log(localStorage.getItem('i18nextLng'));

// Clear and reset
localStorage.removeItem('i18nextLng');
i18n.changeLanguage('en');
```

### Issue: Missing translations

**Solution:**
```javascript
// Add fallback in config
i18n.init({
  fallbackLng: 'en',  // Falls back to English
  missingKeyHandler: (lng, ns, key) => {
    console.warn(`Missing translation: ${key} for ${lng}`);
  }
});
```

---

## 📊 Best Practices

### ✅ DO:
- Keep translation keys organized by feature
- Use nested objects for grouping
- Provide fallback text
- Test all languages before deploying
- Use descriptive key names

### ❌ DON'T:
- Hardcode text strings in components
- Use overly long translation keys
- Mix languages in one file
- Forget to add translations to all language files

---

## 🎯 Component Migration Examples

### Before (Hardcoded):
```jsx
function Header() {
  return <h1>Welcome to FESEE Platform</h1>;
}
```

### After (i18n):
```jsx
function Header() {
  const { t } = useTranslation();
  return <h1>{t('app.title')}</h1>;
}
```

---

## 📦 Package Dependencies

```json
{
  "dependencies": {
    "react-i18next": "^14.x.x",
    "i18next": "^23.x.x",
    "i18next-browser-languagedetector": "^7.x.x"
  }
}
```

---

## 🚀 Testing

```jsx
// Test in console
import { useTranslation } from 'react-i18next';

function TestTranslations() {
  const { t, i18n } = useTranslation();

  return (
    <div>
      <button onClick={() => i18n.changeLanguage('en')}>English</button>
      <button onClick={() => i18n.changeLanguage('vi')}>Tiếng Việt</button>
      <button onClick={() => i18n.changeLanguage('ko')}>한국어</button>
      
      <p>{t('app.title')}</p>
      <p>Current: {i18n.language}</p>
    </div>
  );
}
```

---

## 📞 Need Help?

- Check console for i18n errors
- Verify translation keys match exactly
- Ensure all language files are imported in `lib/i18n.js`
- Test with browser DevTools localStorage inspector

---

**Happy translating! 🌍✨**
