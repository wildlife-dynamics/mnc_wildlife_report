# MNC Wildlife Report — User Guide

This guide walks you through configuring and running the MNC Wildlife Report workflow, which processes elephant, buffalo, rhino, lion, leopard, cheetah, giraffe, hartebeest, and wildlife incident events from EarthRanger to produce tabular CSV reports, interactive maps, herd-size charts, and a dashboard.

---

## Overview

The workflow delivers, for each run:

**CSV tables**
- **wildlife_events.csv** — raw dump of all 13 fetched event types, before any per-branch processing
- **wildlife_events_recorded.csv** — cleaned wildlife incident records (snares, fires, carcasses, injuries, veterinary treatments)
- **wildlife_incidents_summary_table.csv** — pivot table of wildlife incidents by type
- **wildlife_incidents_recorded_by_date.csv** — daily count of unique wildlife incident events
- **overall_elephant_summary_table.csv** / **overall_buffalo_summary_table.csv** — sighting counts by herd composition (Bachelor, Mixed, Female + Calf, Unspecified)
- **overall_lion_summary_table.csv** — sighting counts by pride
- **overall_leopard_summary_table.csv** / **overall_cheetah_summary_table.csv** — sighting counts by individuals present
- **overall_giraffe_summary_table.csv** / **overall_hart_summary_table.csv** / **overall_rhino_summary_table.csv** — daily sighting counts

**Maps and charts (interactive HTML)**
- **wildlife_incidents_map** — point map of wildlife incidents coloured by incident type
- **elephant_sightings_events** — point map of elephant sightings coloured by herd composition
- **elephant_herd_size_bar_chart** — bar chart of elephant herd size distribution
- **elephant_herd_types_map** — bubble map of elephant sightings, bubble size proportional to herd size
- **buffalo_sightings_events** / **buffalo_herd_size_bar_chart** / **buffalo_herd_types_map** — the same three views for buffalo
- **lion_pride_sightings_map** — point map of lion sightings coloured by pride
- **leopard_sightings_map** / **cheetah_sightings_map** — point maps coloured by individuals present
- **giraffe_sightings_map** / **hartebeest_sightings_map** / **rhino_sightings_map** — point maps of sightings

**Dashboard**

A single MNC Wildlife Report dashboard combining all of the above as 21 widgets — one map/chart/table widget per branch output described below.

---

## Prerequisites

Before running the workflow, ensure you have:

- Access to an **EarthRanger** instance with sighting and incident events recorded for the analysis period (`elephant_sighting_rep`, `buffalo_sighting_rep`, `rhino_sighting_rep`, `lion_sighting_rep`, `leopardsightingrep`, `cheetah_sighting_rep`, `giraffe_sighting`, `hartebeest_sighting`, `snare_rep`, `fire_rep`, `wildlife_injury_rep`, `wildlife_treatment_rep`, `wildlife_carcass_rep`)
- Network access to **Dropbox** so the workflow can download the MNC conservancy boundary and parcels files at runtime

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In the Ecoscope app, navigate to the **Workflow Templates** tab and click **Add Workflow Template** (top-right). In the **Github Link** field that appears, paste the repository URL:

```
https://github.com/wildlife-dynamics/mnc-wildlife-report.git
```

Then click **Add Template** to register the template.

---

### Step 2 — Configure the EarthRanger Connection

Navigate to **Data Sources** and click **Connect**. The **Connect Ecoscope to EarthRanger** dialog will open. Fill in the form:

| Field | Description |
|-------|-------------|
| Data Source Name | A label to identify this connection (e.g. `Mara North Conservancy`) |
| EarthRanger URL | Your instance URL (e.g. `your-site.pamdas.org`) |
| EarthRanger Username | Your EarthRanger username |
| EarthRanger Password | Your EarthRanger password |

> **Important:** Credentials entered here are **not** validated during setup. Any authentication errors will only appear when the workflow runs.

Click **Connect** to save the data source.

---

### Step 3 — Select the Workflow

Go back to **Workflow Templates**. The newly added template appears as the **mnc-wildlife-report** card (showing the source repository URL). Click the card to open the workflow configuration form.

---

### Step 4 — Configure Workflow Details, Time Range, and EarthRanger Connection

The configuration form is divided into three sections, each highlighted in the left-hand navigation panel.

**Set Workflow Details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run (required) |
| Workflow Description | Optional notes to differentiate this run from others (e.g. reporting month or site) |

