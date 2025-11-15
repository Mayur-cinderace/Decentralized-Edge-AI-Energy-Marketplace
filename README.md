# Decentralized Edge AI Energy Marketplace

A comprehensive energy trading platform combining machine learning predictions with blockchain smart contracts for decentralized peer-to-peer energy trading.

## 📋 Project Overview

EnergiChain is a decentralized energy marketplace that enables:
- **Energy Producers** to list and sell generated energy (solar, wind, etc.)
- **Energy Consumers** to buy energy at competitive prices
- **AI-Powered Predictions** for energy generation and consumption
- **Blockchain-based Transactions** for secure and transparent trading
- **Smart Contracts** for automated energy trading and settlement

## 📁 Directory Structure

```
Decentralized-Edge-AI-Energy-Marketplace/
│
├── energichain_backend/           # Express.js backend server
│   ├── public/                    # Frontend HTML files & assets
│   │   ├── dashboard.html         # User dashboard
│   │   ├── login.html             # Login page
│   │   ├── signup.html            # Registration page
│   │   └── config/                # Contract configuration
│   │
│   ├── src/
│   │   ├── app.js                 # Express app configuration
│   │   ├── server.js              # Server entry point
│   │   ├── predict.py             # Python ML prediction script
│   │   │
│   │   ├── config/
│   │   │   └── db.js              # Database configuration
│   │   │
│   │   ├── controllers/
│   │   │   ├── authController.js  # Authentication logic
│   │   │   └── tradeController.js # Trade/marketplace logic
│   │   │
│   │   ├── middleware/
│   │   │   └── authMiddleware.js  # JWT authentication middleware
│   │   │
│   │   ├── models/
│   │   │   ├── User.js            # User database model
│   │   │   ├── Trade.js           # Trade database model
│   │   │   └── index.js           # Model initialization
│   │   │
│   │   └── routes/
│   │       ├── authRoutes.js      # Authentication endpoints
│   │       └── tradeRoutes.js     # Trade endpoints
│   │
│   ├── routes/
│   │   └── auth.js                # Additional auth routes
│   │
│   └── package.json               # Node dependencies
│
├── energichain-contract/          # Hardhat Solidity smart contracts
│   ├── contracts/
│   │   ├── EnergyMarketplace.sol  # Main marketplace contract
│   │   ├── EnergyOffer.sol        # Energy offer contract
│   │   └── Lock.sol               # Sample lock contract
│   │
│   ├── scripts/
│   │   ├── deploy.js              # Contract deployment script
│   │   └── check.js               # Contract verification script
│   │
│   ├── test/
│   │   └── Lock.js                # Contract tests
│   │
│   ├── ignition/
│   │   └── modules/
│   │       └── Lock.js            # Hardhat Ignition deployment module
│   │
│   ├── artifacts/                 # Compiled contract artifacts
│   ├── hardhat.config.js          # Hardhat configuration
│   └── package.json               # Node dependencies
│
├── model_train/                   # ML model training & API
│   ├── Train_Generation.py        # Solar generation model training
│   ├── regression.py              # Multi-plant regression model
│   ├── consumer.py                # Consumer consumption prediction
│   ├── api.py                     # FastAPI prediction server
│   ├── metrix_report.txt          # Model evaluation metrics
│   └── README.md                  # Model documentation
│
└── README.md                      # This file
```

## 🚀 Getting Started

### Prerequisites

- **Node.js** v18+
- **Python** 3.8+
- **PostgreSQL** (for backend database)
- **MetaMask** or similar Web3 wallet (for blockchain interaction)

### Backend Setup

```bash
cd energichain_backend
npm install
```

**Configuration:**
Create a `.env` file in `energichain_backend/`:
```env
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=energichain_db
DB_PORT=5432
JWT_SECRET=your_jwt_secret
PORT=5000
```

**Start Backend:**
```bash
node src/server.js
```

Backend runs on `http://localhost:5000`

### Smart Contract Setup

```bash
cd energichain-contract
npm install
```

**Configuration:**
Create a `.env` file in `energichain-contract/`:
```env
PRIVATE_KEY=your_wallet_private_key
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/your_infura_key
```

