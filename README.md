# SPC-services
Smart Parking Credits Services

## Getting Started

### Prerequisites

```bash
brew install poetry
brew tap ethereum/ethereum
brew install solidity
npx hardhat init
npm install
cp example.env .env
```

### Build

```bash
poetry build
```

### Compile Contracts

```bash
npx hardhat compile
```

### Test

Run a Node:

```bash
npx hardhat node
```

Run tests:

```bash
poetry run pytest
```

## Run

### Deploy

```bash
poetry run python parkingmachine deploy
```

### QR Code Scanner

```bash
poetry run python client qr
```

### Parking Machine Service

```bash
poetry run python parkingmachine service 0x84eA74d481Ee0A5332c457a4d796187F6Ba67fEB
```
