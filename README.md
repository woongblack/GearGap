# GearGap

GearGap is a World of Warcraft utility that analyzes your character's gear and recommends the most efficient upgrades based on actual WCL data.

## Repository Structure

This project uses a monorepo structure separating the React frontend from the Python backend.

```
GearGap/
├── frontend/       # React + Vite + TypeScript (UI and logic)
├── backend/        # FastAPI Python backend (Data fetching and processing)
├── .gitignore      
└── README.md       
```

## Running the Application

### 1. Frontend
The frontend is built with React and Vite.

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### 2. Backend
The backend is built with FastAPI. It handles Blizzard API requests and score computation logic.

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

The backend API will be available at `http://localhost:8000`.

## Architecture Note
This structure isolates concerns. The `frontend/` relies exclusively on `/api/...` endpoints provided by the `backend/`. 
