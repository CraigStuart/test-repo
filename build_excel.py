#!/usr/bin/env python3
"""Build london_relocation.xlsx from the canonical dataset."""
import sys
sys.path.insert(0, '.')

from data.london_areas import AREAS
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.utils import get_column_letter

OUTPUT = "london_relocation.xlsx"

# ── Colour constants ──────────────────────────────────────────────────────────
HDR_NAVY  = PatternFill("solid", fgColor="1A2744")
HDR_GREY  = PatternFill("solid", fgColor="5D6D7E")   # band/helper cols
ROW_ODD   = PatternFill("solid", fgColor="F8F6F1")
ROW_EVEN  = PatternFill("solid", fgColor="F0EDE8")
BENCHMARK = PatternFill("solid", fgColor="DDEEFF")

GREEN = PatternFill("solid", fgColor="C6EFCE")
AMBER = PatternFill("solid", fgColor="FFEB9C")
RED   = PatternFill("solid", fgColor="FFC7CE")


def cell_color(col_letter, value):
    """Return fill for absolute-threshold colour coding, or None."""
    rules = {
        "F": lambda v: GREEN if v <= 25 else (AMBER if v <= 35 else RED),
        "H": lambda v: GREEN if v == 0 else (AMBER if v == 1 else RED),
        "I": lambda v: GREEN if v <= 25 else (AMBER if v <= 35 else RED),
        "K": lambda v: GREEN if v == 0 else (AMBER if v == 1 else RED),
        "L": lambda v: GREEN if v == "Yes" else RED,
        "M": lambda v: GREEN if v == "High" else (AMBER if v == "Med" else RED),
        "O": lambda v: GREEN if v == "Good" else (AMBER if v == "Med" else RED),
        "Q": lambda v: GREEN if v == "Comfortable" else (AMBER if v == "Moderate" else RED),
        "R": lambda v: GREEN if v == "Yes" else AMBER,
        "U": lambda v: GREEN if v == "Low" else (AMBER if v == "Med" else RED),
        "V": lambda v: GREEN if v == "Low" else (AMBER if v == "Med" else RED),
        "W": lambda v: GREEN if v == "Low" else (AMBER if v == "Med" else RED),
        "AD": lambda v: GREEN if v == "Low" else (AMBER if v == "Med" else RED),
        "AE": lambda v: GREEN if v == "Yes" else RED,
        "AF": lambda v: GREEN if v == "Low" else (AMBER if v == "Med" else RED),
        "AG": lambda v: GREEN if v == "None" else (AMBER if v in ("Low", "Med") else RED),
        "AH": lambda v: GREEN if v == "Yes" else RED,
        "AI": lambda v: GREEN if v == "Yes" else RED,
        "AJ": lambda v: GREEN if v == "Good" else (AMBER if v == "OK" else RED),
        "AK": lambda v: GREEN if v <= 2000 else (AMBER if v <= 2500 else RED),
        "AS": lambda v: GREEN if v == "Yes" else AMBER,
        "AU": lambda v: GREEN if v in ("Benchmark", "Contender") else RED,
        "AV": lambda v: GREEN if v >= 70 else (AMBER if v >= 55 else RED),
    }
    fn = rules.get(col_letter)
    if fn is None:
        return None
    try:
        return fn(value)
    except Exception:
        return None


