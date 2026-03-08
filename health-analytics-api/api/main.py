"""
Health Analytics API
FastAPI app serving clinical trial participant data
Run: uvicorn api.main:app --reload
Docs: http://localhost:8000/docs
"""

import sqlite3
from pathlib import Path
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys

sys.path.append(str(Path(__file__).parent.parent))
from analysis.summary import (
    get_gender_summary,
    get_age_group_summary,
    get_clinic_summary,
    get_exposure_summary,
    get_gender_by_exposure,
    get_age_by_exposure,
    get_overall_stats,
    get_connection,
)

app = FastAPI(
    title="Health Research Analytics API",
    description="REST API for clinical trial participant data — Exposed vs Unexposed groups",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── ROOT ──
@app.get("/", tags=["Health"])
def root():
    return {
        "project":     "Health Research Analytics API",
        "version":     "1.0.0",
        "status":      "running",
        "docs":        "/docs",
        "endpoints": [
            "/participants",
            "/summary/stats",
            "/summary/gender",
            "/summary/age-groups",
            "/summary/clinics",
            "/summary/exposure",
            "/summary/gender-by-exposure",
            "/summary/age-by-exposure",
        ]
    }

# ── HEALTH CHECK ──
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

# ── PARTICIPANTS ──
@app.get("/participants", tags=["Participants"])
def get_participants(
    exposure: str = Query(None, description="Filter by 'Exposed' or 'Unexposed'"),
    gender:   str = Query(None, description="Filter by 'Male' or 'Female'"),
    clinic:   str = Query(None, description="Filter by clinic name"),
    limit:    int = Query(100, le=500, description="Max records to return"),
    offset:   int = Query(0, description="Pagination offset"),
):
    """Return participant records with optional filters."""
    conn  = get_connection()
    query = "SELECT * FROM participants WHERE 1=1"
    params = []

    if exposure:
        query += " AND exposure = ?"
        params.append(exposure)
    if gender:
        query += " AND gender = ?"
        params.append(gender)
    if clinic:
        query += " AND clinic = ?"
        params.append(clinic)

    query += f" LIMIT {limit} OFFSET {offset}"

    rows = conn.execute(query, params).fetchall()
    cols = ["record_id","event_name","gender","clinic","age","age_group","exposure"]
    conn.close()

    return {
        "total":  len(rows),
        "offset": offset,
        "limit":  limit,
        "data":   [dict(zip(cols, r)) for r in rows]
    }

# ── SUMMARY ENDPOINTS ──
@app.get("/summary/stats", tags=["Summary"])
def overall_stats():
    """Overall dataset statistics."""
    return get_overall_stats()

@app.get("/summary/gender", tags=["Summary"])
def gender_summary():
    """Gender distribution across all participants."""
    return {"data": get_gender_summary()}

@app.get("/summary/age-groups", tags=["Summary"])
def age_group_summary():
    """Participant count by age group."""
    return {"data": get_age_group_summary()}

@app.get("/summary/clinics", tags=["Summary"])
def clinic_summary():
    """Participant count by nearest clinic."""
    return {"data": get_clinic_summary()}

@app.get("/summary/exposure", tags=["Summary"])
def exposure_summary():
    """Exposed vs Unexposed participant counts."""
    return {"data": get_exposure_summary()}

@app.get("/summary/gender-by-exposure", tags=["Summary"])
def gender_by_exposure():
    """Gender breakdown within each exposure group."""
    return {"data": get_gender_by_exposure()}

@app.get("/summary/age-by-exposure", tags=["Summary"])
def age_by_exposure():
    """Age group breakdown within each exposure group."""
    return {"data": get_age_by_exposure()}
