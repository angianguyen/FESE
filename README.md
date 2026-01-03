# FESE - Financial Engineering & Smart Economy

Dự án Monorepo kết hợp Backend (Python/FastAPI) và Blockchain (Solidity/Hardhat).

## Cấu trúc dự án

```
project_fese/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core configuration
│   │   ├── models/      # Data models
│   │   ├── services/    # Business logic
│   │   └── main.py      # FastAPI app entry point
│   └── tests/           # Backend tests
├── blockchain/          # Ethereum smart contracts
│   ├── contracts/       # Solidity contracts
│   ├── scripts/         # Deployment scripts
│   ├── tests/          # Contract tests
│   └── hardhat.config.js
├── shared/             # Shared resources
└── pyproject.toml      # Python dependencies
```

## Yêu cầu hệ thống

- Python 3.12+
- Node.js 18+
- npm hoặc yarn
- uv (Python package manager)

## Cài đặt

### 1. Cài đặt dependencies cho Backend (Python)
```bash
uv sync
```

### 2. Cài đặt dependencies cho Blockchain (Node.js)
```bash
cd blockchain
npm install
```

### 3. Tạo file cấu hình
```bash
cp .env.example .env
```

## Chạy dự án

### Backend (FastAPI)
```bash
# Từ thư mục gốc
make backend

# Hoặc
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API sẽ chạy tại: http://localhost:8000
- Docs: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

### Blockchain (Local Node)
```bash
# Terminal 1: Start local blockchain
make blockchain
# hoặc
cd blockchain
npm run node

# Terminal 2: Deploy contracts
make deploy
# hoặc
cd blockchain
npm run deploy:local
```

## Development

### Biên dịch Smart Contracts
```bash
cd blockchain
npm run compile
```

### Chạy tests
```bash
# Backend tests
pytest backend/tests

# Blockchain tests
cd blockchain
npm test
```

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pandas/NumPy** - Data analysis
- **Matplotlib/Seaborn** - Visualization

### Blockchain
- **Solidity ^0.8.20** - Smart contract language
- **Hardhat** - Development environment
- **OpenZeppelin** - Secure smart contract library
- **Ethers.js** - Ethereum library

## License

MIT
