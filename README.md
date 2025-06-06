NHL Expected Goals (xG) Analysis Platform
A full-stack application featuring a 92.28% AUC machine learning model for NHL shot prediction with an interactive visualization interface.
Show Image
🏒 Overview
This project demonstrates end-to-end ML engineering capabilities:

Backend: Python Flask API serving xG predictions
Frontend: Vue.js interactive rink visualization
Model: Random Forest achieving 92.28% AUC on 313,244 NHL shots
Features: 43 engineered features including player fatigue, shot quality, and game state

🚀 Quick Start
Prerequisites

Python 3.8+
Node.js 16+
Git

Installation

Clone the repository

bashgit clone https://github.com/renewedCRMsolutions/nhl-xg-analysis.git
cd nhl-xg-analysis

Set up Python backend

bash# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

Set up Vue frontend

bash# Install Node dependencies
npm install
Running the Application
You'll need two terminal windows:
Terminal 1 - Backend API:
bash# Make sure venv is activated
cd backend
python src/api.py
You should see:
Starting NHL xG API server...
Server running on http://localhost:8000
Terminal 2 - Frontend:
bash# From project root
npm run dev
You should see:
VITE v5.x.x ready in xxx ms
➜ Local: http://localhost:5173/
Using the Application

Open your browser to http://localhost:5173
Navigate to "xG Visualizer"
Click anywhere on the rink to see real-time xG predictions
Toggle shot modifiers (Rebound, Rush) to see probability changes
Switch to "NHL Game Data" mode to view pre-loaded shot patterns

📊 Model Performance

AUC: 0.9228
Test Samples: 62,649
Features: 43 (including shot distance, angle, player fatigue)
Top Feature: Shot distance (12.27% importance)

Shot Quality Color Coding

🔴 Red (Excellent): >25% chance
🟠 Orange (Great): 15-25% chance
🔵 Light Blue (Good): 8-15% chance
🔷 Dark Blue: <8% (needs screen/deflection)

🛠 API Endpoints
Health Check
GET http://localhost:8000/health
Single Shot Prediction
POST http://localhost:8000/predict/expected-goals
Content-Type: application/json

{
  "xCord": 75,
  "yCord": 0,
  "shotType": "WRIST",
  "shotRebound": 0,
  "shotRush": 0
}
Model Information
GET http://localhost:8000/model/info
📁 Project Structure
nhl-xg-analysis/
├── backend/
│   ├── src/
│   │   ├── api.py          # Flask API server
│   │   ├── predict.py      # xG prediction logic
│   │   └── demo.py         # CLI demo
│   ├── models/             # Trained model files
│   ├── data/               # Sample data
│   └── notebooks/          # Jupyter notebooks
│
├── frontend/
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript types
│   │   └── views/          # Page views
│   └── public/             # Static assets
│
├── visualizations/         # Model performance charts
├── package.json           # Node dependencies
├── requirements.txt       # Python dependencies
└── README.md
🧪 Testing
Backend Tests
bashcd backend
python -m pytest tests/
Frontend Tests
bashnpm run test:unit
Manual Testing

Click various rink locations to verify xG calculations
Test shot modifiers (rebound increases xG by ~25%)
Verify color coding matches probability ranges
Check API response times (<50ms locally)

🚢 Deployment
Backend (Railway/Render)
bashcd backend
# Create requirements.txt if needed
pip freeze > requirements.txt

# Deploy to Railway
railway up
Frontend (Vercel/Netlify)
bash# Build for production
npm run build

# Deploy to Vercel
vercel --prod

# Or drag 'dist' folder to Netlify
🔧 Configuration
Environment Variables
Create .env file in project root:
env# Backend
FLASK_ENV=development
FLASK_DEBUG=True

# Frontend
VITE_API_URL=http://localhost:8000
CORS Configuration
The backend is configured to accept requests from localhost:5173. Update backend/src/api.py for production domains.
📈 Future Enhancements

 Real-time NHL game data integration
 Player-specific xG adjustments
 Historical shot pattern analysis
 Team tendency reports
 Mobile responsive design
 Export visualizations as images

🤝 Contributing
This project was built to demonstrate capabilities for the Pittsburgh Penguins analytics role. For collaboration inquiries: robert@renewed.solutions
📄 License
MIT License - See LICENSE file for details
👨‍💻 Author
Robert Wolfe

Email: robert@renewed.solutions
GitHub: @renewedCRMsolutions
Location: Evans City, PA (Pittsburgh area)


Built with passion for hockey analytics and the Pittsburgh Penguins 🐧