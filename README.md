# Vita-AI 🧠💬  
**AI Health Insight Engine with Gemini Chatbot**  

## 📌 Overview  
Vita-AI is an **AI-powered health analysis and chatbot platform** that processes health metrics, generates personalized insights, and answers queries in real-time.  

- 🧠 **Hybrid Health Insight Engine** → Built using Python, Pandas, and basic ML to process user-uploaded health data (CSV).  
- 💬 **Gemini-Powered Chatbot** → Integrated with a modern React/Next.js frontend for real-time, context-aware health conversations.  
- 📊 **Data-Driven Insights** → Visual health trends, risk alerts, and personalized recommendations to improve wellness engagement.  
- ☁ **Cloud Deployment** → Backend deployed on Render using Flask for seamless scalability.  

---

## 📂 Project Structure  

```
Vita-AI/
│
├── ZMLB/                  # Backend services
│   ├── api.py              # Flask API for chatbot & health insights
│   ├── hybrid_insight_engine.py  # Insight generation engine (rule-based + ML)
│   ├── trends.py           # Health trend plotting logic
│   ├── requirements.txt    # Python dependencies
│   ├── render.yaml         # Deployment config for Render
│   ├── main.py              # Streamlit chatbot entry point
│   └── vita-health-chatbot/ # Chatbot backend code
│
├── ZMLF/                   # Frontend web app (Next.js + TailwindCSS)
│   ├── app/                # Main app pages & routes
│   ├── components/         # Reusable UI components
│   ├── insights/           # Health insights UI views
│   ├── globals.css         # Global styles
│   ├── package.json        # Frontend dependencies
│   └── tailwind.config.js  # TailwindCSS configuration
│
├── ZML-CSV/                # CSV datasets for chatbot & insights
│
└── README.md               # Project documentation
```

---

## 🚀 Features  
- 💬 **Real-Time Health Conversations** → Context-aware chatbot powered by Gemini API.  
- 📊 **Personalized Insights** → Hybrid health analysis using uploaded CSV files.  
- 🌐 **Modern UI** → Next.js + TailwindCSS interface for smooth user interaction.  
- 🔌 **REST API** → Flask backend delivering insights and chatbot responses.  
- 📈 **Visual Trends & Alerts** → Graphical trends, risk detection, and wellness tips.  
- ☁ **Fully Deployable** → Backend ready for cloud deployment with `render.yaml`.  

---

## 🛠️ Tech Stack  

**Frontend**  
- Next.js  
- Tailwind CSS  
- React Chatbot UI  

**Backend**  
- Python 3.x  
- Flask  
- Pandas, NumPy  
- Matplotlib (trend plotting)  
- Google Gemini API  

**Deployment**  
- Render  
- Streamlit (for chatbot interface)  

---

## 📦 Installation  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/VidweshK182/Vita-AI.git
cd Vita-AI
```

### 2️⃣ Backend Setup (ZMLB)  
```bash
cd ZMLB
pip install -r requirements.txt
```

---

## ⚙️ Environment Variables  

**Backend `.env`**  
```
MONGO_URI=<your_mongodb_connection_string>
GEMINI_API_KEY=<your_gemini_api_key>
```

**Frontend `.env.local`**  
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

---

## 📈 Usage  

### ▶️ Run the Streamlit Chatbot  
```bash
cd ZMLB
python main.py
```

### ▶️ Run the Backend API  
```bash
cd ZMLB
python api.py
```

### ▶️ Run the Frontend Web App  
```bash
cd ZMLF
npm install
npm run dev
```

Open the application in your browser:  
- **Frontend UI:** `http://localhost:3000`  
- **Backend API:** `http://localhost:5000`  
- **Streamlit Chatbot:** URL provided by Streamlit after running `main.py`  

---

## 🧠 How It Works 

### 1. Chatbot Layer (Streamlit + Gemini API)
- **SYSTEM_PROMPT** defines the chatbot's tone and scope (health domains: sleep, hydration, nutrition, fitness, mental health, etc.).  
- **ask_gemini()** combines system prompt, chat history, and optional CSV/JSON/TXT insights before sending to Gemini API.  
- Supports **CSV, JSON, TXT** file uploads to provide context to the chatbot.  
- Maintains conversation context using `streamlit.session_state`.  
- Chat history exportable as `.txt`.  

### 2. Backend Insight Engine (Flask)
- Accepts CSV uploads from frontend (`/upload-csv/` endpoint).  
- Uses **hybrid_insight_engine.py** to run rule-based + ML mood prediction analysis.  
- Generates **Matplotlib-based health trend plots** encoded as base64 for frontend embedding.  
- CORS enabled for integration with frontend deployments on Vercel/localhost.  

### 3. Insight Generation Logic
- **Rule-Based:** Detects hydration, sleep, and step count patterns.  
- **Machine Learning:** Logistic Regression predicts mood trends based on past data.  
- Insights returned as human-readable recommendations.  

### 4. Frontend (React + Tailwind)
- Responsive, modern dashboard for health visualizations & chatbot integration.  
- Consumes backend API and renders chart images & textual insights.  

---

## 🧪 Example Insights Output  
```text
"Your hydration has been low for 3+ days. Increase water intake."
"Two days of low sleep logged. Try to wind down earlier tonight."
"Your average steps (4321) are below the healthy range. Try to stay more active."
"You've had 4 down days recently. Try practicing self-care and connecting with loved ones."
```

---

## 🎯 Why This Project Stands Out  
- Combines **AI + Health Analytics** into a cohesive, real-world style product.  
- Demonstrates **prompt engineering, data processing, API integration, and full-stack development**.  
- Uses **both rule-based logic & ML** for richer recommendations.  
- Deployable with minimal configuration using `render.yaml`.  
