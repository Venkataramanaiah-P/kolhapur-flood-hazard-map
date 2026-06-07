# 🗺️ Kolhapur District — Multi-Criteria Flood Hazard Risk Map

**Tools:** Google Earth Engine | QGIS 3.40 | Python  
**CRS:** EPSG:32643 (WGS 84 / UTM Zone 43N)  
**Data:** Sentinel-1 SAR | SRTM DEM | WorldPop 2020 | Sentinel-2 | CHIRPS  

---

## 📌 Project Overview

This project produces a **publication-quality Multi-Criteria Flood Hazard Risk Map** of Kolhapur District, Maharashtra, India — using weighted overlay analysis on 5 geospatial datasets derived from Google Earth Engine.

The 2021 Kolhapur floods caused **52 deaths, displaced 4 lakh people, and caused ₹5,000 crore in damage**. This analysis identifies which areas are most vulnerable and why.

![Flood Hazard Map](exports/Kolhapur_P7_Final.png)

---

## 🎯 Objectives

- Extract and process multi-source geospatial data using Google Earth Engine
- Normalize all raster layers to a common 0–1 scale
- Apply weighted overlay analysis to generate a composite flood hazard index
- Classify hazard into 5 levels: Very Low → Low → Moderate → High → Very High
- Produce a professional cartographic layout for publication and reporting

---

## 🛰️ Data Sources

| Layer | Source | Resolution | GEE Dataset |
|---|---|---|---|
| DEM (Elevation) | SRTM (USGS/NASA) | 30m | `USGS/SRTMGL1_003` |
| Flood Extent (SAR) | Sentinel-1 (ESA) | 10m | `COPERNICUS/S1_GRD` |
| Population Density | WorldPop 2020 | 100m | `WorldPop/GP/100m/pop` |
| NDVI | Sentinel-2 (ESA) | 10m | `COPERNICUS/S2_SR` |
| Slope | Derived from SRTM | 30m | `ee.Terrain.slope()` |

---

## ⚖️ Weighted Overlay Methodology

| Factor | Weight | Rationale |
|---|---|---|
| DEM (Elevation) | **30%** | Low elevation = higher flood accumulation |
| Flood Extent SAR | **25%** | Actual 2021 flood footprint from Sentinel-1 |
| Population Density | **20%** | Higher population = greater exposure |
| Slope | **15%** | Flat terrain = slower drainage = higher risk |
| NDVI | **10%** | Low vegetation = less interception, more runoff |
| **Total** | **100%** | |

### Normalization Formula:
- **Standard:** `(value - min) / (max - min)`
- **Inverted (DEM, Slope, NDVI):** `1 - (value - min) / (max - min)`

### Weighted Overlay Formula (Raster Calculator):
```
(Flood_clip × 0.25) + (DEM_norm × 0.30) + (Pop_norm × 0.20) + (Slope_norm × 0.15) + (NDVI_norm × 0.10)
```

---

## 🗂️ Project Structure

```
Kolhapur_P7/
│
├── scripts/
│   ├── gee_p7_flood_hazard_export.py    # GEE export script (all 5 layers)
│   └── gee_p7_rainfall_export.py        # CHIRPS rainfall export
│
├── exports/
│   └── Kolhapur_P7_Final.png            # Final hazard map (300 DPI)
│
├── .gitignore                           # Excludes raw TIFs (>100MB)
└── README.md
```

---

## 📊 Key Findings

| Risk Zone | Location | Reason |
|---|---|---|
| 🔴 Very High | North Kolhapur plains | Flat terrain + dense population + 2021 SAR flood extent |
| 🟠 High | Karveer urban corridor | High population density + low elevation |
| 🟡 Moderate | Central transition zone | Mixed elevation and land cover |
| 🟢 Low | Eastern slopes | Higher elevation, lower density |
| 🟢 Very Low | Western Ghats (South) | High elevation + dense forest cover |

---

## 🖥️ Tools & Software

| Tool | Purpose |
|---|---|
| Google Earth Engine (Python API) | Data extraction and preprocessing |
| QGIS 3.40 (Bratislava) | Raster processing, weighted overlay, map layout |
| Python 3.12 | GEE scripting |
| Git / GitHub | Version control |

---

## 🔄 Workflow

```
GEE Python Script
      ↓
Export 5 TIF files → Google Drive
      ↓
Download to D:\GIS_Projects\Kolhapur_P7\Data\Raw\
      ↓
QGIS: Reproject → EPSG:32643
      ↓
QGIS: Clip to Kolhapur Boundary
      ↓
QGIS: Normalize each layer (0–1)
      ↓
QGIS: Raster Calculator → Weighted Overlay
      ↓
QGIS: Clip final raster to boundary
      ↓
QGIS: Symbology → YlOrRd, Quantile, 5 classes
      ↓
QGIS: Print Layout → A3 Landscape → Export 300 DPI
```

---

## 🗺️ Map Elements

- ✅ Title and subtitle
- ✅ 5-class YlOrRd hazard symbology
- ✅ Lat/Lon grid lines (0.25° interval)
- ✅ India location inset map
- ✅ Legend with class labels
- ✅ Weights table
- ✅ Scale bar (km)
- ✅ North arrow
- ✅ Data sources
- ✅ Projection information

---

## 👤 Author

**Venkataramanaiah Poliboyina**  
Survey Manager | L&T MAHSR (Bullet Train Project)  
GIS Analyst | 25 Years Civil Engineering Experience  

🔗 [GitHub](https://github.com/Venkataramanaiah-P)  
🔗 [LinkedIn](https://linkedin.com/in/venkataramanaiahpoliboyina)  
📧 ramanaiahpoliboyina@gmail.com  

---

## 📁 Related Projects

| # | Project | Link |
|---|---|---|
| P1 | GEE NDVI Mapping — Pune | GitHub |
| P2 | Time Series Analysis — Maharashtra | GitHub |
| P3 | LULC Classification — Random Forest | GitHub |
| P4 | Hospital Accessibility — Maharashtra | GitHub |
| P5 | PostGIS Urban Risk Analysis | GitHub |
| P6 | Kolhapur Flood Detection — SAR | GitHub |
| **P7** | **Kolhapur Flood Hazard Map** | **This repo** |

---

*Projection: WGS 84 / UTM Zone 43N (EPSG:32643) | Date: June 2026*
