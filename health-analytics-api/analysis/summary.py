"""
Analysis Module
Reusable aggregation functions used by the API
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "health.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_gender_summary():
    conn = get_connection()
    rows = conn.execute("""
        SELECT gender, COUNT(*) as count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM participants), 1) as percentage
        FROM participants
        GROUP BY gender
        ORDER BY count DESC
    """).fetchall()
    conn.close()
    return [{"gender": r[0], "count": r[1], "percentage": r[2]} for r in rows]

def get_age_group_summary():
    conn = get_connection()
    rows = conn.execute("""
        SELECT age_group, COUNT(*) as count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM participants), 1) as percentage
        FROM participants
        GROUP BY age_group
        ORDER BY age_group
    """).fetchall()
    conn.close()
    return [{"age_group": r[0], "count": r[1], "percentage": r[2]} for r in rows]

def get_clinic_summary():
    conn = get_connection()
    rows = conn.execute("""
        SELECT clinic, COUNT(*) as count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM participants), 1) as percentage
        FROM participants
        GROUP BY clinic
        ORDER BY count DESC
    """).fetchall()
    conn.close()
    return [{"clinic": r[0], "count": r[1], "percentage": r[2]} for r in rows]

def get_exposure_summary():
    conn = get_connection()
    rows = conn.execute("""
        SELECT exposure, COUNT(*) as count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM participants), 1) as percentage
        FROM participants
        GROUP BY exposure
        ORDER BY count DESC
    """).fetchall()
    conn.close()
    return [{"exposure": r[0], "count": r[1], "percentage": r[2]} for r in rows]

def get_gender_by_exposure():
    conn = get_connection()
    rows = conn.execute("""
        SELECT exposure, gender, COUNT(*) as count
        FROM participants
        GROUP BY exposure, gender
        ORDER BY exposure, gender
    """).fetchall()
    conn.close()
    return [{"exposure": r[0], "gender": r[1], "count": r[2]} for r in rows]

def get_age_by_exposure():
    conn = get_connection()
    rows = conn.execute("""
        SELECT exposure, age_group, COUNT(*) as count
        FROM participants
        GROUP BY exposure, age_group
        ORDER BY exposure, age_group
    """).fetchall()
    conn.close()
    return [{"exposure": r[0], "age_group": r[1], "count": r[2]} for r in rows]

def get_overall_stats():
    conn = get_connection()
    row = conn.execute("""
        SELECT
            COUNT(*)                        as total,
            ROUND(AVG(age), 1)              as avg_age,
            MIN(age)                        as min_age,
            MAX(age)                        as max_age,
            COUNT(DISTINCT clinic)          as total_clinics,
            COUNT(DISTINCT exposure)        as exposure_groups
        FROM participants
    """).fetchone()
    conn.close()
    return {
        "total_participants": row[0],
        "average_age":        row[1],
        "min_age":            row[2],
        "max_age":            row[3],
        "total_clinics":      row[4],
        "exposure_groups":    row[5],
    }