def build_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Areas"

    # ── Column definitions: (header_text, field_key_or_None, is_band_col) ────
    columns = [
        ("Area",                          "area",                    False),
        ("Postcode",                       "postcode",                False),
        ("Region",                         "region",                  False),
        ("Nearest Station",               "nearest_station",         False),
        ("Walk to Stn (min)",              "walk_to_station_mins",    False),
        ("Her→KX (min)",                   "her_kx_mins",             False),
        ("Her Commute Band",               "her_commute_band",        True),
        ("Her Changes",                    "her_changes",             False),
        ("Him→City (min)",                 "him_city_mins",           False),
        ("Him Commute Band",               "him_commute_band",        True),
        ("Him Changes",                    "him_changes",             False),
        ("Both ≤30",                       "both_u30",                False),
        ("Line Resilience",                "line_resilience",         False),
        ("Backup Notes",                   "backup_notes",            False),
        ("Strike Resilience",              "strike_resilience",       False),
        ("Strike Backup",                  "strike_backup",           False),
        ("Peak Crowding",                  "peak_crowding",           False),
        ("Night Tube",                     "night_tube",              False),
        ("Cycle Her→KX (min)",             "cycling_her_to_kx_mins",  False),
        ("Cycle Him→City (min)",           "cycling_him_to_city_mins",False),
        ("Crime Rate Band",                "crime_rate_band",         False),
        ("Drug Crime Band",                "drug_crime_band",         False),
        ("Deprivation Band",               "deprivation_band",        False),
        ("Demographic Profile",            "demographic_profile",     False),
        ("Area Trajectory",                "area_trajectory",         False),
        ("Hoodmaps Label",                 "hoodmaps_label",          False),
        ("Owner-Occ %",                    "owner_occupier_pct",      False),
        ("Owner-Occ Band",                 "owner_occupier_band",     True),
        ("Community Housing %",            "community_housing_pct",   False),
        ("Social Housing",                 "social_housing",          False),
        ("Night Safe",                     "night_safe",              False),
        ("Flood Risk",                     "flood_risk",              False),
        ("Heathrow Noise",                 "heathrow_noise",          False),
        ("Period Garden Flat ≤£2,800",     "period_garden_flat_u2800",False),
        ("3-Bed ≤£2,800",                  "three_bed_u2800",         False),
        ("Bike Storage",                   "bike_storage",            False),
        ("Indicative Rent £",              "indicative_rent",         False),
        ("Rent Band",                      "rent_band",               True),
        ("Council Tax Band",               "council_tax_band_est",    False),
        ("Big Park",                       "big_park",                False),
        ("Cycling (1–5)",                  "cycling",                 False),
        ("Gym Access (1–5)",               "gym_access",              False),
        ("Amenity Score (1–5)",            "amenity_score",           False),
        ("Quality Grocers Count",          "quality_grocers_count",   False),
        ("2+ Quality Grocers",             "two_plus_grocers",        False),
        ("Fit vs E Putney (1–5)",          "fit_vs_east_putney",      False),
        ("Status",                         "status",                  False),
        ("Score",                          "score",                   False),
        ("Score Tier",                     "score_tier",              True),
        ("Quick Verdict",                  "quick_verdict",           False),
        ("Write-up",                       "write_up",                False),
        ("Latitude",                       "lat",                     False),
        ("Longitude",                      "lng",                     False),
    ]

    # ── Header row ────────────────────────────────────────────────────────────
    header_font    = Font(name="Arial", size=10, bold=True, color="FFFFFF")
    header_align   = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for col_idx, (hdr, _, is_band) in enumerate(columns, start=1):
        cell = ws.cell(row=1, column=col_idx, value=hdr)
        cell.font = header_font
        cell.fill = HDR_GREY if is_band else HDR_NAVY
        cell.alignment = header_align

    ws.row_dimensions[1].height = 50

    # ── Column widths ─────────────────────────────────────────────────────────
    widths = [25,8,14,22,9, 9,14,8, 9,14,8, 8,12,32,12,38,13,9,12,12,
              12,12,12,20,18,15,10,17,14,12, 9,10,14,14,12,12,12,16,22,
              9,9,9,9,12,10,14,13,9,22,40,50,10,10]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    # ── Freeze panes & AutoFilter ─────────────────────────────────────────────
    ws.freeze_panes = "B2"

    # ── Data rows ─────────────────────────────────────────────────────────────
    benchmark_row = None
    for row_idx, area in enumerate(AREAS, start=2):
        fill = ROW_ODD if row_idx % 2 == 1 else ROW_EVEN
        is_benchmark = area["area"] == "East Putney/Southfields"
        if is_benchmark:
            benchmark_row = row_idx

        for col_idx, (_, field, _) in enumerate(columns, start=1):
            raw = area.get(field, "")
            # Convert booleans to Yes/No for clean dropdown filtering
            if isinstance(raw, bool):
                value = "Yes" if raw else "No"
            else:
                value = raw

            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.alignment = Alignment(vertical="top", wrap_text=(col_idx > 48))

            col_letter = get_column_letter(col_idx)
            color = cell_color(col_letter, value)
            cell.fill = color if color else fill

        # Number formats
        rent_col = next(i for i,(h,f,_) in enumerate(columns,1) if f=="indicative_rent")
        score_col = next(i for i,(h,f,_) in enumerate(columns,1) if f=="score")
        ws.cell(row=row_idx, column=rent_col).number_format = "£#,##0"
        ws.cell(row=row_idx, column=score_col).number_format = "0.0"

    last_row = len(AREAS) + 1

    # AutoFilter over all columns
    ws.auto_filter.ref = f"A1:{get_column_letter(len(columns))}{last_row}"

    # ── Benchmark row highlight (override fills) ──────────────────────────────
    if benchmark_row:
        for col_idx in range(1, len(columns)+1):
            c = ws.cell(row=benchmark_row, column=col_idx)
            # Only override if currently row background (not a green/amber/red cell)
            if c.fill.fgColor.rgb in ("FFF8F6F1","FFF0EDE8","00000000"):
                c.fill = BENCHMARK

    # ── Layer 2: Column-wise heatmap (ColorScaleRule) ─────────────────────────
    green_high = ColorScaleRule(
        start_type="min", start_color="FFFFC7CE",
        mid_type="percentile", mid_value=50, mid_color="FFFFEB9C",
        end_type="max", end_color="FFC6EFCE"
    )
    rent_scale = ColorScaleRule(
        start_type="num", start_value=1500, start_color="FFC6EFCE",
        mid_type="num",  mid_value=2400,  mid_color="FFFFEB9C",
        end_type="num",  end_value=3200,  end_color="FFFFC7CE"
    )

    heatmap_fields = ["her_kx_mins","her_changes","him_city_mins","him_changes",
                      "owner_occupier_pct","community_housing_pct",
                      "cycling","gym_access","amenity_score","quality_grocers_count",
                      "fit_vs_east_putney","score"]
    field_to_col = {f: get_column_letter(i+1) for i,(h,f,_) in enumerate(columns)}

    for field in heatmap_fields:
        col = field_to_col.get(field)
        if col:
            rng = f"{col}2:{col}{last_row}"
            rule = rent_scale if field == "indicative_rent" else green_high
            ws.conditional_formatting.add(rng, rule)

    # Rent heatmap separately (inverted)
    rc = field_to_col.get("indicative_rent")
    if rc:
        ws.conditional_formatting.add(f"{rc}2:{rc}{last_row}", rent_scale)

    # ── Methodology sheet ─────────────────────────────────────────────────────
    ws2 = wb.create_sheet("Methodology")
    ws2.column_dimensions["A"].width = 90

    title_font = Font(name="Arial", size=14, bold=True)
    body_font  = Font(name="Arial", size=10)
    head_font  = Font(name="Arial", size=11, bold=True)

    rows = [
        ("London Relocation Decision Tool — Methodology & Caveats", title_font),
        ("", body_font),
        ("PURPOSE", head_font),
        ("Helps a professional couple compare ~65 London areas on commute, safety, property, "
         "and quality of life. Two fixed workplaces: Her at King's Cross St Pancras; "
         "Him at the Guildhall, City of London (nearest: Bank/Moorgate).", body_font),
        ("", body_font),
        ("SCORING FORMULA", head_font),
        ("Total score = Variable pool (82 pts) + Fixed bonus pool (18 pts, capped at 18).", body_font),
        ("", body_font),
        ("Variable pool weights (adjustable in the HTML tool):", body_font),
        ("  Commute .............. 35%  (her commute weighted 60%, his 40% within sub-score)", body_font),
        ("  Private garden ........ 20%  (ground-level exclusive garden only)", body_font),
        ("  Bike storage .......... 15%  (Good = private cellar/outbuilding/garage only)", body_font),
        ("  Space (3-bed ≤£2,800) . 15%", body_font),
        ("  Rent (lower=better) ... 15%  (floor £1,600, ceiling £2,800)", body_font),
        ("", body_font),
        ("Fixed bonus pool (non-adjustable):", body_font),
        ("  Crime Low: +3 | Crime Med: +1 | Drug crime Low: +2 | Social housing Low: +2", body_font),
        ("  Big park: +2 | Gym access ≥4: +2 | Strike resilience Good: +2", body_font),
        ("  Flood risk Low: +1 | No Heathrow noise: +1 | Night Tube: +1 | Cycling ≥4: +1", body_font),
        ("", body_font),
        ("STATUS", head_font),
        ("  Benchmark: East Putney/Southfields (current home)", body_font),
        ("  Contender: Both commutes ≤30 min AND score ≥65", body_font),
        ("  Compromise: everything else (commute fails or score <65)", body_font),
        ("", body_font),
        ("BAND / HELPER COLUMNS (grey headers)", head_font),
        ("  Her/Him Commute Band, Rent Band, Owner-Occ Band, Score Tier are derived text", body_font),
        ("  columns added for easy dropdown filtering — the raw numbers remain adjacent.", body_font),
        ("", body_font),
        ("TWO-LAYER COLOUR CODING", head_font),
        ("  Layer 1 (absolute): green/amber/red based on fixed thresholds per column.", body_font),
        ("  Layer 2 (relative): column-wise colour scale — green=best, red=worst in each column.", body_font),
        ("", body_font),
        ("DATA SOURCES & CAVEATS", head_font),
        ("  Commute times: TfL Journey Planner (AM peak, 08:00 departure), door-to-door.", body_font),
        ("  Walk to station: Google Maps / Walkit.com estimates.", body_font),
        ("  Crime / drug crime: Metropolitan Police (data.police.uk), ward-level, 2024.", body_font),
        ("  Deprivation: English IMD 2019/2023 (MHCLG).", body_font),
        ("  Flood risk: Environment Agency Flood Map for Planning.", body_font),
        ("  Owner-occupier % / community housing: ONS Census 2021.", body_font),
        ("  Demographic profile / area trajectory: Hoodmaps (hoodmaps.com/london-neighborhood-map), "
         "Rightmove area guides, Zoopla market trends, local knowledge.", body_font),
        ("  Heathrow noise: CAA Airspace Change Portal; Heathrow noise contour maps.", body_font),
        ("  Rents: Rightmove / Zoopla market data Q2 2026 (indicative only).", body_font),
        ("  Council tax: London borough / Surrey council tax schedules 2025/26.", body_font),
        ("  Amenities: Google Maps, local knowledge.", body_font),
        ("", body_font),
        ("  All data is indicative. Verify commute times on TfL Journey Planner before "
         "committing. Verify crime statistics at data.police.uk. Flood risk MUST be "
         "checked per specific property via EA flood map. Do not rely on indicative "
         "rents — check Rightmove/Zoopla for current listings.", body_font),
        ("", body_font),
        ("  Last updated: May 2026", body_font),
    ]

    for i, (text, font) in enumerate(rows, start=1):
        cell = ws2.cell(row=i, column=1, value=text)
        cell.font = font
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws2.row_dimensions[i].height = 30 if font == title_font else 15

    wb.save(OUTPUT)
    print(f"Saved {OUTPUT} ({len(AREAS)} areas, {len(columns)} columns)")


if __name__ == "__main__":
    build_excel()
