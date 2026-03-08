# 🏥 Health Research Analytics API

> A REST API built with FastAPI that serves clinical trial participant data — enabling gender, age, clinic, and exposure group analysis. Deployed on Azure App Service via Docker.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![Azure](https://img.shields.io/badge/Azure-App%20Service-0078D4)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![Status](https://img.shields.io/badge/API-✅%20Running-brightgreen)

---

## 🏗️ Architecture

```
CSV Files → Python Ingestion → SQLite DB → FastAPI → Azure App Service
                                                            ↓
                                                    Power BI Dashboard
```

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.12 | Core language |
| FastAPI | 0.111 | REST API framework |
| SQLite | Built-in | Lightweight database |
| Pandas | 2.2 | Data ingestion & transformation |
| Docker | Latest | Containerisation |
| Azure App Service | Free Tier | Cloud deployment |
| Power BI | Desktop | Dashboard & visualisation |

---

## 📁 Project Structure

```
health-analytics-api/
├── data/
│   ├── combined_participants.csv   # Source data
│   └── health.db                  # SQLite database (auto-generated)
├── ingestion/
│   └── load_data.py               # CSV → SQLite
├── api/
│   └── main.py                    # FastAPI endpoints
├── analysis/
│   └── summary.py                 # Aggregation functions
├── powerbi/
│   └── connection_guide.md        # How to connect Power BI
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── AZURE_DEPLOY.md
└── README.md
```

---

## 🚀 Getting Started

### Option A — Run with Docker (Recommended)
```bash
git clone https://github.com/JabulaniMcineka/health-analytics-api.git
cd health-analytics-api
docker-compose up -d
```
API live at: **http://localhost:8000**
Auto docs at: **http://localhost:8000/docs**

### Option B — Run locally
```bash
pip install -r requirements.txt
python ingestion/load_data.py
uvicorn api.main:app --reload
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Project info & endpoint list |
| GET | `/health` | Health check |
| GET | `/participants` | All participants (filterable) |
| GET | `/summary/stats` | Overall stats (total, avg age, etc.) |
| GET | `/summary/gender` | Gender distribution |
| GET | `/summary/age-groups` | Age group breakdown |
| GET | `/summary/clinics` | Participants by clinic |
| GET | `/summary/exposure` | Exposed vs Unexposed counts |
| GET | `/summary/gender-by-exposure` | Gender split per exposure group |
| GET | `/summary/age-by-exposure` | Age group split per exposure group |

### Filter Examples
```bash
# All exposed female participants
GET /participants?exposure=Exposed&gender=Female

# Participants from a specific clinic
GET /participants?clinic=Hlabisa Clinic

# Paginate results
GET /participants?limit=20&offset=40
```

---

## 📊 Power BI Integration
See [`powerbi/connection_guide.md`](powerbi/connection_guide.md) for step-by-step instructions on connecting Power BI to the API.

---

## ☁️ Azure Deployment
See [`AZURE_DEPLOY.md`](AZURE_DEPLOY.md) for step-by-step deployment to Azure App Service.

Live URL (after deployment):
```
https://health-analytics-api.azurewebsites.net/docs
```

---

## 👤 Author

**Jabulani Mcineka**
- 🏅 AWS Certified Cloud Practitioner (2025)
- 🏅 AWS Certified Data Engineer – Associate (2025)
- 🎓 Postgraduate Diploma in Computer Science — Tshwane University of Technology
- 🔗 [LinkedIn](https://www.linkedin.com/in/jabulani-mcineka-941360182)
- 💻 [GitHub](https://github.com/JabulaniMcineka)

---

## 📄 License
MIT
