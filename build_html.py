#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '.')
from data.london_areas import AREAS

OUTPUT = "london_relocation.html"

areas_json = json.dumps(AREAS, ensure_ascii=False)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>London Relocation Intelligence</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>
:root {{
  --bg: #F8F6F1;
  --navy: #1A2744;
  --gold: #C9A84C;
  --sage: #7B9E87;
  --amber-col: #D4933A;
  --terra: #C4614A;
  --text: #2C2C2C;
  --muted: #6B6B6B;
}}
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'DM Sans', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
}}
h1, h2, h3, h4, .playfair {{ font-family: 'Playfair Display', serif; }}

/* HEADER */
header {{
  background: var(--navy);
  color: white;
  padding: 28px 32px 24px;
  border-bottom: 3px solid var(--gold);
}}
header h1 {{
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: white;
}}
header .subtitle {{
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  color: rgba(255,255,255,0.65);
  margin-top: 4px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}}

/* MAIN LAYOUT */
main {{ max-width: 1400px; margin: 0 auto; padding: 0 20px 40px; }}

/* CONTROLS */
.controls-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin: 24px 0;
}}
.panel {{
  background: white;
  border-radius: 12px;
  padding: 20px 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}}
.panel h3 {{
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--navy);
  margin-bottom: 14px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}}

/* WEIGHT SLIDERS */
.weight-bars {{
  display: flex;
  gap: 3px;
  height: 28px;
  margin-bottom: 14px;
  border-radius: 4px;
  overflow: hidden;
}}
.weight-bar-seg {{
  transition: width 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.62rem;
  font-weight: 600;
  color: white;
  overflow: hidden;
  white-space: nowrap;
}}
.weight-bar-seg.commute {{ background: var(--navy); }}
.weight-bar-seg.garden {{ background: var(--sage); }}
.weight-bar-seg.bike {{ background: var(--amber-col); }}
.weight-bar-seg.space {{ background: var(--gold); }}
.weight-bar-seg.rent {{ background: var(--terra); }}

.slider-row {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}}
.slider-row label {{
  font-size: 0.82rem;
  font-weight: 500;
  width: 72px;
  flex-shrink: 0;
  color: var(--text);
}}
.slider-row input[type=range] {{
  flex: 1;
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  background: #e0ddd6;
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}}
.slider-row input[type=range]::-webkit-slider-thumb {{
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--navy);
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
}}
.slider-row input[type=range]::-moz-range-thumb {{
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--navy);
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 1px 4px rgba(0,0,0,0.2);
}}
.slider-val {{
  font-size: 0.8rem;
  font-weight: 600;
  width: 34px;
  text-align: right;
  color: var(--navy);
}}

