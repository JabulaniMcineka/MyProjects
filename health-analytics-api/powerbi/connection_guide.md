# 📊 Power BI Connection Guide — Health Analytics API

---

## Prerequisites
- Power BI Desktop installed (free): https://powerbi.microsoft.com/desktop
- API running locally OR deployed on Azure

---

## Step 1 — Start the API

### Option A: Local (Docker)
```bash
docker-compose up -d
```
API ready at: **http://localhost:8000**

### Option B: Azure (after deployment)
API ready at: **https://health-analytics-api.azurewebsites.net**

> Test your API is working by opening http://localhost:8000/docs in your browser first.

---

## Step 2 — Connect Each Endpoint in Power BI

You will connect each endpoint as a separate query. Repeat for every endpoint you need.

### 2.1 Open Power BI Desktop
1. Click **Home** -> **Get Data** -> **Web**
2. Select **Basic**
3. Paste one of the URLs from the table below
4. Click **OK**

| Query Name | URL |
|---|---|
| Stats | `http://localhost:8000/summary/stats` |
| Gender | `http://localhost:8000/summary/gender` |
| AgeGroups | `http://localhost:8000/summary/age-groups` |
| Clinics | `http://localhost:8000/summary/clinics` |
| Exposure | `http://localhost:8000/summary/exposure` |
| GenderByExposure | `http://localhost:8000/summary/gender-by-exposure` |
| AgeByExposure | `http://localhost:8000/summary/age-by-exposure` |
| Participants | `http://localhost:8000/participants` |

---

## Step 3 — Transform Data in Power Query

### For summary endpoints (gender, age-groups, clinics, exposure, etc.)

The API returns JSON like:
```json
{ "data": [ {"gender": "Female", "count": 117, "percentage": 50.9} ] }
```

Steps:
1. In Power Query you will see a single cell showing "Record"
2. Click the "List" or "Record" icon next to "data"
3. Click "Into Table" (top left button)
4. Click the expand icon (two arrows) on the Column1 header
5. Tick all columns you want and click OK
6. Right-click "count" column -> Change Type -> Whole Number
7. Right-click "percentage" column -> Change Type -> Decimal Number
8. Rename the query (right panel) to match the Query Name from the table above
9. Click Close & Apply

### For the stats endpoint (/summary/stats)

The API returns a flat JSON object with no "data" array:
```json
{ "total_participants": 230, "average_age": 31.8, "min_age": 16, "max_age": 70 }
```

Steps:
1. You will see a table with two columns: Name and Value — no expansion needed
2. Right-click numeric values -> Change Type -> Whole Number or Decimal
3. Rename the query to Stats
4. Click Close & Apply

### For the participants endpoint (/participants)

The API returns:
```json
{ "total": 230, "offset": 0, "limit": 100, "data": [...] }
```

Steps:
1. Click the "data" field -> Into Table
2. Expand all columns
3. Set "age" column -> Whole Number, all others -> Text
4. Rename query to Participants
5. Click Close & Apply

---

## Step 4 — Build Your Dashboard

### Recommended Visuals

| Visual Type | Fields | Source Query |
|---|---|---|
| Card | Total Participants | Stats -> total_participants |
| Card | Average Age | Stats -> average_age |
| Card | Min / Max Age | Stats -> min_age / max_age |
| Donut Chart | Legend: gender, Values: count | Gender |
| Bar Chart | Axis: age_group, Values: count | AgeGroups |
| Clustered Bar | Axis: exposure, Values: count, Legend: gender | GenderByExposure |
| Clustered Bar | Axis: exposure, Values: count, Legend: age_group | AgeByExposure |
| Bar Chart | Axis: clinic, Values: count | Clinics |
| Pie Chart | Legend: exposure, Values: count | Exposure |
| Table | All columns | Participants |

### Suggested Layout

```
+-------------+-------------+-------------+
|  Total: 230 |  Avg Age:32 |  Clinics: 6 |   <- Cards
+-------------+-------------+-------------+
|  Gender Donut    |   Exposure Pie        |   <- Row 2
+------------------------------------------+
|  Age Groups Bar Chart (full width)       |   <- Row 3
+------------------------------------------+
|  Gender by Exposure  | Age by Exposure   |   <- Row 4
+------------------------------------------+
|  Participants Table (full width)         |   <- Row 5
+------------------------------------------+
```

---

## Step 5 — Add Slicers (Interactive Filters)

Add these slicers to make your dashboard interactive:
- Exposure Group slicer: Participants -> exposure
- Gender slicer: Participants -> gender
- Clinic slicer: Participants -> clinic

To add a slicer: select the Slicer visual -> drag your field into Field.

---

## Step 6 — After Azure Deployment

Update all data sources in one step:
1. Click Home -> Transform Data -> Data Source Settings
2. Select http://localhost:8000
3. Click Change Source
4. Replace with: https://health-analytics-api.azurewebsites.net
5. Click OK -> Close & Apply

All queries update automatically.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "Couldn't connect" error | Make sure API is running — open http://localhost:8000 in browser first |
| Data column shows List but won't expand | Click the List text first, then click Into Table |
| Columns show as "any" type | Manually set each column type in Power Query |
| Numbers showing as text | Right-click column -> Change Type -> Whole Number |
| Azure URL not working | Open https://your-url.azurewebsites.net/health to check if it's live |
| Data doesn't refresh | Click Home -> Refresh in Power BI |

---

## Publishing to Power BI Service (optional)

To share your dashboard online:
1. Click File -> Publish -> Publish to Power BI
2. Sign in with your Microsoft account (free)
3. Choose My Workspace
4. Dashboard live at: https://app.powerbi.com