**Time Range**

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start date and time — all wildlife events from this point are fetched |
| Until | End date and time of the analysis window |

**Connect to EarthRanger**

Select the EarthRanger data source configured in Step 2 from the **Data Source** dropdown (e.g. `Mara North Conservancy`).

Once all three sections are filled, click **Submit** to start the workflow.

---

## Running the Workflow

Once submitted, the runner will:

1. Download the MNC community conservancy boundary and parcels files from Dropbox; fix invalid geometries; build a grey conservancy-outline layer (filtered to `grazing_zone == Conservancy`) and a khaki-filled parcels layer. Compute the global map zoom level and centre from the Mara North Conservancy boundary extent — this view state is reused by every map in the workflow.
2. Fetch all 13 event types from EarthRanger for the analysis period as a single batch; persist the raw dump as `wildlife_events.csv`; extract the date from each event's timestamp; add a temporal index.
3. **Wildlife incidents branch** — filter `snare_rep`, `fire_rep`, `wildlife_injury_rep`, `wildlife_treatment_rep`, and `wildlife_carcass_rep` events; resolve field IDs to display titles; normalise and flatten event details; drop housekeeping columns; save the cleaned records as `wildlife_events_recorded.csv`; pivot by incident type and save as `wildlife_incidents_summary_table.csv`; count unique incidents per day and save as `wildlife_incidents_recorded_by_date.csv`; produce a point map coloured by incident type and save as `wildlife_incidents_map.html`.
4. **Elephant branch** — filter `elephant_sighting_rep` events; resolve field IDs to display titles; normalise and flatten event details; retain herd composition, herd size, and demographic columns (female, male, sub-adult, under a year); fill missing herd composition with Unspecified and missing counts with 0; standardise herd-composition labels (Bachelor, Mixed, Female + Calf, Unspecified); bin herd size into 5 equal-interval bins and produce a bar chart saved as `elephant_herd_size_bar_chart.html`; produce a clustered bubble map sized by herd size saved as `elephant_herd_types_map.html`; produce a herd-composition point map saved as `elephant_sightings_events.html`; summarise sightings by herd type and save as `overall_elephant_summary_table.csv`.
5. **Buffalo branch** — same pipeline as elephant, without the female/male/sub-adult/under-a-year breakdown; herd size and herd composition only. Produces `buffalo_herd_size_bar_chart.html`, `buffalo_herd_types_map.html`, `buffalo_sightings_events.html`, and `overall_buffalo_summary_table.csv`.
6. **Lion branch** — filter `lion_sighting_rep` events; resolve field IDs to display titles; normalise and flatten event details; retain female, male, group size, individuals present, pride, and young; fill missing pride with Undefined; produce a point map coloured by pride saved as `lion_pride_sightings_map.html`; summarise sightings by pride and save as `overall_lion_summary_table.csv`.
7. **Leopard branch** — filter `leopardsightingrep` events; retain female, male, group size, individuals present, and young; fill missing individuals-present with Undefined; produce a point map coloured by individuals present saved as `leopard_sightings_map.html`; summarise sightings by individuals present and save as `overall_leopard_summary_table.csv`.
8. **Cheetah branch** — identical pipeline to leopard; produces `cheetah_sightings_map.html` and `overall_cheetah_summary_table.csv`.
9. **Giraffe branch** — filter `giraffe_sighting` events; normalise and flatten event details; produce a point map saved as `giraffe_sightings_map.html`; count sightings per day and save as `overall_giraffe_summary_table.csv`.
10. **Hartebeest branch** — filter `hartebeest_sighting` events; same pipeline as giraffe; produces `hartebeest_sightings_map.html` and `overall_hart_summary_table.csv`.
11. **Rhino branch** — filter `rhino_sighting_rep` events; same pipeline as giraffe and hartebeest; produces `rhino_sightings_map.html` and `overall_rhino_summary_table.csv`.
12. Assemble the **MNC Wildlife Report dashboard** from all 21 map, chart, and table widgets produced above.
13. Save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

> Every task in the workflow is automatically skipped if its input data is empty or an upstream step was skipped, so a run with no events of a given type simply omits that branch's outputs rather than failing. Widget-creation steps are the exception — they always run so that a placeholder widget still appears on the dashboard even if the branch behind it was skipped.

---

## Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`.

### CSV Tables