/* FILTERS */
.filters-panel {{ display: flex; flex-direction: column; gap: 8px; }}
details.filter-group {{
  background: #faf9f6;
  border: 1px solid #ece9e1;
  border-radius: 8px;
  overflow: hidden;
}}
details.filter-group summary {{
  padding: 10px 14px;
  font-size: 0.84rem;
  font-weight: 600;
  color: var(--navy);
  cursor: pointer;
  user-select: none;
  list-style: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
details.filter-group summary::-webkit-details-marker {{ display: none; }}
details.filter-group summary::after {{
  content: '›';
  font-size: 1.1rem;
  transition: transform 0.2s;
  color: var(--muted);
}}
details.filter-group[open] summary::after {{
  transform: rotate(90deg);
}}
.filter-body {{
  padding: 10px 14px 14px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px 12px;
}}
.filter-item {{
  display: flex;
  flex-direction: column;
  gap: 3px;
}}
.filter-item label {{
  font-size: 0.75rem;
  color: var(--muted);
  font-weight: 500;
}}
.filter-item select {{
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8rem;
  padding: 5px 8px;
  border: 1px solid #ddd9d0;
  border-radius: 5px;
  background: white;
  color: var(--text);
  cursor: pointer;
  outline: none;
}}
.filter-item select:focus {{ border-color: var(--navy); }}
.checkbox-row {{
  display: flex;
  align-items: center;
  gap: 7px;
  grid-column: span 2;
}}
.checkbox-row label {{
  font-size: 0.8rem;
  color: var(--text);
  font-weight: 500;
  cursor: pointer;
}}
.checkbox-row input[type=checkbox] {{
  width: 15px;
  height: 15px;
  cursor: pointer;
  accent-color: var(--navy);
}}
.rent-slider-row {{ grid-column: span 2; }}
.rent-slider-row input[type=range] {{
  width: 100%;
  margin-top: 4px;
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  background: #e0ddd6;
  border-radius: 2px;
  cursor: pointer;
}}
.rent-slider-row input[type=range]::-webkit-slider-thumb {{
  -webkit-appearance: none;
  width: 16px; height: 16px;
  border-radius: 50%;
  background: var(--terra);
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}}
.rent-slider-row input[type=range]::-moz-range-thumb {{
  width: 16px; height: 16px;
  border-radius: 50%;
  background: var(--terra);
  cursor: pointer;
  border: 2px solid white;
}}

/* STATS BAR */
.stats-bar {{
  background: var(--navy);
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 0.87rem;
  display: flex;
  align-items: center;
  gap: 16px;
}}
.stats-bar strong {{ color: var(--gold); }}

/* WRITE-UP PANEL */
.writeup-panel {{
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  overflow: hidden;
  max-height: 0;
  transition: max-height 0.4s ease;
  margin-bottom: 16px;
}}
.writeup-panel.open {{ max-height: 600px; }}
.writeup-inner {{
  padding: 24px 28px;
  overflow-y: auto;
  max-height: 600px;
}}
.writeup-header {{
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}}
.writeup-title {{
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--navy);
  line-height: 1.2;
}}
.score-pill {{
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  color: white;
  white-space: nowrap;
  align-self: center;
}}
.status-badge {{
  display: inline-block;
  padding: 3px 10px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  align-self: center;
  border: 1.5px solid currentColor;
}}
.status-badge.Benchmark {{ color: var(--gold); }}
.status-badge.Contender {{ color: var(--sage); }}
.status-badge.Compromise {{ color: var(--muted); }}

.writeup-meta {{
  font-size: 0.82rem;
  color: var(--muted);
  margin-bottom: 14px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}}
.writeup-meta span {{ display: flex; align-items: center; gap: 4px; }}

.writeup-commute {{
  background: #f4f2ec;
  border-radius: 8px;
  padding: 10px 16px;
  font-size: 0.84rem;
  margin-bottom: 12px;
  line-height: 1.8;
}}
.writeup-commute .ok {{ color: var(--sage); font-weight: 700; }}
.writeup-commute .no {{ color: var(--terra); font-weight: 700; }}

.writeup-strike {{
  font-size: 0.82rem;
  color: var(--muted);
  margin-bottom: 14px;
  padding: 8px 12px;
  background: #fef9f0;
  border-left: 3px solid var(--gold);
  border-radius: 0 6px 6px 0;
}}

.facts-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 14px;
}}
.fact-card {{
  background: #f8f6f1;
  border-radius: 8px;
  padding: 10px 12px;
  text-align: center;
}}
.fact-card .fact-val {{
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--navy);
}}
.fact-card .fact-lbl {{
  font-size: 0.7rem;
  color: var(--muted);
  margin-top: 2px;
}}

.demographics-row {{
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 14px;
  font-size: 0.82rem;
}}
.demo-chip {{
  background: #eeeae0;
  padding: 4px 10px;
  border-radius: 20px;
  color: var(--text);
}}

.writeup-text {{
  font-size: 0.88rem;
  line-height: 1.75;
  color: var(--text);
  margin-bottom: 10px;
}}
.quick-verdict {{
  font-size: 0.85rem;
  color: var(--muted);
  font-style: italic;
  border-top: 1px solid #ece9e1;
  padding-top: 10px;
}}

/* MAP */
.map-container {{
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  margin-bottom: 16px;
}}
#map {{ height: 420px; width: 100%; }}

/* TABLE */
.table-container {{
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  overflow: hidden;
}}
.table-scroll {{ overflow-x: auto; }}
table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8rem;
}}
thead {{
  background: var(--navy);
  position: sticky;
  top: 0;
  z-index: 10;
}}
thead th {{
  padding: 11px 10px;
  text-align: left;
  color: white;
  font-weight: 600;
  white-space: nowrap;
  cursor: pointer;
  user-select: none;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}}
