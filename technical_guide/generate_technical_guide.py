"""
Generate the MNC Wildlife Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: mnc_wildlife_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "mnc_wildlife_report_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)

def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"MNC Wildlife Report — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)
W = A4[0] - 4*cm

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("MNC Wildlife Report", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Wildlife sightings and incident reporting across the Mara North Conservancy", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>mnc-wildlife-report</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>mnc-wildlife-report</b> workflow fetches wildlife sighting and "
      "incident events from EarthRanger for a specified time window in a "
      "single batch and routes them into nine independent reporting branches "
      "— one per species group (elephant, buffalo, rhino, lion, leopard, "
      "cheetah, giraffe, hartebeest) and one for wildlife incidents (snares, "
      "fires, carcasses, injuries, veterinary treatments). Before any event "
      "data is fetched, the workflow downloads the MNC conservancy boundary "
      "and parcels geospatial files from Dropbox and computes a single shared "
      "map view state from the Mara North Conservancy boundary, reused by "
      "every map the workflow produces."),
    sp(4),
    p("The workflow delivers:"),
    bullet("<b>12 CSV tables</b> — a raw event dump, cleaned/pivoted wildlife "
           "incident records, and per-species sighting summaries"),
    bullet("<b>13 interactive HTML maps and charts</b> — herd-composition "
           "point maps for elephant and buffalo, clustered herd-size bubble "
           "maps and bar charts for elephant and buffalo, category-coloured "
           "point maps for lion/leopard/cheetah, plain sighting maps for "
           "giraffe/hartebeest/rhino, and an incident-type map"),
    bullet("<b>1 dashboard</b> with 21 widgets — one map, chart, or table "
           "widget per output above (the two wildlife-incident CSV summaries "
           "are not wrapped as dashboard widgets)"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output", "Type", "Branch"],
            ["wildlife_events.csv",                    "CSV",   "Raw event dump (all 13 types)"],
            ["wildlife_incidents_map.html",             "Map",   "Wildlife incidents — by type"],
            ["wildlife_events_recorded.csv",            "CSV",   "Wildlife incidents — cleaned"],
            ["wildlife_incidents_summary_table.csv",    "CSV",   "Wildlife incidents — pivoted"],
            ["wildlife_incidents_recorded_by_date.csv", "CSV",   "Wildlife incidents — by date"],
            ["elephant_sightings_events.html",          "Map",   "Elephant — herd composition"],
            ["elephant_herd_size_bar_chart.html",       "Chart", "Elephant — herd size bins"],
            ["elephant_herd_types_map.html",             "Map",  "Elephant — herd size bubbles"],
            ["overall_elephant_summary_table.csv",      "CSV",  "Elephant — by herd type"],
            ["buffalo_sightings_events.html",           "Map",  "Buffalo — herd composition"],
            ["buffalo_herd_size_bar_chart.html",        "Chart","Buffalo — herd size bins"],
            ["buffalo_herd_types_map.html",              "Map", "Buffalo — herd size bubbles"],
            ["overall_buffalo_summary_table.csv",       "CSV",  "Buffalo — by herd type"],
            ["lion_pride_sightings_map.html",           "Map",  "Lion — by pride"],
            ["overall_lion_summary_table.csv",          "CSV",  "Lion — by pride"],
            ["leopard_sightings_map.html",              "Map",  "Leopard — by individual"],
            ["overall_leopard_summary_table.csv",       "CSV",  "Leopard — by individual"],
            ["cheetah_sightings_map.html",              "Map",  "Cheetah — by individual"],
            ["overall_cheetah_summary_table.csv",       "CSV",  "Cheetah — by individual"],
            ["giraffe_sightings_map.html",              "Map",  "Giraffe sightings"],
            ["overall_giraffe_summary_table.csv",       "CSV",  "Giraffe — by date"],
            ["hartebeest_sightings_map.html",           "Map",  "Hartebeest sightings"],
            ["overall_hart_summary_table.csv",          "CSV",  "Hartebeest — by date"],
            ["rhino_sightings_map.html",                "Map",  "Rhino sightings"],
            ["overall_rhino_summary_table.csv",         "CSV",  "Rhino — by date"],
        ],
        [7*cm, 1.8*cm, W - 8.8*cm],
    ),
    note("Earlier versions of this workflow also rendered every map and "
         "chart as a PNG via html_to_png. The current spec no longer produces "
         "PNGs — every map, chart, and summary table is HTML only, persisted "
         "with persist_text or persist_df."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-platform",                ">=2.15.0, <2.16.0", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",    "0.1.0rc14.*", "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",       "0.0.0rc1.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-wwf-virunga","0.0.0rc9.*", "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-big-life",  "1.0.1.*",     "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",       "1.0.1.*",     "ecoscope-workflows-custom"],
            ["pydeck",                            "0.9.2",       "conda-forge"],
            ["opentelemetry-sdk",                 ">=1.20.0, <2.0.0", "conda-forge"],
        ],
        [6.7*cm, 3.3*cm, W - 10*cm],
    ),
    note("<b>ecoscope-platform</b> replaces the previously separate "
         "<b>ecoscope-workflows-core</b> and <b>ecoscope-workflows-ext-ecoscope</b> "
         "packages. <b>ecoscope-workflows-ext-wwf-virunga</b> is a new dependency "
         "in this spec, added solely to provide the draw_bar_chart task used by "
         "the elephant and buffalo herd-size charts. <b>ecoscope-workflows-ext-mep</b>, "
         "listed in earlier versions of this spec, is no longer required. "
         "<b>opentelemetry-sdk</b> enables distributed tracing for the compiled "
         "workflow's task graph; <b>pydeck</b> backs the base-map tile layers."),
    sp(6),
    h2("2.2  Connections and external assets"),
    make_table(
        [
            ["Asset", "Task / Source", "Purpose"],
            ["EarthRanger", "set_er_connection",
             "Fetch event records and resolve event detail display titles "
             "via process_events_details (used by all branches except giraffe, "
             "hartebeest, and rhino need it too — every species branch calls it)."],
            ["mnc_conservancy.gpkg", "ecoscope_workflows_ext_ste.tasks.io.fetch_and_persist_file (Dropbox)",
             "MNC community conservancy boundaries. Filtered twice: to "
             "grazing_zone == Conservancy for the outline layer, and to "
             "name == Mara North Conservancy to compute the shared map view state."],
            ["mnc_across_the_river_parcels.gpkg", "ecoscope_workflows_ext_ste.tasks.io.fetch_and_persist_file (Dropbox)",
             "MNC across-the-river land parcels, rendered as a filled polygon "
             "layer on every map."],
        ],
        [3.5*cm, 5.2*cm, W - 8.7*cm],
    ),
    note("Both Dropbox files are downloaded with overwrite_existing: false and "
         "retries: 3, via the ecoscope_workflows_ext_ste.tasks.io namespace "
         "(previously the bare fetch_and_persist_file task). If the files "
         "already exist from a previous run, the download step is skipped."),
    sp(6),
    h2("2.3  Grouper and global skip conditions"),
    p("The workflow uses an <b>empty grouper list</b> (groupers: []). "
      "All records are processed as a single undivided dataset; the grouper "
      "is passed through to the temporal index and the dashboard only."),
    sp(4),
    p("A single <b>task-instance-defaults</b> block at the top of the spec "
      "applies the same skipif conditions — <b>any_is_empty_df</b> and "
      "<b>any_dependency_skipped</b> — to every task automatically, instead "
      "of each task repeating an identical skipif block. See Section 8.1 for "
      "the one class of task that explicitly overrides this default."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. GEOSPATIAL ASSET PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Geospatial Asset Pipeline"),
    hr(),
    p("Before any event data is fetched, the workflow prepares the base map "
      "layers and view state shared by every map it produces."),
    sp(6),
    h2("3.1  Base map tile layers"),
    p("Task: <b>set_base_maps_pydeck</b>. Two raster tile layers are "
      "configured: an Esri World Hillshade layer (opacity 0.80) and an Esri "
      "World Boundaries and Places (Alternate) reference layer (opacity 0.35), "
      "both capped at max_zoom 20."),
    sp(6),
    h2("3.2  Conservancy boundary and parcels layers"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "ecoscope_workflows_ext_ste.tasks.io.fetch_and_persist_file",
             "Download <b>mnc_conservancy.gpkg</b> and "
             "<b>mnc_across_the_river_parcels.gpkg</b> from Dropbox."],
            ["2", "load_df",
             "Load each into a GeoDataFrame (layer: null, deserialize_json: false)."],
            ["3", "ecoscope_workflows_ext_mnc.tasks.transformation.fix_invalid_geometries",
             "Repair invalid geometries in the conservancy boundary GeoDataFrame."],
            ["4", "filter_df (×2)",
             "Filter the fixed boundary to grazing_zone == 'Conservancy' for the "
             "outline layer, and separately to name == 'Mara North Conservancy' "
             "for the view-state calculation (Section 3.3)."],
            ["5", "ecoscope_workflows_ext_custom.tasks.results.create_geojson_layer (×2)",
             "<b>Conservancy layer</b> — unfilled, grey outline "
             "(get_line_color: [169,169,169], line width 1.75). "
             "<b>Parcels layer</b> — filled dark khaki "
             "(get_fill_color: [189,183,107,60], line width 1.5, legend title "
             "'Map Layers')."],
        ],
        [1.2*cm, 6.5*cm, W - 7.7*cm],
    ),
    note("Earlier versions of this workflow split the conservancy boundary "
         "into six styled grazing-zone layers (Conservancy Herd Zone, Grazing "
         "Zones 1–4) and rendered a text-label layer with conservancy names. "
         "Both have been removed from the current spec — every map now uses "
         "only the plain conservancy outline and the parcels layer as static "
         "background."),
    sp(6),
    h2("3.3  Shared map view state"),
    p("Task group <b>Map Zoom &amp; Extent</b>: "
      "<b>ecoscope_workflows_ext_ste.tasks.spatial_operations.envelope_gdf</b> "
      "computes the bounding envelope of the Mara North Conservancy boundary "
      "(filter_mara_north), then "
      "<b>ecoscope_workflows_ext_ste.tasks.spatial_operations.compute_view_state_from_gdf</b> "
      "derives a view state from that envelope (pitch: 0, bearing: 0, "
      "max_zoom: 15). This single view state (<b>gdf_image_extent</b>) is "
      "passed to every draw_map call in the workflow — none of the eleven "
      "maps compute their own."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. EVENT INGESTION PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Event Ingestion Pipeline"),
    hr(),
    h2("4.1  Event retrieval"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task",       "get_events"],
            ["event_types","elephant_sighting_rep, buffalo_sighting_rep, "
                           "rhino_sighting_rep, lion_sighting_rep, "
                           "leopardsightingrep, cheetah_sighting_rep, "
                           "giraffe_sighting, hartebeest_sighting, "
                           "snare_rep, fire_rep, wildlife_injury_rep, "
                           "wildlife_treatment_rep, wildlife_carcass_rep"],
            ["Columns retained",
             "id, time, event_type, event_category, reported_by, "
             "serial_number, geometry, created_at, event_details, patrols"],
            ["include_details",         "true"],
            ["raise_on_empty",          "true"],
            ["include_null_geometry",   "false"],
            ["include_updates",         "false"],
            ["include_related_events",  "false"],
            ["include_display_values",  "false"],
            ["force_point_geometry",    "true"],
        ],
        [5*cm, W - 5*cm],
    ),
    note("All 13 event types are fetched in a single get_events call, then "
         "persisted verbatim as <b>wildlife_events.csv</b> before any "
         "per-branch filtering. force_point_geometry: true normalises every "
         "event's geometry to a point before it reaches the branch pipelines."),
    sp(6),
    h2("4.2  Date extraction and temporal indexing"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "extract_column_as_type",
             "Extract the <b>time</b> column as <b>output_type: date</b> "
             "into a new column named <b>date</b>."],
            ["2", "add_temporal_index",
             "Add a temporal index using <b>time_col: date</b>, "
             "groupers: [], cast_to_datetime: true, format: mixed. "
             "Produces <b>events_temporal</b>, the shared input to every branch."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("4.3  Branch filters"),
    p("Every branch begins by filtering events_temporal to its own event "
      "type(s). Species branches use <b>filter_df</b> (op: equal); the "
      "wildlife incidents branch uses <b>filter_row_values</b> to capture "
      "five event types in one step."),
    make_table(
        [
            ["Branch", "Filter task", "event_type value(s)"],
            ["Wildlife incidents", "filter_row_values",
             "snare_rep, fire_rep, wildlife_injury_rep, "
             "wildlife_treatment_rep, wildlife_carcass_rep"],
            ["Elephant",    "filter_df", "elephant_sighting_rep"],
            ["Buffalo",     "filter_df", "buffalo_sighting_rep"],
            ["Lion",        "filter_df", "lion_sighting_rep"],
            ["Leopard",     "filter_df", "leopardsightingrep"],
            ["Cheetah",     "filter_df", "cheetah_sighting_rep"],
            ["Giraffe",     "filter_df", "giraffe_sighting"],
            ["Hartebeest",  "filter_df", "hartebeest_sighting"],
            ["Rhino",       "filter_df", "rhino_sighting_rep"],
        ],
        [3.8*cm, 3.2*cm, W - 7*cm],
    ),
    sp(6),
    h2("4.4  Common species normalisation pattern"),
    p("Every species branch runs the same three steps after filtering, "
      "using the EarthRanger client to resolve display titles:"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "process_events_details",
             "Resolve event detail field IDs to display titles "
             "(map_to_titles: true, ordered: true)."],
            ["2", "normalize_json_column",
             "Flatten the <b>event_details</b> JSON column "
             "(skip_if_not_exists: true, sort_columns: true)."],
            ["3", "drop_column_prefix",
             "Remove the <b>event_details__</b> prefix from all flattened "
             "columns (duplicate_strategy: keep_original)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    p("Elephant, buffalo, lion, leopard, and cheetah additionally run a "
      "<b>map_columns</b> step to drop housekeeping columns and rename fields "
      "to snake_case (parameters vary per branch — see Sections 6–9). "
      "Giraffe, hartebeest, and rhino skip map_columns entirely and pass the "
      "prefix-dropped output directly into their map and summary steps."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. BRANCH 1 — WILDLIFE INCIDENTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Branch 1 — Wildlife Incidents"),
    hr(),
    p("Captures five incident event types in one filter_row_values step and "
      "produces three CSV tables plus a point map."),
    sp(6),
    h2("5.1  Normalisation and column selection"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "process_events_details",
             "Resolve field IDs to display titles (map_to_titles: true, ordered: true)."],
            ["2", "normalize_json_column",
             "Flatten event_details (skip_if_not_exists: true, sort_columns: true)."],
            ["3", "drop_column_prefix",
             "Remove the event_details__ prefix (duplicate_strategy: keep_original)."],
            ["4", "map_columns",
             "Drop index, time, event_category, reported_by, serial_number "
             "(retain_columns: [], rename_columns: {}, raise_if_not_found: false)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("5.2  Outputs"),
    make_table(
        [
            ["Step", "Task", "Output"],
            ["1", "persist_df",
             "<b>wildlife_events_recorded.csv</b> — cleaned incident records."],
            ["2", "make_wildlife_summary_table",
             "ecoscope_workflows_ext_mnc custom task. Pivots events by type "
             "with readable labels (fire_rep→Fire, snare_rep→Snare, "
             "wildlife_carcass_rep→Wildlife carcass, "
             "wildlife_injury_rep→Injured wildlife, "
             "wildlife_treatment_rep→Veterinary treatment; max_unique: 6, "
             "shorten_width: 300)."],
            ["3", "persist_df",
             "<b>wildlife_incidents_summary_table.csv</b> — pivoted incident summary."],
            ["4", "summarize_df",
             "Group by <b>date</b>; nunique id → <b>no_of_events</b>. reset_index: true."],
            ["5", "persist_df",
             "<b>wildlife_incidents_recorded_by_date.csv</b> — daily incident count "
             "(no totals row is appended in the current spec)."],
        ],
        [1.2*cm, 3.5*cm, W - 4.7*cm],
    ),
    sp(6),
    h2("5.3  Incident map"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "ecoscope_workflows_ext_custom.tasks.transformation.drop_null_geometry",
             "Drop rows with null geometry."],
            ["2", "apply_color_map",
             "Colour points by <b>event_type</b> using <b>tab10</b> → column <b>colors</b>."],
            ["3", "map_column_value",
             "Map event_type → event_type_mapped with readable labels "
             "(default: Undefined, keep_unmapped: false)."],
            ["4", "ecoscope_workflows_ext_custom.tasks.results.create_scatterplot_layer",
             "Render points: get_radius: 3, opacity: 0.55. "
             "Legend title: 'Wildlife Incidents', sorted ascending."],
            ["5", "ecoscope_workflows_ext_ste.tasks.spatial_operations.combine_deckgl_map_layers",
             "Static layers: parcels + conservancy boundary."],
            ["6", "ecoscope_workflows_ext_big_life.tasks.results.draw_map",
             "max_zoom: 10, legend placement: bottom-right, "
             "view_state: shared gdf_image_extent."],
            ["7", "persist_text",
             "Save as <b>wildlife_incidents_map.html</b>."],
            ["8", "create_map_widget_single_view",
             "“Wildlife Incident Map” dashboard widget "
             "(skipif: [never] — always runs, see Section 8.1)."],
        ],
        [1.2*cm, 6*cm, W - 7.2*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. BRANCH 2 — ELEPHANT SIGHTINGS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Branch 2 — Elephant Sightings"),
    hr(),
    p("Filters <b>elephant_sighting_rep</b> events and produces a "
      "herd-composition point map, a herd-size bar chart, a herd-size bubble "
      "map, and a herd-type summary table."),
    sp(6),
    h2("6.1  Column mapping"),
    p("Task: <b>map_columns</b> (raise_if_not_found: false). "
      "Dropped: index, time, event_type, event_category, reported_by, "
      "serial_number, event_type_display, Comments. Renamed:"),
    make_table(
        [
            ["Source column (title after prefix drop)", "Renamed to"],
            ["Female",           "female"],
            ["Herd Demographic", "herd_composition"],
            ["Herd size",        "herd_size"],
            ["Male",             "male"],
            ["Subadult",         "sub_adult"],
            ["< 1 year",         "underayear"],
        ],
        [7*cm, W - 7*cm],
    ),
    sp(6),
    h2("6.2  Cleaning and value mapping"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fill_missing_values",
             "Fill nulls in <b>herd_composition</b> with <b>Undefined</b>."],
            ["2", "fill_missing_values",
             "Fill nulls in underayear, female, male, herd_size, sub_adult with 0."],
            ["3", "convert_columns_to_int",
             "Cast underayear, female, male, herd_size, sub_adult to integer "
             "(errors: coerce, fill_value: 0)."],
            ["4", "map_column_value",
             "Standardise herd_composition → herd_composition_mapped: "
             "bachelor→Bachelor, femalecalf→Female + Calf, mixed→Mixed, "
             "Undefined/Unspecified→Unspecified (default: Undefined, "
             "keep_unmapped: false)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("6.3  Herd-size bar chart"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "apply_classification",
             "Bin <b>herd_size</b> into <b>5</b> equal-interval bins "
             "(scheme: equal_interval, k: 5, label_ranges: true) "
             "→ column <b>herd_size_bins</b>."],
            ["2", "order_categorical_by_number",
             "Order herd_size_bins as a sortable category."],
            ["3", "ecoscope_workflows_ext_wwf_virunga.tasks.plot.draw_bar_chart",
             "Bar chart: category = herd_size_bins; count of id; "
             "marker_color: #6495ed; axis titles 'Group size' / "
             "'Number of records'; bargap/bargroupgap: 0.05."],
            ["4", "persist_text",
             "Save as <b>elephant_herd_size_bar_chart.html</b>."],
            ["5", "create_plot_widget_single_view",
             "“Elephant Herd Size Distribution” dashboard widget."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("6.4  Herd-size bubble map"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "ecoscope_workflows_ext_custom.tasks.transformation.drop_null_geometry",
             "Drop rows with null geometry from the ordered/binned table."],
            ["2", "ecoscope_workflows_ext_big_life.tasks.results.create_clustered_labeled_scatterplot_layer",
             "Clustered bubble layer: get_value/get_radius = herd_size, "
             "aggregate: true, cluster_max_radius: 40, fixed colour "
             "[0,191,255] (deep sky blue), white text labels."],
            ["3", "combine_deckgl_map_layers + draw_map",
             "Static layers: parcels + conservancy boundary. "
             "Legend title: 'Herd Size'."],
            ["4", "persist_text",
             "Save as <b>elephant_herd_types_map.html</b>."],
            ["5", "create_map_widget_single_view",
             "“Elephant Herd Size Map” dashboard widget."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("6.5  Herd-composition point map"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "apply_color_map",
             "Colour by <b>herd_composition</b> using <b>tab10</b> "
             "→ column herd_composition_colors."],
            ["2", "create_scatterplot_layer",
             "get_radius: 3, opacity: 0.55. Legend title: 'Herd Types'."],
            ["3", "combine_deckgl_map_layers + draw_map",
             "Static layers: parcels + conservancy boundary."],
            ["4", "persist_text",
             "Save as <b>elephant_sightings_events.html</b>."],
            ["5", "create_map_widget_single_view",
             "“Elephant Herd Composition Map” dashboard widget."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("6.6  Herd-type summary table"),
    p("Task: <b>summarize_df</b> grouped by <b>herd_composition_mapped</b>, "
      "nunique id → observations. Renamed to 'Herd Type' via map_columns, "
      "persisted as <b>overall_elephant_summary_table.csv</b>, rendered with "
      "draw_table (sorting/filtering enabled, download disabled), and wrapped "
      "as the “Elephant Herd Composition Summary” table widget."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. BRANCH 3 — BUFFALO SIGHTINGS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Branch 3 — Buffalo Sightings"),
    hr(),
    p("Filters <b>buffalo_sighting_rep</b> events. The pipeline mirrors the "
      "elephant branch exactly (Section 6) — column mapping, cleaning, "
      "herd-size binning, bar chart, bubble map, composition map, and summary "
      "table — with one structural difference: buffalo events carry no "
      "female/male/sub-adult/under-a-year demographic breakdown, only "
      "<b>herd_composition</b> and <b>herd_size</b>."),
    sp(6),
    h2("7.1  Column mapping"),
    make_table(
        [
            ["Source column", "Renamed to"],
            ["Herd Demographic", "herd_composition"],
            ["Herd Size",        "herd_size"],
        ],
        [7*cm, W - 7*cm],
    ),
    note("Dropped columns: index, time, event_type, event_category, "
         "reported_by, serial_number, event_type_display, Comment "
         "(singular — 'Comment', not 'Comments' as in the elephant branch)."),
    sp(6),
    h2("7.2  Outputs"),
    make_table(
        [
            ["Output", "Description"],
            ["buffalo_sightings_events.html",     "Buffalo locations coloured by herd_composition (tab10)"],
            ["buffalo_herd_size_bar_chart.html",  "Bar chart of buffalo herd size bins (equal_interval, k=5)"],
            ["buffalo_herd_types_map.html",       "Clustered bubble map of buffalo herd sizes"],
            ["overall_buffalo_summary_table.csv", "Sighting counts by herd type"],
        ],
        [6*cm, W - 6*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. BRANCH 4 — LION SIGHTINGS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Branch 4 — Lion Sightings"),
    hr(),
    p("Filters <b>lion_sighting_rep</b> events and produces a pride-coloured "
      "point map and a pride summary table."),
    sp(6),
    h2("8.1  Column mapping"),
    p("Task: <b>map_columns</b> (raise_if_not_found: false). "
      "Dropped: index, time, event_type, event_category, reported_by, "
      "serial_number, event_type_display, Comment, Behavior. Renamed:"),
    make_table(
        [
            ["Source column", "Renamed to"],
            ["Female",              "female"],
            ["Male",                "male"],
            ["Group Size",          "group_size"],
            ["Individuals Present", "individuals_present"],
            ["Pride",               "pride"],
            ["Young",               "young"],
        ],
        [7*cm, W - 7*cm],
    ),
    sp(6),
    h2("8.2  Cleaning and value mapping"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fill_missing_values",
             "Fill nulls in <b>pride</b> with <b>Undefined</b>."],
            ["2", "map_column_value",
             "Map pride → mapped_pride: Undefined→Undefined, "
             "'Other (specify in comments)'→Undefined, Unknown→Undefined "
             "(default: Undefined, <b>keep_unmapped: true</b> — named prides "
             "pass through unchanged)."],
            ["3", "apply_color_map",
             "Colour by <b>mapped_pride</b> using <b>tab10</b> → column colors."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("8.3  Outputs"),
    make_table(
        [
            ["Output", "Description"],
            ["lion_pride_sightings_map.html", "Lion locations coloured by mapped_pride (tab10)"],
            ["overall_lion_summary_table.csv","Sighting counts grouped by pride, renamed to 'Pride'"],
        ],
        [6*cm, W - 6*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. BRANCH 5 — LEOPARD SIGHTINGS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Branch 5 — Leopard Sightings"),
    hr(),
    p("Filters <b>leopardsightingrep</b> events (note: no underscore between "
      "'leopard' and 'sighting' in the raw event type string). Structurally "
      "identical to the lion branch, but keyed on individuals present rather "
      "than pride."),
    sp(6),
    h2("9.1  Column mapping"),
    p("Task: <b>map_columns</b> (raise_if_not_found: false). "
      "Dropped: index, time, event_type, event_category, reported_by, "
      "serial_number, event_type_display, Comment, Behavior. Renamed: "
      "Female→female, Male→male, Group Size→group_size, "
      "Individuals Present→individuals_present, Young→young. "
      "(No Pride field for leopard.)"),
    sp(6),
    h2("9.2  Cleaning and value mapping"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fill_missing_values",
             "Fill nulls in <b>individuals_present</b> with <b>Undefined</b>."],
            ["2", "map_column_value",
             "Map individuals_present → individuals_present_mapped: "
             "Undefined→Undefined, 'Other (specify in comments)'→Undefined, "
             "Unknown→Undefined (keep_unmapped: true)."],
            ["3", "apply_color_map",
             "Colour by <b>individuals_present_mapped</b> using <b>tab10</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("9.3  Outputs"),
    make_table(
        [
            ["Output", "Description"],
            ["leopard_sightings_map.html",
             "Leopard locations coloured by individuals_present_mapped. "
             "Legend title: 'Individuals'."],
            ["overall_leopard_summary_table.csv",
             "Sighting counts grouped by individuals_present, renamed to 'Individuals'"],
        ],
        [6*cm, W - 6*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. BRANCH 6 — CHEETAH SIGHTINGS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Branch 6 — Cheetah Sightings"),
    hr(),
    p("Filters <b>cheetah_sighting_rep</b> events. The pipeline is identical "
      "to the leopard branch (Section 9) — same column mapping, same "
      "cleaning, same value mapping on <b>individuals_present</b>."),
    sp(6),
    h2("10.1  Outputs"),
    make_table(
        [
            ["Output", "Description"],
            ["cheetah_sightings_map.html",
             "Cheetah locations coloured by individuals_present_mapped. "
             "Legend title: 'Individuals'."],
            ["overall_cheetah_summary_table.csv",
             "Sighting counts grouped by individuals_present, renamed to 'Individuals'"],
        ],
        [6*cm, W - 6*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 11. BRANCHES 7–9 — GIRAFFE, HARTEBEEST, RHINO
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("11. Branches 7–9 — Giraffe, Hartebeest, Rhino"),
    hr(),
    p("These three branches are the simplest in the workflow: after the "
      "common normalisation pattern (Section 4.4) there is no map_columns "
      "step, no value mapping, and no herd-size logic — just a fixed-colour "
      "point map and a daily-count summary table."),
    sp(6),
    h2("11.1  Filters and map colour"),
    make_table(
        [
            ["Branch", "event_type value", "Map file", "Point colour"],
            ["Giraffe",    "giraffe_sighting",    "giraffe_sightings_map.html",    "[72, 61, 139] dark slate blue"],
            ["Hartebeest", "hartebeest_sighting",  "hartebeest_sightings_map.html", "[72, 61, 139] dark slate blue"],
            ["Rhino",      "rhino_sighting_rep",   "rhino_sightings_map.html",      "[72, 61, 139] dark slate blue"],
        ],
        [3*cm, 4*cm, 4.5*cm, W - 11.5*cm],
    ),
    p("Each map: <b>drop_null_geometry</b> → <b>create_scatterplot_layer</b> "
      "(get_radius: 3, opacity: 0.55, single fixed legend entry 'Sighting') "
      "→ <b>combine_deckgl_map_layers</b> (parcels + conservancy boundary) → "
      "<b>draw_map</b> → <b>persist_text</b> → <b>create_map_widget_single_view</b>."),
    sp(6),
    h2("11.2  Daily-count summary tables"),
    make_table(
        [
            ["Branch", "Output CSV", "Widget"],
            ["Giraffe",    "overall_giraffe_summary_table.csv", "Giraffe Sightings Summary"],
            ["Hartebeest", "overall_hart_summary_table.csv",    "Hartebeest Sightings Summary"],
            ["Rhino",      "overall_rhino_summary_table.csv",   "Rhino Sightings Summary"],
        ],
        [3*cm, 6*cm, W - 9*cm],
    ),
    note("Each table is produced by summarize_df grouped by <b>date</b> "
         "(nunique id → observations), persisted as CSV, rendered with "
         "draw_table, and wrapped as a table widget — the same pattern used "
         "for the herd-type summaries in Sections 6 and 7, but grouped by "
         "date instead of a category column. No totals row is appended."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 12. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("12. Output Files"),
    hr(),
    p("All outputs are written to <b>ECOSCOPE_WORKFLOWS_RESULTS</b>."),
    h2("12.1  CSV tables"),
    make_table(
        [
            ["File", "Branch", "Description"],
            ["wildlife_events.csv",                     "All",
             "Raw dump of all 13 fetched event types, pre-branching"],
            ["wildlife_events_recorded.csv",             "Wildlife incidents",
             "Cleaned incident records"],
            ["wildlife_incidents_summary_table.csv",     "Wildlife incidents",
             "Pivoted incident summary by type"],
            ["wildlife_incidents_recorded_by_date.csv",  "Wildlife incidents",
             "Daily unique incident count"],
            ["overall_elephant_summary_table.csv",       "Elephant",
             "Sighting counts by herd type"],
            ["overall_buffalo_summary_table.csv",        "Buffalo",
             "Sighting counts by herd type"],
            ["overall_lion_summary_table.csv",           "Lion",
             "Sighting counts by pride"],
            ["overall_leopard_summary_table.csv",        "Leopard",
             "Sighting counts by individuals present"],
            ["overall_cheetah_summary_table.csv",        "Cheetah",
             "Sighting counts by individuals present"],
            ["overall_giraffe_summary_table.csv",        "Giraffe",
             "Daily unique sighting count"],
            ["overall_hart_summary_table.csv",           "Hartebeest",
             "Daily unique sighting count"],
            ["overall_rhino_summary_table.csv",          "Rhino",
             "Daily unique sighting count"],
        ],
        [6*cm, 2.5*cm, W - 8.5*cm],
    ),
    sp(6),
    h2("12.2  Maps and charts"),
    make_table(
        [
            ["File", "Branch", "Coloured by"],
            ["wildlife_incidents_map.html",     "Wildlife incidents", "event_type_mapped"],
            ["elephant_sightings_events.html",  "Elephant", "herd_composition"],
            ["elephant_herd_size_bar_chart.html","Elephant", "herd_size_bins (bar chart)"],
            ["elephant_herd_types_map.html",     "Elephant", "fixed colour, bubble size = herd_size"],
            ["buffalo_sightings_events.html",   "Buffalo",  "herd_composition"],
            ["buffalo_herd_size_bar_chart.html","Buffalo",  "herd_size_bins (bar chart)"],
            ["buffalo_herd_types_map.html",      "Buffalo",  "fixed colour, bubble size = herd_size"],
            ["lion_pride_sightings_map.html",   "Lion",     "mapped_pride"],
            ["leopard_sightings_map.html",      "Leopard",  "individuals_present_mapped"],
            ["cheetah_sightings_map.html",      "Cheetah",  "individuals_present_mapped"],
            ["giraffe_sightings_map.html",      "Giraffe",  "fixed colour"],
            ["hartebeest_sightings_map.html",   "Hartebeest","fixed colour"],
            ["rhino_sightings_map.html",        "Rhino",    "fixed colour"],
        ],
        [6*cm, 2.5*cm, W - 8.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 13. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("13. Workflow Execution Logic"),
    hr(),
    h2("13.1  Global skip conditions and widget-creation override"),
    p("This workflow defines a single <b>task-instance-defaults</b> block "
      "applying <b>any_is_empty_df</b> and <b>any_dependency_skipped</b> as "
      "skipif conditions to every task by default. Every "
      "<b>create_map_widget_single_view</b>, <b>create_plot_widget_single_view</b>, "
      "and <b>create_table_widget_single_view</b> task explicitly overrides "
      "this with <b>skipif: conditions: [never]</b> — these widget-wrapper "
      "tasks always run, regardless of whether their upstream map, chart, or "
      "table was skipped."),
    note("This means every one of the 21 entries in the dashboard's widgets "
         "list is always populated, even for a branch whose underlying event "
         "data was empty for the run — the widget-creation task itself never "
         "skips, only the data-producing tasks feeding it do."),
    sp(6),
    h2("13.2  Nine independent branches"),
    make_table(
        [
            ["Branch", "Event type(s)", "CSV outputs", "HTML outputs"],
            ["Wildlife incidents", "snare_rep, fire_rep, wildlife_injury_rep, "
             "wildlife_treatment_rep, wildlife_carcass_rep", "3", "1 map"],
            ["Elephant",   "elephant_sighting_rep",  "1", "3 (map + bar chart + bubble map)"],
            ["Buffalo",    "buffalo_sighting_rep",   "1", "3 (map + bar chart + bubble map)"],
            ["Lion",       "lion_sighting_rep",      "1", "1 map"],
            ["Leopard",    "leopardsightingrep",     "1", "1 map"],
            ["Cheetah",    "cheetah_sighting_rep",   "1", "1 map"],
            ["Giraffe",    "giraffe_sighting",       "1", "1 map"],
            ["Hartebeest", "hartebeest_sighting",    "1", "1 map"],
            ["Rhino",      "rhino_sighting_rep",     "1", "1 map"],
        ],
        [3.2*cm, 5*cm, 1.8*cm, W - 10*cm],
    ),
    sp(6),
    h2("13.3  No PNG rendering"),
    p("Unlike earlier versions of this workflow, the current spec contains "
      "no html_to_png steps anywhere. Every map, bar chart, and summary "
      "table is persisted as HTML only (via persist_text or persist_df + "
      "draw_table + persist_text), and consumed directly by the dashboard "
      "widgets — nothing is rasterised to a static image."),
    sp(6),
    h2("13.4  Dashboard"),
    p("The workflow concludes with <b>gather_dashboard</b> (step name "
      "“MNC event report dashboard”, id: mnc_events_dashboard), "
      "which packages workflow details, time range, groupers, and a "
      "<b>widgets</b> list of all <b>21</b> map/chart/table widgets produced "
      "across the nine branches — one map widget per branch, plus a chart "
      "widget and table widget for elephant/buffalo, and a table widget for "
      "every other species branch. The wildlife incidents branch is the only "
      "one whose CSV summaries (pivoted-by-type and by-date) are not wrapped "
      "as table widgets."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 14. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("14. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned in spec.yaml"],
            ["ecoscope-platform",                 ">=2.15.0, <2.16.0"],
            ["ecoscope-workflows-ext-custom",     "0.1.0rc14.*"],
            ["ecoscope-workflows-ext-ste",        "0.0.0rc1.*"],
            ["ecoscope-workflows-ext-wwf-virunga","0.0.0rc9.*"],
            ["ecoscope-workflows-ext-big-life",   "1.0.1.*"],
            ["ecoscope-workflows-ext-mnc",        "1.0.1.*"],
            ["pydeck",                             "0.9.2"],
            ["opentelemetry-sdk",                  ">=1.20.0, <2.0.0"],
        ],
        [7*cm, W - 7*cm],
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF written → {OUTPUT_FILE}")