**Deploy Contracts:**
```bash
npx hardhat ignition deploy ./ignition/modules/Lock.js --network sepolia
```

**Run Tests:**
```bash
npx hardhat test
```

### ML Model Setup

```bash
cd model_train
pip install -r requirements.txt
```

**Requirements:**
```
pandas==2.0.0
numpy==1.24.0
scikit-learn==1.3.0
joblib==1.3.0
matplotlib==3.7.0
fastapi==0.100.0
uvicorn==0.23.0
```

**Train Models:**
```bash
python Train_Generation.py
python regression.py
python consumer.py
```

**Start Prediction API:**
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

API runs on `http://localhost:8000`

## 📊 Key Components

### Backend (Node.js/Express)

**Features:**
- User authentication & authorization (JWT)
- Energy trade management
- Database persistence (PostgreSQL with Sequelize ORM)
- RESTful API endpoints
- Python ML integration

**Key Endpoints:**
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `GET /trades` - List energy trades
- `POST /trades` - Create new trade
- `PUT /trades/:id` - Update trade
- `DELETE /trades/:id` - Delete trade

### Smart Contracts (Solidity)

**Contracts:**
1. **EnergyMarketplace.sol** - Main marketplace contract
   - Manages energy listings
   - Handles transactions
   - Enforces trade rules

2. **EnergyOffer.sol** - Energy offer contract
   - Represents individual energy offers
   - Tracks offer status
   - Manages offer lifecycle

**Contract Deployment:**
- Network: Sepolia Testnet (configurable)
- Compiler: Solidity 0.8+
- Framework: Hardhat

### ML Models (Python)

**Three Models:**

1. **Solar Generation Predictor** (Train_Generation.py)
   - Predicts AC power output
   - Uses RandomForestRegressor
   - Input: Irradiation, temperature, temporal features
   - Accuracy: Evaluated using R² and MSE

2. **Multi-Plant Regression** (regression.py)
   - Predicts energy across multiple plants
   - Handles multi-source data
   - Encodes categorical plant identifiers

3. **Consumer Consumption Predictor** (consumer.py)
   - Forecasts consumption patterns
   - Time-based feature engineering
   - Supports demand-side predictions

**Prediction API (FastAPI):**
```bash
POST /predict
{
  "ambient_temp": 25.5,
  "module_temp": 35.2,
  "irradiation": 800,
  "hour": 10,
  "day": 15,
  "month": 6,
  "source_key": "Plant_1"
}
```

Response:
```json
{
  "predicted_dc_power": 1250.5
}
```

## 🔐 Authentication

The platform uses JWT (JSON Web Tokens) for authentication:

1. User registers/logs in via `/auth/signup` or `/auth/login`
2. Backend returns JWT token
3. Token stored in browser localStorage
4. Token included in Authorization header for protected endpoints
5. Backend verifies token using `authMiddleware.js`

**Token Format:**
```
Authorization: Bearer <token>
```

## 💾 Database Schema

**PostgreSQL Tables:**

### Users
- `id` - Primary key
- `username` - Unique username
- `email` - User email
- `password` - Hashed password (bcrypt)
- `wallet_address` - Blockchain wallet address
- `role` - User role (producer/consumer)
- `created_at` - Timestamp

### Trades
- `id` - Primary key
- `seller_id` - Producer  user ID
- `buyer_id` - Consumer user ID
- `energy_amount` - kWh amount
- `price_per_unit` - Price/kWh
- `total_price` - Total trade value
- `status` - Trade status (pending/completed/cancelled)
- `transaction_hash` - Blockchain transaction hash
- `created_at` - Timestamp

## 🔗 Blockchain Integration

**Wallet Connection:**
1. User clicks "Connect Wallet" on dashboard
2. MetaMask/Web3 wallet prompts for connection
3. User's blockchain address stored in database
4. Smart contract transactions signed by user

**Trade Settlement:**
1. Energy trade created in database
2. Smart contract function called
3. Payment transferred via blockchain
4. Transaction hash stored
5. Trade marked as completed

## 📈 Workflow

