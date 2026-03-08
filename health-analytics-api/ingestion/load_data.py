"""
Ingestion Script
Loads CSV data into SQLite database
Run: python ingestion/load_data.py
"""

import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH   = Path(__file__).parent.parent / "data" / "health.db"
CSV_PATH  = Path(__file__).parent.parent / "data" / "combined_participants.csv"

def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS participants (
            record_id    TEXT PRIMARY KEY,
            event_name   TEXT,
            gender       TEXT,
            clinic       TEXT,
            age          INTEGER,
            age_group    TEXT,
            exposure     TEXT
        )
    """)
    conn.commit()

def extract_exposure(event_name: str) -> str:
    if "Unexposed" in str(event_name):
        return "Unexposed"
    elif "Exposed" in str(event_name):
        return "Exposed"
    return "Unknown"

def load(csv_path=CSV_PATH, db_path=DB_PATH):
    print("=" * 50)
    print("  HEALTH ANALYTICS — DATA INGESTION")
    print("=" * 50)

    print(f"\n📂 Reading CSV: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"   ✅ {len(df)} rows loaded")

    # Rename columns to clean names
    df = df.rename(columns={
        "Record ID":            "record_id",
        "Event Name":           "event_name",
        "Participant's Gender": "gender",
        "Nearest clinic":       "clinic",
        "Participant's Age":    "age",
        "Age group":            "age_group",
    })

    # Derive exposure column
    df["exposure"] = df["event_name"].apply(extract_exposure)

    print(f"\n🗄️  Writing to SQLite: {db_path}")
    conn = sqlite3.connect(db_path)
    create_table(conn)

    # Replace existing data
    df.to_sql("participants", conn, if_exists="replace", index=False)
    conn.commit()

    count = conn.execute("SELECT COUNT(*) FROM participants").fetchone()[0]
    conn.close()

    print(f"   ✅ {count} records inserted into participants table")
    print(f"\n📊 Quick summary:")
    print(f"   Exposed   : {len(df[df['exposure'] == 'Exposed'])}")
    print(f"   Unexposed : {len(df[df['exposure'] == 'Unexposed'])}")
    print(f"   Clinics   : {df['clinic'].nunique()}")
    print(f"   Age range : {df['age'].min()} – {df['age'].max()}")
    print(f"\n✅ Ingestion complete!")

if __name__ == "__main__":
    load()