thead th:hover {{ background: rgba(255,255,255,0.1); }}
thead th.sort-active {{ color: var(--gold); }}
tbody tr {{
  border-bottom: 1px solid #f0ede5;
  cursor: pointer;
  transition: background 0.1s;
}}
tbody tr:hover {{ background: #f8f6f1; }}
tbody tr.selected {{ background: #edf3ef; }}
tbody tr.row-benchmark {{ border-left: 4px solid var(--gold); }}
tbody tr.row-contender {{ border-left: 2px solid var(--sage); }}
tbody td {{
  padding: 9px 10px;
  color: var(--text);
  white-space: nowrap;
}}
.rank-cell {{
  font-weight: 700;
  color: var(--muted);
  font-size: 0.75rem;
  width: 32px;
}}
.ok-tick {{ color: var(--sage); font-weight: 700; }}
.no-tick {{ color: var(--terra); font-weight: 600; }}

@media (max-width: 768px) {{
  header {{ padding: 18px 16px; }}
  header h1 {{ font-size: 1.4rem; }}
  main {{ padding: 0 12px 30px; }}
  .controls-grid {{ grid-template-columns: 1fr; gap: 14px; }}
  .filter-body {{ grid-template-columns: 1fr; }}
  .checkbox-row {{ grid-column: span 1; }}
  .facts-grid {{ grid-template-columns: repeat(2, 1fr); }}
  #map {{ height: 300px; }}
}}
</style>
</head>
<body>

<header>
  <h1>London Relocation Intelligence</h1>
  <div class="subtitle">65 areas &middot; dual commute &middot; May 2026</div>
</header>

<main>
  <div class="controls-grid">
    <!-- LEFT: Weight sliders -->
    <div class="panel">
      <h3>Score Weights</h3>
      <div class="weight-bars" id="weightBars">
        <div class="weight-bar-seg commute" id="wb-commute"></div>
        <div class="weight-bar-seg garden" id="wb-garden"></div>
        <div class="weight-bar-seg bike" id="wb-bike"></div>
        <div class="weight-bar-seg space" id="wb-space"></div>
        <div class="weight-bar-seg rent" id="wb-rent"></div>
      </div>
      <div class="slider-row">
        <label>Commute</label>
        <input type="range" id="sl-commute" min="0" max="100" value="35">
        <span class="slider-val" id="sv-commute">35%</span>
      </div>
      <div class="slider-row">
        <label>Garden</label>
        <input type="range" id="sl-garden" min="0" max="100" value="20">
        <span class="slider-val" id="sv-garden">20%</span>
      </div>
      <div class="slider-row">
        <label>Bike</label>
        <input type="range" id="sl-bike" min="0" max="100" value="15">
        <span class="slider-val" id="sv-bike">15%</span>
      </div>
      <div class="slider-row">
        <label>Space</label>
        <input type="range" id="sl-space" min="0" max="100" value="15">
        <span class="slider-val" id="sv-space">15%</span>
      </div>
      <div class="slider-row">
        <label>Rent</label>
        <input type="range" id="sl-rent" min="0" max="100" value="15">
        <span class="slider-val" id="sv-rent">15%</span>
      </div>
    </div>

    <!-- RIGHT: Filters -->
    <div class="panel filters-panel">
      <h3>Filters</h3>

      <details class="filter-group">
        <summary>Commute &amp; Resilience</summary>
        <div class="filter-body">
          <div class="checkbox-row">
            <input type="checkbox" id="f-bothU30">
            <label for="f-bothU30">Both commutes &le;30 min</label>
          </div>
          <div class="filter-item">
            <label>Her commute band</label>
            <select id="f-herBand">
              <option value="Any">Any</option>
              <option value="≤20 min">&le;20 min</option>
              <option value="21–30 min">21&ndash;30 min</option>
              <option value="31–40 min">31&ndash;40 min</option>
              <option value="41–50 min">41&ndash;50 min</option>
              <option value="51+ min">51+ min</option>
            </select>
          </div>
          <div class="filter-item">
            <label>Him commute band</label>
            <select id="f-himBand">
              <option value="Any">Any</option>
              <option value="≤20 min">&le;20 min</option>
              <option value="21–30 min">21&ndash;30 min</option>
              <option value="31–40 min">31&ndash;40 min</option>
              <option value="41–50 min">41&ndash;50 min</option>
              <option value="51+ min">51+ min</option>
            </select>
          </div>
          <div class="filter-item">
            <label>Line resilience</label>
            <select id="f-lineRes">
              <option value="Any">Any</option>
              <option value="High">High</option>
              <option value="Med">Med</option>
              <option value="Low">Low</option>
            </select>
          </div>
          <div class="filter-item">
            <label>Strike resilience</label>
            <select id="f-strikeRes">
              <option value="Any">Any</option>
              <option value="Good">Good</option>
              <option value="Med">Med</option>
              <option value="Poor">Poor</option>
            </select>
          </div>
          <div class="filter-item">
            <label>Peak crowding</label>
            <select id="f-crowding">
              <option value="Any">Any</option>
              <option value="Comfortable">Comfortable</option>
              <option value="Moderate">Moderate</option>
              <option value="Crowded">Crowded</option>
            </select>
          </div>
          <div class="checkbox-row">
            <input type="checkbox" id="f-nightTube">
            <label for="f-nightTube">Night Tube</label>
          </div>
        </div>
      </details>

      <details class="filter-group">
        <summary>Safety &amp; Demographics</summary>
        <div class="filter-body">
          <div class="filter-item">
            <label>Crime rate</label>
            <select id="f-crime">
              <option value="Any">Any</option>
              <option value="Low">Low</option>
              <option value="Med">Med</option>
              <option value="High">High</option>
              <option value="Very High">Very High</option>
            </select>
          </div>
          <div class="filter-item">
            <label>Drug crime</label>
            <select id="f-drugCrime">
              <option value="Any">Any</option>
              <option value="Low">Low</option>
              <option value="Med">Med</option>
              <option value="High">High</option>
            </select>
          </div>
          <div class="filter-item">
            <label>Social housing</label>
            <select id="f-socialHousing">
              <option value="Any">Any</option>
              <option value="Low">Low</option>
              <option value="Med">Med</option>
              <option value="High">High</option>
            </select>
          </div>
          <div class="filter-item">
            <label>Flood risk</label>
            <select id="f-floodRisk">
              <option value="Any">Any</option>
              <option value="Low">Low</option>
              <option value="Med">Med</option>
              <option value="High">High</option>
            </select>
          </div>
          <div class="filter-item">
            <label>Heathrow noise</label>
            <select id="f-heathrowNoise">
              <option value="Any">Any</option>
              <option value="None">None</option>
              <option value="Low">Low</option>
              <option value="Med">Med</option>
              <option value="High">High</option>
            </select>
          </div>
          <div class="filter-item">
            <label>Area trajectory</label>
            <select id="f-trajectory">
              <option value="Any">Any</option>
              <option value="Gentrifying">Gentrifying</option>
              <option value="Established affluent">Established affluent</option>
              <option value="Peaked">Peaked</option>
              <option value="Mixed">Mixed</option>
            </select>
          </div>
        </div>
      </details>

      <details class="filter-group">
        <summary>Property &amp; Lifestyle</summary>
        <div class="filter-body">
          <div class="checkbox-row">
            <input type="checkbox" id="f-periodGarden">
            <label for="f-periodGarden">Period garden flat &le;&pound;2,800</label>
          </div>
          <div class="checkbox-row">
            <input type="checkbox" id="f-threeBed">
            <label for="f-threeBed">3-bed &le;&pound;2,800</label>
          </div>
          <div class="filter-item">
            <label>Bike storage</label>
            <select id="f-bikeStorage">
              <option value="Any">Any</option>
              <option value="Good">Good</option>
              <option value="OK">OK</option>
              <option value="Hard">Hard</option>
            </select>
          </div>
          <div class="filter-item">
            <label>Gym access min</label>
            <select id="f-gymAccess">
              <option value="Any">Any</option>
              <option value="3">3+</option>
              <option value="4">4+</option>
              <option value="5">5</option>
            </select>
          </div>
          <div class="checkbox-row">
            <input type="checkbox" id="f-twoGrocers">
            <label for="f-twoGrocers">2+ quality grocers</label>
          </div>
          <div class="checkbox-row">
            <input type="checkbox" id="f-bigPark">
            <label for="f-bigPark">Big park</label>
          </div>
          <div class="filter-item">
            <label>Status</label>
            <select id="f-status">
              <option value="All">All</option>
              <option value="Benchmark">Benchmark</option>
              <option value="Contender">Contender</option>
              <option value="Compromise">Compromise</option>
            </select>
          </div>
          <div class="filter-item">
            <label>Region</label>
            <select id="f-region">
              <option value="All">All</option>
              <option value="SW/South">SW/South</option>
              <option value="West">West</option>
              <option value="North">North</option>
              <option value="NE">NE</option>
              <option value="Surrey/Commuter">Surrey/Commuter</option>
            </select>
          </div>
          <div class="rent-slider-row filter-item" style="grid-column:span 2">
            <label>Max rent: <span id="rentValLabel">Max: &pound;3,000</span></label>
            <input type="range" id="f-maxRent" min="1500" max="3000" step="50" value="3000">
          </div>
        </div>
      </details>
    </div>
  </div>

  <!-- STATS BAR -->
  <div class="stats-bar" id="statsBar">
    <span>Loading&hellip;</span>
  </div>

  <!-- WRITE-UP PANEL -->
  <div class="writeup-panel" id="writeupPanel">
    <div class="writeup-inner" id="writeupInner"></div>
  </div>

  <!-- MAP -->
  <div class="map-container">
    <div id="map"></div>
  </div>

  <!-- TABLE -->
  <div class="table-container">
    <div class="table-scroll">
      <table id="areaTable">
        <thead>
          <tr>
            <th data-col="rank">Rank</th>
            <th data-col="area">Area</th>
            <th data-col="score" class="sort-active">Score &#9660;</th>
            <th data-col="status">Status</th>
            <th data-col="region">Region</th>
            <th data-col="both_u30">Both&le;30</th>
            <th data-col="her_kx_mins">Her&rarr;KX</th>
            <th data-col="him_city_mins">Him&rarr;City</th>
            <th data-col="strike_resilience">Strike</th>
            <th data-col="period_garden_flat_u2800">Garden</th>
            <th data-col="three_bed_u2800">3-Bed</th>
            <th data-col="cycling">Bike</th>
            <th data-col="indicative_rent">Rent &pound;</th>
            <th data-col="crime_rate_band">Crime</th>
            <th data-col="heathrow_noise">Noise</th>
            <th data-col="area_trajectory">Trajectory</th>
          </tr>
        </thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
  </div>
</main>

<script>
const AREAS_DATA = {areas_json};

let weights = {{commute:35, garden:20, bike:15, space:15, rent:15}};
let filters = {{
  bothU30: false, region:'All',
  herBand:'Any', himBand:'Any',
  lineRes:'Any', strikeRes:'Any',
  crowding:'Any', nightTube: false,
  crime:'Any', drugCrime:'Any', socialHousing:'Any',
  floodRisk:'Any', heathrowNoise:'Any',
  periodGarden:false, threeBed:false,
  bikeStorage:'Any', maxRent:3000,
  status:'All', trajectory:'Any',
  gymAccess:'Any', twoGrocers:false, bigPark:false,
}};

let selectedArea = null;
let sortCol = 'score';
let sortAsc = false;
let map = null;
let markers = {{}};
let computedAreas = [];
let filteredIds = new Set();

function computeScore(a, w) {{
  const norm = Object.values(w).reduce((s,v)=>s+v,0);
  const wn = Object.fromEntries(Object.entries(w).map(([k,v])=>[k,v/norm]));
  const base = a.both_u30 ? 50 : 0;
  const herPts = Math.max(0, 25 - Math.max(0, a.her_kx_mins - 20)*2.5);
  const himPts = Math.max(0, 25 - Math.max(0, a.him_city_mins - 20)*2.5);
  const timePts = herPts*0.6 + himPts*0.4;
  const changePen = (a.her_changes + a.him_changes)*5;
  const resBon = {{High:10,Med:5,Low:0}}[a.line_resilience]||0;
  const cs = Math.max(0,Math.min(100,base+timePts-changePen+resBon))/100;
  const gs = a.period_garden_flat_u2800?1:0;
  const bs = {{Good:1,OK:.5,Hard:0}}[a.bike_storage]||0;
  const ss = a.three_bed_u2800?1:0;
  const rs = Math.max(0,Math.min(1,(2800-a.indicative_rent)/1200));
  const variable = 82*(wn.commute*cs + wn.garden*gs + wn.bike*bs + wn.space*ss + wn.rent*rs);
  let bonus=0;
  bonus += a.crime_rate_band==='Low'?3:(a.crime_rate_band==='Med'?1:0);
  bonus += a.drug_crime_band==='Low'?2:0;
  bonus += a.social_housing==='Low'?2:0;
  bonus += a.big_park?2:0;
  bonus += a.gym_access>=4?2:0;
  bonus += a.strike_resilience==='Good'?2:0;
  bonus += a.flood_risk==='Low'?1:0;
  bonus += a.heathrow_noise==='None'?1:0;
  bonus += a.night_tube?1:0;
  bonus += a.cycling>=4?1:0;
  bonus = Math.min(18,bonus);
  return Math.round(Math.min(100,Math.max(0,variable+bonus))*10)/10;
}}

function applyFilters(areas) {{
  return areas.filter(a => {{
    if(filters.bothU30 && !a.both_u30) return false;
    if(filters.region!=='All' && a.region!==filters.region) return false;
    if(filters.herBand!=='Any' && a.her_commute_band!==filters.herBand) return false;
    if(filters.himBand!=='Any' && a.him_commute_band!==filters.himBand) return false;
    if(filters.lineRes!=='Any' && a.line_resilience!==filters.lineRes) return false;
    if(filters.strikeRes!=='Any' && a.strike_resilience!==filters.strikeRes) return false;
    if(filters.crowding!=='Any' && a.peak_crowding!==filters.crowding) return false;
    if(filters.nightTube && !a.night_tube) return false;
    if(filters.crime!=='Any' && a.crime_rate_band!==filters.crime) return false;
    if(filters.drugCrime!=='Any' && a.drug_crime_band!==filters.drugCrime) return false;
    if(filters.socialHousing!=='Any' && a.social_housing!==filters.socialHousing) return false;
    if(filters.floodRisk!=='Any' && a.flood_risk!==filters.floodRisk) return false;
    if(filters.heathrowNoise!=='Any' && a.heathrow_noise!==filters.heathrowNoise) return false;
    if(filters.periodGarden && !a.period_garden_flat_u2800) return false;
    if(filters.threeBed && !a.three_bed_u2800) return false;
    if(filters.bikeStorage!=='Any' && a.bike_storage!==filters.bikeStorage) return false;
    if(a.indicative_rent > filters.maxRent) return false;
    if(filters.status!=='All' && a.status!==filters.status) return false;
    if(filters.trajectory!=='Any' && a.area_trajectory!==filters.trajectory) return false;
    if(filters.gymAccess!=='Any'){{
      const mn=parseInt(filters.gymAccess);
      if(a.gym_access<mn) return false;
    }}
    if(filters.twoGrocers && !a.two_plus_grocers) return false;
    if(filters.bigPark && !a.big_park) return false;
    return true;
  }});
}}

function scoreColor(score) {{
  if(score>=70) return '#7B9E87';
  if(score>=55) return '#D4933A';
  return '#C4614A';
}}

function fmtMins(m) {{
  return m + ' min';
}}

function fmtChanges(n) {{
  return n === 0 ? 'direct' : n + ' chg';
}}

function selectArea(areaName) {{
  selectedArea = areaName;
  renderWriteup();
  renderTable();
  updateMapSelection();
}}

function renderWriteup() {{
  if (!selectedArea) return;
  const a = computedAreas.find(x => x.area === selectedArea);
  if (!a) return;

  const sc = a.score;
  const col = scoreColor(sc);

  const both = a.both_u30
    ? '<span class="ok">&#10003;</span>'
    : '<span class="no">&#10007;</span>';

  const html = `
    <div class="writeup-header">
      <div class="writeup-title playfair">${{a.area}}</div>
      <div class="score-pill" style="background:${{col}}">${{sc}}</div>
      <div class="status-badge ${{a.status}}">${{a.status}}</div>
    </div>
    <div class="writeup-meta">
      <span>&#128205; ${{a.postcode}}</span>
      <span>&#127758; ${{a.region}}</span>
      <span>&#127968; ${{a.hoodmaps_label}}</span>
    </div>
    <div class="writeup-commute">
      <strong>Her &rarr; KX:</strong> ${{fmtMins(a.her_kx_mins)}} (${{fmtChanges(a.her_changes)}})
      &nbsp;&nbsp;|&nbsp;&nbsp;
      <strong>Him &rarr; City:</strong> ${{fmtMins(a.him_city_mins)}} (${{fmtChanges(a.him_changes)}})
      &nbsp;&nbsp;|&nbsp;&nbsp;
      <strong>Both &le;30:</strong> ${{both}}
    </div>
    <div class="writeup-strike">
      &#9889; <strong>Resilience:</strong> ${{a.line_resilience}} &mdash; ${{a.strike_backup || 'N/A'}}
    </div>
    <div class="facts-grid">
      <div class="fact-card">
        <div class="fact-val">&pound;${{a.indicative_rent.toLocaleString()}}</div>
        <div class="fact-lbl">Indicative Rent</div>
      </div>
      <div class="fact-card">
        <div class="fact-val">${{a.flood_risk}}</div>
        <div class="fact-lbl">Flood Risk</div>
      </div>
      <div class="fact-card">
        <div class="fact-val">${{a.heathrow_noise}}</div>
        <div class="fact-lbl">Heathrow Noise</div>
      </div>
      <div class="fact-card">
        <div class="fact-val">${{a.cycling}}/5</div>
        <div class="fact-lbl">Bike Score</div>
      </div>
      <div class="fact-card">
        <div class="fact-val">${{a.period_garden_flat_u2800 ? '&#10003;' : '&#10007;'}}</div>
        <div class="fact-lbl">Period Garden Flat</div>
      </div>
      <div class="fact-card">
        <div class="fact-val">${{a.three_bed_u2800 ? '&#10003;' : '&#10007;'}}</div>
        <div class="fact-lbl">3-Bed &le;&pound;2,800</div>
      </div>
    </div>
    <div class="demographics-row">
      <div class="demo-chip">Crime: ${{a.crime_rate_band}}</div>
      <div class="demo-chip">Drug crime: ${{a.drug_crime_band}}</div>
      <div class="demo-chip">Social housing: ${{a.social_housing}}</div>
      <div class="demo-chip">Trajectory: ${{a.area_trajectory}}</div>
    </div>
    <div class="writeup-text">${{a.write_up || ''}}</div>
    <div class="quick-verdict">${{a.quick_verdict || ''}}</div>
  `;

  document.getElementById('writeupInner').innerHTML = html;
  const panel = document.getElementById('writeupPanel');
  panel.classList.add('open');
  panel.scrollIntoView({{behavior: 'smooth', block: 'nearest'}});
}}

function updateWeightBars() {{
  const keys = ['commute','garden','bike','space','rent'];
  const total = keys.reduce((s,k) => s + weights[k], 0) || 1;
  keys.forEach(k => {{
    const el = document.getElementById('wb-' + k);
    if (el) el.style.width = (weights[k]/total*100) + '%';
  }});
}}

function recalcAll() {{
  // Recompute scores
  computedAreas = AREAS_DATA.map(a => {{
    const copy = Object.assign({{}}, a);
    copy.score = computeScore(a, weights);
    return copy;
  }});

  // Apply filters
  const filtered = applyFilters(computedAreas);
  filteredIds = new Set(filtered.map(a => a.area));

  // Sort
  const sorted = [...computedAreas].sort((a,b) => {{
    let va = a[sortCol], vb = b[sortCol];
    if (typeof va === 'boolean') {{ va = va ? 1 : 0; vb = vb ? 1 : 0; }}
    if (typeof va === 'string') {{ va = va.toLowerCase(); vb = vb.toLowerCase(); }}
    if (va < vb) return sortAsc ? -1 : 1;
    if (va > vb) return sortAsc ? 1 : -1;
    return 0;
  }});

  // Assign ranks based on score desc (score rank, not sort rank)
  const scoreRanked = [...computedAreas].sort((a,b) => b.score - a.score);
  const rankMap = {{}};
  scoreRanked.forEach((a, i) => rankMap[a.area] = i + 1);

  renderTable(sorted, rankMap);
  updateStats(filtered);
  updateMapMarkers();
}}

function updateStats(filtered) {{
  const n = filtered.length;
  const top = [...filtered].sort((a,b) => b.score - a.score)[0];
  const bar = document.getElementById('statsBar');
  if (top) {{
    bar.innerHTML = `Showing <strong>${{n}}</strong> of <strong>65</strong> areas &nbsp;&middot;&nbsp; Top pick: <strong>${{top.area}}</strong> (<strong>${{top.score}}</strong>)`;
  }} else {{
    bar.innerHTML = `Showing <strong>0</strong> of <strong>65</strong> areas &mdash; no areas match current filters`;
  }}
}}

function renderTable(sorted, rankMap) {{
  if (!sorted) {{
    sorted = computedAreas;
    rankMap = {{}};
    const sr = [...computedAreas].sort((a,b) => b.score - a.score);
    sr.forEach((a,i) => rankMap[a.area] = i+1);
  }}

  const tbody = document.getElementById('tableBody');
  let html = '';

  sorted.forEach(a => {{
    const inFilter = filteredIds.has(a.area);
    const rank = rankMap[a.area] || '-';
    const sc = a.score;
    const col = scoreColor(sc);
    const rowClass = [
      a.status === 'Benchmark' ? 'row-benchmark' : (a.status === 'Contender' ? 'row-contender' : ''),
      a.area === selectedArea ? 'selected' : '',
      !inFilter ? 'filtered-out' : ''
    ].filter(Boolean).join(' ');

    const opacity = inFilter ? '' : 'opacity:0.35;';
    const both = a.both_u30
      ? '<span class="ok-tick">&#10003;</span>'
      : '<span class="no-tick">&#10007;</span>';

    html += `<tr class="${{rowClass}}" style="${{opacity}}" data-area="${{escHtml(a.area)}}" onclick="selectArea(this.dataset.area)">
      <td class="rank-cell">${{rank}}</td>
      <td><strong>${{escHtml(a.area)}}</strong></td>
      <td><span class="score-pill" style="background:${{col}};padding:2px 8px;border-radius:12px;color:white;font-size:0.8rem;font-weight:700;">${{sc}}</span></td>
      <td><span class="status-badge ${{a.status}}" style="font-size:0.7rem;">${{a.status}}</span></td>
      <td>${{escHtml(a.region)}}</td>
      <td>${{both}}</td>
      <td>${{a.her_kx_mins}} min</td>
      <td>${{a.him_city_mins}} min</td>
      <td>${{escHtml(a.strike_resilience)}}</td>
      <td>${{a.period_garden_flat_u2800 ? '<span class="ok-tick">&#10003;</span>' : '<span class="no-tick">&#10007;</span>'}}</td>
      <td>${{a.three_bed_u2800 ? '<span class="ok-tick">&#10003;</span>' : '<span class="no-tick">&#10007;</span>'}}</td>
      <td>${{a.cycling}}/5</td>
      <td>&pound;${{a.indicative_rent.toLocaleString()}}</td>
      <td>${{escHtml(a.crime_rate_band)}}</td>
      <td>${{escHtml(a.heathrow_noise)}}</td>
      <td>${{escHtml(a.area_trajectory)}}</td>
    </tr>`;
  }});

  tbody.innerHTML = html;

  // Update header sort indicators
  document.querySelectorAll('thead th').forEach(th => {{
    const col = th.dataset.col;
    th.classList.toggle('sort-active', col === sortCol);
    const arrow = col === sortCol ? (sortAsc ? ' &#9650;' : ' &#9660;') : '';
    th.innerHTML = th.textContent.replace(/ [▲▼]$/,'') + arrow;
  }});
}}

function escHtml(s) {{
  if (s == null) return '';
  return String(s)
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}}

function updateMapMarkers() {{
  if (!map) return;
  AREAS_DATA.forEach(a => {{
    const marker = markers[a.area];
    if (!marker) return;
    const computed = computedAreas.find(x => x.area === a.area);
    const sc = computed ? computed.score : a.score;
    const inFilter = filteredIds.has(a.area);
    const col = scoreColor(sc);
    const isSelected = a.area === selectedArea;
    const radius = a.status === 'Benchmark' ? 12 : 8;

    marker.setStyle({{
      fillColor: col,
      color: isSelected ? '#1A2744' : 'white',
      weight: isSelected ? 3 : 1.5,
      fillOpacity: inFilter ? 0.85 : 0.12,
      opacity: inFilter ? 1 : 0.25,
      radius: radius,
    }});
  }});
}}

function updateMapSelection() {{
  if (!map) return;
  const a = computedAreas.find(x => x.area === selectedArea);
  if (!a) return;
  const marker = markers[a.area];
  if (!marker) return;
  map.panTo([a.lat, a.lng], {{animate: true, duration: 0.5}});
  marker.openPopup();
  updateMapMarkers();
}}

function initMap() {{
  map = L.map('map', {{
    center: [51.505, -0.09],
    zoom: 11,
    zoomControl: true,
  }});

  L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19,
  }}).addTo(map);

  // Workplace star markers
  const starIcon = (label) => L.divIcon({{
    html: `<div style="font-size:22px;line-height:1;filter:drop-shadow(0 1px 2px rgba(0,0,0,0.4));">&#11088;</div><div style="font-size:10px;font-weight:600;background:rgba(255,255,255,0.92);padding:2px 5px;border-radius:4px;white-space:nowrap;margin-top:2px;color:#1A2744;">${{label}}</div>`,
    className: '',
    iconAnchor: [11, 11],
  }});

  L.marker([51.5308, -0.1238], {{icon: starIcon('Her office: King\'s Cross')}})
    .addTo(map)
    .bindPopup('<strong>Her office: King\'s Cross</strong>');

  L.marker([51.5175, -0.0886], {{icon: starIcon('His office: City')}})
    .addTo(map)
    .bindPopup('<strong>His office: City/Moorgate</strong>');

  // Area markers
  AREAS_DATA.forEach(a => {{
    const sc = a.score;
    const col = scoreColor(sc);
    const radius = a.status === 'Benchmark' ? 12 : 8;

    const marker = L.circleMarker([a.lat, a.lng], {{
      radius: radius,
      fillColor: col,
      color: 'white',
      weight: 1.5,
      fillOpacity: 0.85,
      opacity: 1,
    }}).addTo(map);

    marker.bindPopup(`
      <strong style="font-family:'Playfair Display',serif;font-size:1rem;">${{escHtml(a.area)}}</strong><br>
      <span style="font-size:0.8rem;color:#6B6B6B;">${{escHtml(a.postcode)}} &middot; ${{escHtml(a.region)}}</span><br>
      <span style="font-size:0.85rem;">Score: <strong style="color:${{col}}">${{sc}}</strong></span><br>
      <span style="font-size:0.8rem;">Her&rarr;KX: ${{a.her_kx_mins}}min | Him&rarr;City: ${{a.him_city_mins}}min</span>
    `);

    marker.on('click', () => selectArea(a.area));
    markers[a.area] = marker;
  }});
}}

function initControls() {{
  // Weight sliders
  ['commute','garden','bike','space','rent'].forEach(k => {{
    const sl = document.getElementById('sl-' + k);
    const sv = document.getElementById('sv-' + k);
    sl.addEventListener('input', () => {{
      weights[k] = parseInt(sl.value);
      sv.textContent = weights[k] + '%';
      updateWeightBars();
      recalcAll();
    }});
  }});

  // Filter controls
  const filterMap = [
    ['f-bothU30', 'bothU30', 'checkbox'],
    ['f-herBand', 'herBand', 'select'],
    ['f-himBand', 'himBand', 'select'],
    ['f-lineRes', 'lineRes', 'select'],
    ['f-strikeRes', 'strikeRes', 'select'],
    ['f-crowding', 'crowding', 'select'],
    ['f-nightTube', 'nightTube', 'checkbox'],
    ['f-crime', 'crime', 'select'],
    ['f-drugCrime', 'drugCrime', 'select'],
    ['f-socialHousing', 'socialHousing', 'select'],
    ['f-floodRisk', 'floodRisk', 'select'],
    ['f-heathrowNoise', 'heathrowNoise', 'select'],
    ['f-trajectory', 'trajectory', 'select'],
    ['f-periodGarden', 'periodGarden', 'checkbox'],
    ['f-threeBed', 'threeBed', 'checkbox'],
    ['f-bikeStorage', 'bikeStorage', 'select'],
    ['f-gymAccess', 'gymAccess', 'select'],
    ['f-twoGrocers', 'twoGrocers', 'checkbox'],
    ['f-bigPark', 'bigPark', 'checkbox'],
    ['f-status', 'status', 'select'],
    ['f-region', 'region', 'select'],
  ];

  filterMap.forEach(([id, key, type]) => {{
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('change', () => {{
      if (type === 'checkbox') {{
        filters[key] = el.checked;
      }} else {{
        filters[key] = el.value;
      }}
      recalcAll();
    }});
  }});

  // Rent slider
  const rentSl = document.getElementById('f-maxRent');
  const rentLbl = document.getElementById('rentValLabel');
  rentSl.addEventListener('input', () => {{
    filters.maxRent = parseInt(rentSl.value);
    rentLbl.textContent = 'Max: £' + parseInt(rentSl.value).toLocaleString();
    recalcAll();
  }});

  // Table header sort
  document.querySelectorAll('thead th').forEach(th => {{
    th.addEventListener('click', () => {{
      const col = th.dataset.col;
      if (!col) return;
      if (sortCol === col) {{
        sortAsc = !sortAsc;
      }} else {{
        sortCol = col;
        sortAsc = col !== 'score';
      }}
      recalcAll();
    }});
  }});
}}

document.addEventListener('DOMContentLoaded', () => {{
  computedAreas = AREAS_DATA.map(a => Object.assign({{}}, a));
  filteredIds = new Set(computedAreas.map(a => a.area));
  updateWeightBars();
  initMap();
  initControls();
  recalcAll();
}});
</script>
</body>
</html>"""

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Written {OUTPUT} ({len(html):,} bytes)")