```
1. User Registration & Login
   ↓
2. Connect Blockchain Wallet
   ↓
3. Browse Energy Listings
   (AI predictions show generation/consumption forecasts)
   ↓
4. Create/Accept Trade Offer
   ↓
5. Blockchain Transaction
   (Smart contract executes payment)
   ↓
6. Trade Completion
   (Energy transfer recorded)
```

## 🧪 Testing

**Backend Tests:**
```bash
cd energichain_backend
npm test
```

**Smart Contract Tests:**
```bash
cd energichain-contract
npx hardhat test
```

**ML Model Evaluation:**
Models output evaluation metrics to `metrix_report.txt` after training.

## 📚 API Documentation

### Authentication Endpoints
```
POST /auth/signup
POST /auth/login
GET /auth/profile (requires auth)
```

### Trade Endpoints
```
GET /trades (list all trades)
POST /trades (create trade, requires auth)
GET /trades/:id (get trade details)
PUT /trades/:id (update trade, requires auth)
DELETE /trades/:id (delete trade, requires auth)
```

### Prediction Endpoints (ML API)
```
POST /predict (energy generation forecast)
```

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Node.js, Express.js, Sequelize ORM |
| **Database** | PostgreSQL |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Blockchain** | Solidity, Hardhat, Ethers.js |
| **ML/AI** | Python, Scikit-learn, FastAPI |
| **Authentication** | JWT, bcrypt |
| **Web3** | MetaMask, Web3.js |

## 🔒 Security Considerations

1. **Password Security**: Bcrypt hashing with salt rounds
2. **API Authentication**: JWT tokens with expiration
3. **SQL Injection Prevention**: Sequelize parameterized queries
4. **Smart Contract Safety**: OpenZeppelin contracts audit
5. **CORS Configuration**: Restricted to trusted origins
6. **Environment Variables**: Sensitive data in .env files

## 📝 Environment Variables

### Backend (.env)
```env
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=energichain_db
DB_PORT=5432
JWT_SECRET=your_secret_key
JWT_EXPIRE=7d
PORT=5000
NODE_ENV=development
```

### Smart Contracts (.env)
```env
PRIVATE_KEY=your_private_key
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/key
ETHERSCAN_API_KEY=your_etherscan_key
```

## 🚨 Troubleshooting

**Backend Won't Start:**
- Check PostgreSQL is running
- Verify database credentials in `.env`
- Check port 5000 isn't in use

**Smart Contract Deployment Fails:**
- Verify private key in `.env`
- Check RPC URL connectivity
- Ensure sufficient test ETH on Sepolia

**ML API Errors:**
- Install all Python dependencies
- Check data files exist for model training
- Verify correct Python version (3.8+)

**Database Connection Issues:**
- Ensure PostgreSQL running: `sudo systemctl start postgresql`
- Check credentials in database config
- Create database: `createdb energichain_db`

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/feature-name`
2. Commit changes: `git commit -m 'Add feature'`
3. Push to branch: `git push origin feature/feature-name`
4. Open Pull Request

## 📄 License

ISC License - See individual package.json files for details

## 🤖 Future Enhancements

- [ ] Advanced AI models (LSTM/GRU for time series)
- [ ] Mobile app (React Native)
- [ ] Real-time notifications (WebSockets)
- [ ] Energy grid optimization algorithms
- [ ] Carbon footprint tracking
- [ ] Renewable energy certificates (REC) trading
- [ ] Advanced analytics dashboard
- [ ] Multi-chain support
- [ ] Automated market maker (AMM)
- [ ] Energy storage integration

## 👥 Team

- **Project**: Decentralized Edge AI Energy Marketplace
- **Repository**: Mayur-cinderace/Decentralized-Edge-AI-Energy-Marketplace

## 📞 Support

For issues and questions:
1. Check existing GitHub issues
2. Review documentation in component READMEs
3. Create detailed issue report with reproduction steps

## 🔗 Resources

- [Hardhat Documentation](https://hardhat.org/)
- [Express.js Guide](https://expressjs.com/)
- [Solidity Docs](https://docs.soliditylang.org/)
- [Scikit-learn Guide](https://scikit-learn.org/)
- [Sequelize ORM](https://sequelize.org/)
- [Web3.js Docs](https://web3js.readthedocs.io/)

---

**Last Updated:** November 15, 2025