| File | Description |
|------|-------------|
| `wildlife_events.csv` | Raw dump of all 13 fetched event types before branch processing |
| `wildlife_events_recorded.csv` | Cleaned wildlife incident records (snares, fires, carcasses, injuries, veterinary treatments) |
| `wildlife_incidents_summary_table.csv` | Pivot table of wildlife incidents by type (Fire, Snare, Wildlife carcass, Injured wildlife, Veterinary treatment) |
| `wildlife_incidents_recorded_by_date.csv` | Daily unique wildlife incident count (date, no_of_events) |
| `overall_elephant_summary_table.csv` | Elephant sighting counts by herd type (Bachelor, Mixed, Female + Calf, Unspecified) |
| `overall_buffalo_summary_table.csv` | Buffalo sighting counts by herd type |
| `overall_lion_summary_table.csv` | Lion sighting counts by pride |
| `overall_leopard_summary_table.csv` | Leopard sighting counts by individuals present |
| `overall_cheetah_summary_table.csv` | Cheetah sighting counts by individuals present |
| `overall_giraffe_summary_table.csv` | Daily unique giraffe sighting count |
| `overall_hart_summary_table.csv` | Daily unique hartebeest sighting count |
| `overall_rhino_summary_table.csv` | Daily unique rhino sighting count |

### Maps and Charts

| File | Description |
|------|-------------|
| `wildlife_incidents_map.html` | Wildlife incident locations coloured by incident type |
| `elephant_sightings_events.html` | Elephant sighting locations coloured by herd composition |
| `elephant_herd_size_bar_chart.html` | Bar chart of elephant herd size frequency distribution (5 bins) |
| `elephant_herd_types_map.html` | Clustered bubble map of elephant sightings; bubble size proportional to herd size |
| `buffalo_sightings_events.html` | Buffalo sighting locations coloured by herd composition |
| `buffalo_herd_size_bar_chart.html` | Bar chart of buffalo herd size frequency distribution (5 bins) |
| `buffalo_herd_types_map.html` | Clustered bubble map of buffalo sightings; bubble size proportional to herd size |
| `lion_pride_sightings_map.html` | Lion sighting locations coloured by pride |
| `leopard_sightings_map.html` | Leopard sighting locations coloured by individuals present |
| `cheetah_sightings_map.html` | Cheetah sighting locations coloured by individuals present |
| `giraffe_sightings_map.html` | Giraffe sighting locations on conservancy boundaries and parcels |
| `hartebeest_sightings_map.html` | Hartebeest sighting locations on conservancy boundaries and parcels |
| `rhino_sightings_map.html` | Rhino sighting locations on conservancy boundaries and parcels |

## Dashboard

The workflow run also produces the **MNC Wildlife Report dashboard**, viewable in the workflow runner, with 21 widgets:

| Widget | Source |
|--------|--------|
| Wildlife Incident Map | `wildlife_incidents_map.html` |
| Elephant Herd Size Map | `elephant_herd_types_map.html` |
| Elephant Herd Composition Map | `elephant_sightings_events.html` |
| Elephant Herd Size Distribution | `elephant_herd_size_bar_chart.html` |
| Elephant Herd Composition Summary | `overall_elephant_summary_table.csv` |
| Buffalo Herd Size Map | `buffalo_herd_types_map.html` |
| Buffalo Herd Composition Map | `buffalo_sightings_events.html` |
| Buffalo Herd Size Distribution | `buffalo_herd_size_bar_chart.html` |
| Buffalo Herd Composition Summary | `overall_buffalo_summary_table.csv` |
| Lion Sightings Map | `lion_pride_sightings_map.html` |
| Lion Sightings Summary | `overall_lion_summary_table.csv` |
| Leopard Sightings Map | `leopard_sightings_map.html` |
| Leopard Sightings Summary | `overall_leopard_summary_table.csv` |
| Cheetah Sightings Map | `cheetah_sightings_map.html` |
| Cheetah Sightings Summary | `overall_cheetah_summary_table.csv` |
| Giraffe Sightings Map | `giraffe_sightings_map.html` |
| Giraffe Sightings Summary | `overall_giraffe_summary_table.csv` |
| Hartebeest Sightings Map | `hartebeest_sightings_map.html` |
| Hartebeest Sightings Summary | `overall_hart_summary_table.csv` |
| Rhino Sightings Map | `rhino_sightings_map.html` |
| Rhino Sightings Summary | `overall_rhino_summary_table.csv` |

> Each table widget is sortable and filterable in place; downloading directly from the widget is disabled — use the corresponding CSV output file for that.
