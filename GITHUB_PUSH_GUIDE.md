# 🚀 Hướng dẫn Push Code lên GitHub

## ⚠️ Lỗi hiện tại:
```
remote: Permission to KhannGia/fesee.git denied to angianguyen.
fatal: unable to access 'https://github.com/KhannGia/fesee.git/': The requested URL returned error: 403
```

→ **Nguyên nhân:** Git đang dùng credentials của user `angianguyen`, không phải `KhannGia`

---

## ✅ Giải pháp 1: GitHub CLI (Khuyến nghị)

### Bước 1: Cài đặt GitHub CLI
```bash
winget install --id GitHub.cli
```

### Bước 2: Login với tài khoản KhannGia
```bash
gh auth login
```

Chọn:
- `? What account do you want to log into?` → **GitHub.com**
- `? What is your preferred protocol for Git operations?` → **HTTPS**
- `? Authenticate Git with your GitHub credentials?` → **Yes**
- `? How would you like to authenticate GitHub CLI?` → **Login with a web browser**

→ Copy code → Mở browser → Paste code → Authorize

### Bước 3: Push code
```bash
cd E:\fese_main
git push -u origin feature/protocol-console-sepolia
```

---

## ✅ Giải pháp 2: Personal Access Token (PAT)

### Bước 1: Tạo Token
1. Vào: https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Đặt tên: `fesee-deployment`
4. Chọn scopes:
   - ✅ `repo` (full control)
5. Click **Generate token**
6. **Copy token** (chỉ hiện 1 lần!)

### Bước 2: Cập nhật Remote URL
```bash
cd E:\fese_main
git remote set-url origin https://TOKEN@github.com/KhannGia/fesee.git
```

Thay `TOKEN` bằng token vừa copy.

**Ví dụ:**
```bash
git remote set-url origin https://ghp_abc123xyz789@github.com/KhannGia/fesee.git
```

### Bước 3: Push code
```bash
git push -u origin feature/protocol-console-sepolia
```

---

## ✅ Giải pháp 3: SSH Key (Bảo mật nhất)

### Bước 1: Tạo SSH Key
```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
```

Nhấn Enter 3 lần (không cần passphrase).

### Bước 2: Copy Public Key
```bash
cat ~/.ssh/id_ed25519.pub
```

### Bước 3: Add vào GitHub
1. Vào: https://github.com/settings/ssh/new
2. Title: `fesee-windows-pc`
3. Paste nội dung từ `id_ed25519.pub`
4. Click **Add SSH key**

### Bước 4: Đổi Remote sang SSH
```bash
cd E:\fese_main
git remote set-url origin git@github.com:KhannGia/fesee.git
```

### Bước 5: Push code
```bash
git push -u origin feature/protocol-console-sepolia
```

---

## 📋 Kiểm tra trạng thái

### Xem remote hiện tại:
```bash
git remote -v
```

### Xem branch hiện tại:
```bash
git branch -a
```

### Xem files đã commit:
```bash
git log --stat -1
```

---

## 🔐 Đảm bảo Bảo mật

### File .gitignore đã bảo vệ:
- ✅ `node_modules/` - Dependencies
- ✅ `.env` - Private keys, RPC URLs
- ✅ `artifacts/`, `cache/` - Build outputs
- ✅ `.next/` - Frontend build

### Kiểm tra .env KHÔNG bị commit:
```bash
git ls-files | grep ".env"
```

→ **Không có kết quả** = An toàn ✅

---

## 🚀 Sau khi Push thành công

### Xem branch trên GitHub:
```
https://github.com/KhannGia/fesee/tree/feature/protocol-console-sepolia
```

### Tạo Pull Request:
```
https://github.com/KhannGia/fesee/compare/feature/protocol-console-sepolia
```

---

## 🆘 Troubleshooting

### "fatal: Authentication failed"
→ Dùng GitHub CLI hoặc Personal Access Token

### "remote: Repository not found"
→ Kiểm tra spelling: `KhannGia/fesee` (không phải `fese`)

### "Everything up-to-date"
→ Không có thay đổi mới để push

### "error: failed to push some refs"
→ Pull trước rồi mới push:
```bash
git pull origin feature/protocol-console-sepolia --rebase
git push -u origin feature/protocol-console-sepolia
```

---

**Chọn Giải pháp 1 (GitHub CLI) nếu muốn nhanh!**
