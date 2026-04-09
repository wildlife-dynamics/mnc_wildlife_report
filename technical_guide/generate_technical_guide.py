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
    p("Wildlife sightings and incident reporting across MNC conservancy zones", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>mnc_wildlife_report</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>mnc_wildlife_report</b> workflow fetches wildlife sighting and "
      "incident events from EarthRanger for a specified time window and routes "
      "them into nine independent reporting branches — one per species group "
      "(elephant, buffalo, rhino, lion, leopard, cheetah, giraffe, hartebeest) "
      "and one for wildlife incidents (snares, fires, carcasses, injuries, "
      "veterinary treatments). In parallel, the workflow downloads MNC "
      "conservancy boundary and parcels geospatial files from Dropbox to use "
      "as base layers on all maps."),
    sp(4),
    p("The workflow delivers:"),
    bullet("<b>11 CSV tables</b> — daily event counts with totals rows for "
           "each species, individual identity summaries for leopard and cheetah, "
           "and raw/summarised wildlife incident records"),
    bullet("<b>13 maps (HTML + PNG)</b> — herd-composition point maps for all "
           "species, herd-size bubble maps and bar charts for elephant and "
           "buffalo, and an incident type map"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output", "Type", "Branch"],
            ["total_elephants_events_recorded.csv",    "CSV", "Elephant"],
            ["elephant_sightings_events.html / .png",  "Map", "Elephant — herd composition"],
            ["elephant_herd_size_bar_chart.html / .png","Chart","Elephant — herd size bins"],
            ["elephant_herd_types_map.html / .png",    "Map", "Elephant — herd size bubbles"],
            ["total_buffalo_events_recorded.csv",      "CSV", "Buffalo"],
            ["buffalo_sightings_events.html / .png",   "Map", "Buffalo — herd composition"],
            ["buffalo_herd_size_bar_chart.html / .png","Chart","Buffalo — herd size bins"],
            ["buffalo_herd_types_map.html / .png",     "Map", "Buffalo — herd size bubbles"],
            ["total_rhino_events_recorded.csv",        "CSV", "Rhino"],
            ["rhino_sightings_events.html / .png",     "Map", "Rhino sightings"],
            ["total_lion_events_recorded.csv",         "CSV", "Lion"],
            ["lion_sightings_events.html / .png",      "Map", "Lion — by pride"],
            ["total_leopard_events_recorded.csv",      "CSV", "Leopard"],
            ["individual_leopard_summary.csv",         "CSV", "Leopard — by individual"],
            ["leopard_sightings_events.html / .png",   "Map", "Leopard — by individual"],
            ["total_cheetah_events_recorded.csv",      "CSV", "Cheetah"],
            ["individual_cheetah_summary.csv",         "CSV", "Cheetah — by individual"],
            ["giraffe_sightings_events.html / .png",   "Map", "Giraffe sightings"],
            ["hartebeest_sightings_events.html / .png","Map", "Hartebeest sightings"],
            ["wildlife_events_recorded.csv",           "CSV", "Wildlife incidents — raw"],
            ["wildlife_incidents_summary_table.csv",   "CSV", "Wildlife incidents — pivoted"],
            ["wildlife_incidents_recorded_by_date.csv","CSV", "Wildlife incidents — by date"],
            ["wildlife_incidents_map.html / .png",     "Map", "Wildlife incidents — by type"],
        ],
        [7*cm, 1.8*cm, W - 8.8*cm],
    ),
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
            ["ecoscope-workflows-core",        "0.22.18.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-ecoscope","0.22.18.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",  "0.0.43.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",     "0.0.18.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",     "0.0.8.*",   "ecoscope-workflows-custom"],
        ],
        [6.5*cm, 3*cm, W - 9.5*cm],
    ),
    sp(6),
    h2("2.2  Connections and external assets"),
    make_table(
        [
            ["Asset", "Task / Source", "Purpose"],
            ["EarthRanger", "set_er_connection",
             "Fetch event records and resolve event detail display titles "
             "via process_events_details (used by all species branches)"],
            ["mnc_conservancy.gpkg", "fetch_and_persist_file (Dropbox)",
             "MNC community conservancy boundaries split by grazing_zone. "
             "Used to generate conservancy boundary and text label layers."],
            ["mnc_across_the_river_parcels.gpkg", "fetch_and_persist_file (Dropbox)",
             "MNC across-the-river land parcels. "
             "Used as a polygon layer on all maps."],
        ],
        [3.5*cm, 4*cm, W - 7.5*cm],
    ),
    note("Both Dropbox files are downloaded with overwrite_existing: false and "
         "retries: 3. If the files already exist from a previous run the "
         "download step is skipped."),
    sp(6),
    h2("2.3  Grouper"),
    p("The workflow uses an <b>empty grouper list</b> (groupers: []). "
      "All records are processed as a single undivided dataset. "
      "The grouper is passed to the temporal index and the dashboard only."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. GEOSPATIAL ASSET PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Geospatial Asset Pipeline"),
    hr(),
    p("Before any event data is fetched, the workflow downloads and prepares "
      "all geospatial base layers. The same layers appear on every map "
      "produced by the workflow."),
    sp(6),
    h2("3.1  Conservancy boundary pipeline"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fetch_and_persist_file",
             "Download <b>mnc_conservancy.gpkg</b> from Dropbox."],
            ["2", "load_df",
             "Load into a GeoDataFrame (layer: null, deserialize_json: false)."],
            ["3", "split_gdf_by_column",
             "Split by <b>grazing_zone</b> column into a dict keyed by zone name "
             "(Conservancy, Conservancy Herd Zone, Grazing Zone 1–4)."],
            ["4", "annotate_gdf_dict_with_geom_type",
             "Attach geometry-type metadata to each GDF in the dict."],
            ["5", "create_deckgl_layers_from_gdf_dict (×2)",
             "<b>create_mnc_styled_layers</b> — styled layers for all 6 zone types "
             "(defined but not used in any map in this workflow). "
             "<b>create_conservancy_boundaries</b> — conservancy outline only "
             "(grey, opacity 0.95, no fill). Used on all species and incident maps."],
            ["6", "create_gdf_from_dict",
             "Extract the <b>Conservancy</b> key → conservancy_gdf "
             "(used for text labels)."],
            ["7", "filter_df",
             "Filter load_comm_shp to rows where grazing_zone != 'Conservancy' "
             "→ overall_grazing_zones. Used to compute the global map view state."],
            ["8", "create_custom_text_layer",
             "Render conservancy name labels from the <b>name</b> field at polygon "
             "centroids (Calibri bold 700, size 1500 m, billboard: true)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("3.2  Parcels pipeline"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "fetch_and_persist_file",
             "Download <b>mnc_across_the_river_parcels.gpkg</b> from Dropbox."],
            ["2", "load_df",
             "Load into a GeoDataFrame."],
            ["3", "get_gdf_geom_type",
             "Detect and attach geometry type."],
            ["4", "create_deckgl_layer_from_gdf",
             "Render as filled polygons: dark khaki (#bdb76b), opacity 0.15. "
             "Legend: 'Parcels'."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("3.3  Global map view state"),
    p("Task: <b>view_state_deck_gdf</b>. Computes map centre and zoom from "
      "<b>overall_grazing_zones</b> (pitch: 0, bearing: 0). "
      "This computed view state is shared by all maps (max_zoom: 15 per map)."),
    note("All maps in this workflow use the same three static base layers: "
         "create_conservancy_boundaries + create_mnc_parcels_layers + "
         "conservancy_text_layer. The create_mnc_styled_layers layer set "
         "(grazing zones with colours) is defined in the spec but is not "
         "referenced by any map."),
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
        ],
        [5*cm, W - 5*cm],
    ),
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
             "Produces <b>events_temporal</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("4.3  Branch filters"),
    p("Each branch begins by filtering events_temporal to its event type. "
      "Species branches use <b>filter_df</b> (op: equal, reset_index: true). "
      "The wildlife incidents branch uses <b>filter_row_values</b> "
      "(column: event_type, values list) to capture five event types at once."),
    make_table(
        [
            ["Branch", "Filter task", "event_type value(s)"],
            ["Elephant",    "filter_df",        "elephant_sighting_rep"],
            ["Buffalo",     "filter_df",        "buffalo_sighting_rep"],
            ["Rhino",       "filter_df",        "rhino_sighting_rep"],
            ["Lion",        "filter_df",        "lion_sighting_rep"],
            ["Leopard",     "filter_df",        "leopardsightingrep"],
            ["Cheetah",     "filter_df",        "cheetah_sighting_rep"],
            ["Giraffe",     "filter_df",        "giraffe_sighting"],
            ["Hartebeest",  "filter_df",        "hartebeest_sighting"],
            ["Wildlife incidents", "filter_row_values",
             "snare_rep, fire_rep, wildlife_injury_rep, "
             "wildlife_treatment_rep, wildlife_carcass_rep"],
        ],
        [3.5*cm, 3.5*cm, W - 7*cm],
    ),
    sp(6),
    h2("4.4  Common species normalisation pattern"),
    p("Every species branch (except rhino, giraffe, hartebeest and wildlife "
      "incidents — see per-branch notes) runs the same four steps after "
      "filtering:"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "process_events_details",
             "Resolve event detail field IDs to display titles "
             "(map_to_titles: true, ordered: true). Requires the ER client."],
            ["2", "normalize_json_column",
             "Flatten the <b>event_details</b> JSON column "
             "(skip_if_not_exists: true, sort_columns: true)."],
            ["3", "drop_column_prefix",
             "Remove the <b>event_details__</b> prefix from all flattened "
             "columns (duplicate_strategy: keep_original)."],
            ["4", "map_columns",
             "Drop housekeeping columns, retain relevant fields, and rename "
             "to snake_case. Parameters vary per branch."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. BRANCH 1 — ELEPHANT SIGHTINGS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Branch 1 — Elephant Sightings"),
    hr(),
    p("Filters <b>elephant_sighting_rep</b> events and produces a daily "
      "count table, a herd-composition point map, a herd-size bar chart, "
      "and a herd-size bubble map."),
    sp(6),
    h2("5.1  Column mapping"),
    p("Task: <b>map_columns</b> (raise_if_not_found: true). "
      "Dropped: index, time, event_category, reported_by, serial_number, Comments. "
      "Renamed:"),
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
    h2("5.2  Cleaning and value mapping"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "replace_missing_with_label",
             "Fill nulls in <b>herd_composition</b> with <b>'Unspecified'</b>."],
            ["2", "convert_to_int",
             "Cast herd_size, female, male, sub_adult, underayear to integer "
             "(errors: coerce, fill_value: 0)."],
            ["3", "map_column_values",
             "Standardise herd_composition labels: "
             "bachelor→Bachelor, femalecalf→Female/Calf, "
             "mixed→Mixed, unspecified→Unspecified (inplace: true)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("5.3  Daily count table"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "summarize_df",
             "Group by <b>date</b>; count unique events as <b>no_of_events</b> "
             "(aggregator: nunique, column: id). reset_index: true."],
            ["2", "add_totals_row",
             "Append a <b>Total</b> row (label_col: date)."],
            ["3", "persist_df",
             "Save as <b>total_elephants_events_recorded.csv</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("5.4  Herd-composition point map"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "exclude_geom_outliers",  "Remove spatial outliers (z_threshold: 3)."],
            ["2", "drop_null_geometry",     "Drop rows with null geometry."],
            ["3", "apply_color_map",
             "Colour points by <b>herd_composition</b> using <b>tab20</b> "
             "→ output column <b>colors</b>."],
            ["4", "create_scatterplot_layer",
             "Render points: get_radius: 4, opacity: 0.75. "
             "Legend title: 'Herd Types', label from herd_composition."],
            ["5", "combine_deckgl_map_layers",
             "Static layers: conservancy_boundaries + parcels + text labels. "
             "Grouped: elephant composition layer."],
            ["6", "draw_map",
             "max_zoom: 15, legend: bottom-right, view_state: global_zoom_value."],
            ["7", "persist_text + html_to_png",
             "Save as <b>elephant_sightings_events.html / .png</b> "
             "(device_scale_factor: 2.0, wait: 40 s)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("5.5  Herd-size bar chart"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "bin_columns",
             "Bin <b>herd_size</b> into 7 equal-width bins "
             "(suffix: 'bins', inplace: false) → column <b>herd_sizebins</b>."],
            ["2", "categorize_bins",
             "Convert bin intervals to sortable category labels "
             "(col: herd_sizebins) → adds <b>herd_sizebins_sort</b>."],
            ["3", "draw_bar_chart",
             "Bar chart: category = herd_sizebins; agg_func = count on id; "
             "marker_color = lightsteelblue; axis labels: Group size / Number of records."],
            ["4", "persist_text + html_to_png",
             "Save as <b>elephant_herd_size_bar_chart.html / .png</b> "
             "(wait_for_timeout: 10 ms — chart renders immediately)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("5.6  Herd-size bubble map"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "drop_null_values",
             "Drop rows where <b>herd_sizebins_sort</b> is null."],
            ["2", "exclude_geom_outliers", "Remove spatial outliers (z_threshold: 3)."],
            ["3", "drop_null_geometry",    "Drop rows with null geometry."],
            ["4", "clean_dataframe_index",
             "Reset index, drop index column, rename any unnamed columns to 'idx'."],
            ["5", "apply_color_map",
             "Colour points by <b>herd_sizebins_sort</b> using <b>Blues</b> "
             "colormap → output column <b>colors</b>."],
            ["6", "create_scatterplot_layer",
             "Bubble map: get_radius = herd_size (actual count), "
             "radius_units: pixels, radius_scale: 0.43. "
             "Legend title: 'Group Sizes', sorted ascending."],
            ["7", "combine_deckgl_map_layers",
             "Static layers: conservancy_boundaries + parcels + text labels. "
             "Grouped: elephant herd-size layer."],
            ["8", "draw_map + persist_text + html_to_png",
             "Save as <b>elephant_herd_types_map.html / .png</b> "
             "(wait: 40 s, max_zoom: 15)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. BRANCH 2 — BUFFALO SIGHTINGS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Branch 2 — Buffalo Sightings"),
    hr(),
    p("Filters <b>buffalo_sighting_rep</b> events. The pipeline is identical "
      "to the elephant branch in structure (daily count, herd-composition map, "
      "herd-size bar chart, herd-size bubble map) with the following "
      "column-level differences:"),
    sp(6),
    h2("6.1  Column mapping differences from elephant"),
    make_table(
        [
            ["Column", "Elephant", "Buffalo"],
            ["Herd size column title", "'Herd size' (lowercase s)", "'Herd Size' (capital S)"],
            ["Sex breakdowns", "female, male, sub_adult, underayear renamed and cast to int",
             "Sex breakdown columns commented out in spec — only herd_size is cast to int"],
            ["Drop list", "Includes 'Comments'", "Does not include Comments"],
        ],
        [3.5*cm, 4*cm, W - 7.5*cm],
    ),
    sp(6),
    h2("6.2  Outputs"),
    make_table(
        [
            ["Output", "Description"],
            ["total_buffalo_events_recorded.csv",      "Daily unique buffalo sighting count + Total row"],
            ["buffalo_sightings_events.html / .png",   "Buffalo locations coloured by herd_composition"],
            ["buffalo_herd_size_bar_chart.html / .png","Bar chart of buffalo herd size bins"],
            ["buffalo_herd_types_map.html / .png",     "Bubble map of buffalo herd sizes (Blues colormap)"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. BRANCH 3 — RHINO SIGHTINGS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Branch 3 — Rhino Sightings"),
    hr(),
    p("Filters <b>rhino_sighting_rep</b> events. This branch is simpler than "
      "elephant and buffalo — there is no map_columns step. The workflow reads "
      "directly from <b>drop_rhino_prefix</b> for both the summary table and "
      "the map."),
    sp(6),
    h2("7.1  Daily count table"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "summarize_df",
             "Group by <b>date</b>; nunique id → <b>no_of_events</b>. reset_index: true."],
            ["2", "add_totals_row", "Append a Total row."],
            ["3", "persist_df", "Save as <b>total_rhino_events_recorded.csv</b>."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("7.2  Sightings map"),
    p("Points are coloured by <b>event_type</b> (tab20 colormap). "
      "Legend title: 'Rhino Sightings'. "
      "Base layers: conservancy_boundaries + parcels + text labels. "
      "Saved as <b>rhino_sightings_events.html / .png</b>."),
    note("Because there is no map_columns step, all event columns from the "
         "prefix-drop output are carried through to the map, including "
         "housekeeping columns such as event_category and reported_by."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. BRANCH 4 — LION SIGHTINGS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Branch 4 — Lion Sightings"),
    hr(),
    p("Filters <b>lion_sighting_rep</b> events and produces a daily count "
      "table and a pride-based sighting map."),
    sp(6),
    h2("8.1  Column mapping"),
    p("Task: <b>map_columns</b> (raise_if_not_found: true). "
      "Dropped: index, time, event_category, reported_by, serial_number, "
      "Comment, Behavior. Renamed:"),
    make_table(
        [
            ["Source column", "Renamed to"],
            ["Female",              "female"],
            ["Group Size",          "group_size"],
            ["Individuals Present", "individuals_present"],
            ["Male",                "male"],
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
            ["1", "replace_missing_with_label",
             "Fill nulls in <b>pride</b> with <b>'Unspecified'</b>."],
            ["2", "convert_to_int",
             "Cast young, female, male, group_size to integer "
             "(errors: coerce, fill_value: 0)."],
            ["3", "map_column_values",
             "Standardise pride labels: Unknown→Unknown, "
             "unspecified→Unknown, 'Other (specify in comments)'→Unknown."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("8.3  Outputs"),
    make_table(
        [
            ["Output", "Description"],
            ["total_lion_events_recorded.csv",   "Daily unique lion sighting count + Total row"],
            ["lion_sightings_events.html / .png", "Lion locations coloured by pride (tab20)"],
        ],
        [5.5*cm, W - 5.5*cm],
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
      "'leopard' and 'sighting' in the event type string). Produces a daily "
      "count table, an individual-leopard summary table, and a point map."),
    sp(6),
    h2("9.1  Column mapping"),
    p("Task: <b>map_columns</b> (raise_if_not_found: true). "
      "Dropped: index, time, event_category, reported_by, serial_number, "
      "Comment, Behavior. Renamed: Female→female, Group Size→group_size, "
      "Individuals Present→individuals_present, Male→male, Young→young. "
      "(No 'Pride' field for leopard.)"),
    sp(6),
    h2("9.2  Cleaning and value mapping"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "replace_missing_with_label",
             "Fill nulls in <b>individuals_present</b> with <b>'Unspecified'</b>."],
            ["2", "convert_to_int",
             "Cast young, female, male, group_size to integer."],
            ["3", "map_column_values",
             "Standardise individuals_present: Unknown→Unknown, "
             "Unspecified→Unknown, 'Other (specify in comments)'→Unknown."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("9.3  Outputs"),
    make_table(
        [
            ["Output", "Description"],
            ["total_leopard_events_recorded.csv",
             "Daily unique leopard sighting count (groupby: date, nunique id) + Total row"],
            ["individual_leopard_summary.csv",
             "Sighting count grouped by individuals_present "
             "(groupby: individuals_present, nunique id → no_of_events)"],
            ["leopard_sightings_events.html / .png",
             "Leopard locations coloured by individuals_present (tab20). "
             "Legend title: 'Individual'."],
        ],
        [5.5*cm, W - 5.5*cm],
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
      "to the leopard branch — same column mapping, same cleaning, same "
      "value mapping on <b>individuals_present</b>."),
    sp(6),
    h2("10.1  Outputs"),
    make_table(
        [
            ["Output", "Description"],
            ["total_cheetah_events_recorded.csv",
             "Daily unique cheetah sighting count + Total row"],
            ["individual_cheetah_summary.csv",
             "Sighting count grouped by individuals_present"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    sp(6),
    note("The spec contains a known bug: the persist_cheetah_urls step "
         "references <b>draw_leopard_map.return</b> instead of "
         "draw_cheetah_map.return, and saves to the filename "
         "<b>leopard_sightings_events.html</b>. As a result the cheetah map "
         "HTML/PNG output will duplicate the leopard map rather than rendering "
         "cheetah sighting locations."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 11. BRANCH 7 — GIRAFFE SIGHTINGS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("11. Branch 7 — Giraffe Sightings"),
    hr(),
    p("Filters <b>giraffe_sighting</b> events. This is a map-only branch — "
      "no CSV summary table is produced."),
    sp(6),
    h2("11.1  Column mapping"),
    p("Task: <b>map_columns</b> (raise_if_not_found: true). "
      "Dropped: index, time, event_category, reported_by, serial_number. "
      "No columns are renamed (rename_columns: {})."),
    sp(6),
    h2("11.2  Map"),
    p("Points are coloured by <b>event_type</b> (tab20). "
      "Legend title: 'Giraffe Sightings'. "
      "Base layers: conservancy_boundaries + parcels + text labels. "
      "Saved as <b>giraffe_sightings_events.html / .png</b>."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 12. BRANCH 8 — HARTEBEEST SIGHTINGS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("12. Branch 8 — Hartebeest Sightings"),
    hr(),
    p("Filters <b>hartebeest_sighting</b> events. Structure is identical "
      "to the giraffe branch — map-only, no CSV summary."),
    sp(6),
    h2("12.1  Column mapping"),
    p("Task: <b>map_columns</b> (raise_if_not_found: true). "
      "Dropped: index, time, event_category, reported_by, serial_number. "
      "No columns are renamed."),
    sp(6),
    h2("12.2  Map"),
    p("Points are coloured by <b>event_type</b> (tab20). "
      "Base layers: conservancy_boundaries + parcels + text labels. "
      "Saved as <b>hartebeest_sightings_events.html / .png</b>."),
    note("The hartebeest scatterplot layer has legend title 'Giraffe Sightings' "
         "in the spec — this is a copy-paste oversight in the spec and does not "
         "affect the data, only the map legend label."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 13. BRANCH 9 — WILDLIFE INCIDENTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("13. Branch 9 — Wildlife Incidents"),
    hr(),
    p("Captures five incident event types using <b>filter_row_values</b> and "
      "produces three CSV tables and a point map. Unlike the species branches, "
      "this branch does <b>not</b> use <b>process_events_details</b> — it "
      "normalises the raw event_details JSON directly."),
    sp(6),
    h2("13.1  Normalisation"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "normalize_json_column",
             "Flatten <b>event_details</b> directly from the filtered DataFrame "
             "(skip_if_not_exists: true, sort_columns: true). "
             "Columns retain the raw event_details__ prefix."],
            ["2", "transform_columns",
             "Rename eight specific prefixed columns to readable names "
             "(skip_missing_rename: true, required_columns: []). "
             "All other event_details__ columns are left as-is."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("13.2  Column renames (transform_columns)"),
    make_table(
        [
            ["Source column (event_details__*)", "Renamed to"],
            ["wildlifecarcass_species",         "wildlife_carcass_species"],
            ["wildlifecarcass_suspectedcause",  "wildlife_carcass_suspected_cause"],
            ["wildlifecarcass_visibleinjury",   "wildlife_carcass_visible_injury"],
            ["wildlifecarcass_comments",        "wildlife_carcass_comments"],
            ["wildlifetreatment_species",       "wildlife_treatment_species"],
            ["wildlifetreatment_comments",      "wildlife_treatment_comments"],
            ["wildlifetreatment_vetattending",  "wildlife_treatment_vet_attending"],
            ["wildlifetreatment_vetprognosis",  "wildlife_treatment_vet_prognosis"],
        ],
        [7*cm, W - 7*cm],
    ),
    sp(6),
    h2("13.3  CSV outputs"),
    make_table(
        [
            ["Step", "Task", "Output"],
            ["1", "persist_df",
             "<b>wildlife_events_recorded.csv</b> — full renamed DataFrame "
             "(all columns after transform_columns)."],
            ["2", "make_wildlife_summary_table",
             "Custom task that pivots events by type with readable labels: "
             "fire_rep→Fire, snare_rep→Snare, wildlife_carcass_rep→Wildlife carcass, "
             "wildlife_injury_rep→Injured wildlife, "
             "wildlife_treatment_rep→Veterinary treatment. "
             "(max_unique: 6, shorten_width: 300)"],
            ["3", "persist_df",
             "<b>wildlife_incidents_summary_table.csv</b> — pivoted incident summary."],
            ["4", "summarize_df + add_totals_row",
             "Group by <b>date</b>, nunique id → <b>no_of_events</b> + Total row."],
            ["5", "persist_df",
             "<b>wildlife_incidents_recorded_by_date.csv</b> — daily incident count."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("13.4  Incident map"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "exclude_geom_outliers", "Remove spatial outliers (z_threshold: 3)."],
            ["2", "drop_null_geometry",    "Drop rows with null geometry."],
            ["3", "apply_color_map",
             "Colour points by <b>event_type</b> (tab20) → column <b>colors</b>."],
            ["4", "map_column_values",
             "Replace raw event_type values with readable labels in place: "
             "fire_rep→Fire, snare_rep→Snare, wildlife_carcass_rep→Wildlife carcass, "
             "wildlife_injury_rep→Injured wildlife, "
             "wildlife_treatment_rep→Veterinary treatment."],
            ["5", "create_scatterplot_layer",
             "Render points: get_radius: 4, opacity: 0.75. "
             "Legend title: 'Incidents', label from event_type."],
            ["6", "combine_deckgl_map_layers",
             "Static layers: conservancy_boundaries + parcels + text labels."],
            ["7", "draw_map + persist_text + html_to_png",
             "Save as <b>wildlife_incidents_map.html / .png</b> "
             "(max_zoom: 15, wait: 40 s, device_scale_factor: 2.0)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 14. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("14. Output Files"),
    hr(),
    p("All outputs are written to <b>ECOSCOPE_WORKFLOWS_RESULTS</b>."),
    h2("14.1  CSV tables"),
    make_table(
        [
            ["File", "Branch", "Description"],
            ["total_elephants_events_recorded.csv",    "Elephant",
             "Daily unique sighting count (date, no_of_events) + Total"],
            ["total_buffalo_events_recorded.csv",      "Buffalo",
             "Daily unique sighting count + Total"],
            ["total_rhino_events_recorded.csv",        "Rhino",
             "Daily unique sighting count + Total"],
            ["total_lion_events_recorded.csv",         "Lion",
             "Daily unique sighting count + Total"],
            ["total_leopard_events_recorded.csv",      "Leopard",
             "Daily unique sighting count + Total"],
            ["individual_leopard_summary.csv",         "Leopard",
             "Sighting count by individuals_present"],
            ["total_cheetah_events_recorded.csv",      "Cheetah",
             "Daily unique sighting count + Total"],
            ["individual_cheetah_summary.csv",         "Cheetah",
             "Sighting count by individuals_present"],
            ["wildlife_events_recorded.csv",           "Wildlife incidents",
             "Full renamed incident records"],
            ["wildlife_incidents_summary_table.csv",   "Wildlife incidents",
             "Pivoted incident summary by type"],
            ["wildlife_incidents_recorded_by_date.csv","Wildlife incidents",
             "Daily unique incident count + Total"],
        ],
        [5.5*cm, 2.5*cm, W - 8*cm],
    ),
    sp(6),
    h2("14.2  Maps and charts"),
    make_table(
        [
            ["File", "Branch", "Coloured by"],
            ["elephant_sightings_events.html / .png",   "Elephant", "herd_composition"],
            ["elephant_herd_size_bar_chart.html / .png","Elephant", "herd_size bins (bar chart)"],
            ["elephant_herd_types_map.html / .png",     "Elephant", "herd_sizebins_sort (Blues, bubble size = herd_size)"],
            ["buffalo_sightings_events.html / .png",    "Buffalo",  "herd_composition"],
            ["buffalo_herd_size_bar_chart.html / .png", "Buffalo",  "herd_size bins (bar chart)"],
            ["buffalo_herd_types_map.html / .png",      "Buffalo",  "herd_sizebins_sort (Blues, bubble size = herd_size)"],
            ["rhino_sightings_events.html / .png",      "Rhino",    "event_type"],
            ["lion_sightings_events.html / .png",       "Lion",     "pride"],
            ["leopard_sightings_events.html / .png",    "Leopard",  "individuals_present"],
            ["giraffe_sightings_events.html / .png",    "Giraffe",  "event_type"],
            ["hartebeest_sightings_events.html / .png", "Hartebeest","event_type"],
            ["wildlife_incidents_map.html / .png",      "Wildlife incidents","event_type (mapped to readable labels)"],
        ],
        [5.5*cm, 2.5*cm, W - 8*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 15. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("15. Workflow Execution Logic"),
    hr(),
    h2("15.1  Per-task skip conditions"),
    p("Every task from event retrieval onwards carries its own explicit skipif:"),
    make_table(
        [
            ["Condition", "Behaviour"],
            ["any_is_empty_df",        "Skip if any input DataFrame is empty"],
            ["any_dependency_skipped", "Skip if any upstream dependency was skipped"],
        ],
        [5*cm, W - 5*cm],
    ),
    note("Skip conditions propagate independently across all nine branches. "
         "If no rhino events are returned, only the rhino branch is skipped; "
         "all other branches continue normally."),
    sp(6),
    h2("15.2  Nine independent branches"),
    make_table(
        [
            ["Branch", "Event type(s)", "CSV outputs", "Map outputs"],
            ["Elephant",   "elephant_sighting_rep",  "1", "3 (composition + bar chart + bubble)"],
            ["Buffalo",    "buffalo_sighting_rep",   "1", "3 (composition + bar chart + bubble)"],
            ["Rhino",      "rhino_sighting_rep",     "1", "1"],
            ["Lion",       "lion_sighting_rep",      "1", "1"],
            ["Leopard",    "leopardsightingrep",     "2", "1"],
            ["Cheetah",    "cheetah_sighting_rep",   "2", "1 (see bug note §10)"],
            ["Giraffe",    "giraffe_sighting",       "0", "1"],
            ["Hartebeest", "hartebeest_sighting",    "0", "1"],
            ["Wildlife incidents",
             "snare_rep, fire_rep, wildlife_injury_rep, "
             "wildlife_treatment_rep, wildlife_carcass_rep",
             "3", "1"],
        ],
        [3*cm, 4*cm, 1.5*cm, W - 8.5*cm],
    ),
    sp(6),
    h2("15.3  HTML to PNG settings"),
    p("All maps and bar charts are converted to PNG with the same settings "
      "except the bar charts: device_scale_factor: 2.0, full_page: false, "
      "max_concurrent_pages: 1. Map wait_for_timeout: 40 000 ms; "
      "bar chart wait_for_timeout: 10 ms (chart renders client-side immediately)."),
    sp(6),
    h2("15.4  Dashboard"),
    p("The workflow ends with <b>gather_dashboard</b> (widgets: []) which "
      "packages workflow details, time range, and groupers. "
      "No widget outputs are configured."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 16. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("16. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned in spec.yaml"],
            ["ecoscope-workflows-core",        "0.22.18.*"],
            ["ecoscope-workflows-ext-ecoscope","0.22.18.*"],
            ["ecoscope-workflows-ext-custom",  "0.0.43.*"],
            ["ecoscope-workflows-ext-ste",     "0.0.18.*"],
            ["ecoscope-workflows-ext-mnc",     "0.0.8.*"],
        ],
        [7*cm, W - 7*cm],
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF written → {OUTPUT_FILE}")
