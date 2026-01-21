# RateMyMP

A full-stack platform that empowers Canadians to hold their elected representatives accountable by visualizing MPs' voting records, conflicts of interest, and parliamentary activity through an intuitive, data-driven interface.

## Overview

RateMyMP bridges the gap between citizens and Parliament by aggregating and presenting federal political data in an accessible format. Search for your MP, explore their voting history, track parliamentary motions, and stay informed about how your representatives vote on issues that matter to you.

## Features

- **MP Search & Discovery**
  - Search by MP name or postal code
  - View comprehensive MP profiles with party affiliation and constituency
  
- **Parliamentary Motion Tracking**
  - Browse recent parliamentary motions and bills
  - Filter by category and voting outcome
  - View detailed vote breakdowns by party
  
- **Voting Records Visualization**
  - Interactive charts showing voting patterns
  - Party-by-party vote breakdowns
  - Historical voting trends

- **MP Report Cards**
  - Detailed voting history analysis
  - Conflicts of interest visualization
  - Parliamentary activity tracking
  
- **High-Performance Architecture**
  - React + TypeScript frontend with Tailwind CSS
  - Express.js backend with PostgreSQL database
  - React Query for efficient data caching
  - Sub-100ms API response times

## Tech Stack

**Frontend:**
- React 18 with TypeScript
- Tailwind CSS for styling
- React Query for state management and caching
- React Router for navigation
- Recharts for data visualization

**Backend:**
- Node.js with Express.js
- PostgreSQL database
- REST API architecture
- Automated data validation

**DevOps:**
- Docker containerization
- CI/CD pipeline (GitHub Actions)

## Data Sources

This project integrates data from trusted Canadian parliamentary sources:

- **[Our Commons](https://www.ourcommons.ca/)** - Official House of Commons data
- **[OpenParliament](https://openparliament.ca/)** - Parliamentary voting records and debates
- **[Parliament of Canada Open Data](https://www.parl.ca/opendata/)** - Official government APIs

## Getting Started

### Prerequisites

- Node.js 18+
- PostgreSQL 14+
- npm or yarn

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ratemymp.git
cd ratemymp
```

2. **Install dependencies**
```bash
# Install frontend dependencies
cd client
npm install

# Install backend dependencies
cd ../server
npm install
```

3. **Set up environment variables**
```bash
# In server directory
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

4. **Initialize database**
```bash
cd server
npm run db:migrate
npm run db:seed
```

5. **Run the application**
```bash
# Terminal 1 - Backend
cd server
npm run dev

# Terminal 2 - Frontend
cd client
npm run dev
```

The app will be available at `http://localhost:5173`

### Using Docker

```bash
docker-compose up
```

## 📁 Project Structure

```
ratemymp/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API service layer
│   │   └── hooks/         # Custom React hooks
│   └── package.json
├── server/                # Express backend
│   ├── src/
│   │   ├── routes/        # API routes
│   │   ├── controllers/   # Request handlers
│   │   ├── models/        # Database models
│   │   └── services/      # Business logic
│   └── package.json
└── docker-compose.yml
```

## Key Features Deep Dive

### MP Profile Pages
Each MP has a dedicated profile showing:
- Biographical information
- Current committee memberships
- Recent votes and positions
- Contact information

### Motion Tracking
Browse and filter parliamentary motions with:
- Category-based filtering
- Vote outcome visualization
- Party breakdown charts
- Historical motion archives

### Search Functionality
Find your representative quickly:
- Search by name (autocomplete)
- Lookup by postal code
- Filter by party or province

## Privacy & Data

- All data is sourced from public government records
- No user data is collected or stored
- Open-source and transparent

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting PRs.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

