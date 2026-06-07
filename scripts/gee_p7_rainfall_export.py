"""
=============================================================
P7 - Kolhapur Flood Hazard Map
GEE Export Script - CHIRPS Rainfall
Author: Venkataramanaiah Poliboyina
Date: June 2026
GitHub: github.com/Venkataramanaiah-P
=============================================================
Dataset: CHIRPS Daily Rainfall
Period: June - September 2021 (Monsoon season)
Scale: 50m (resampled from native 5566m)
CRS: EPSG:32643 (WGS 84 / UTM Zone 43N)
Output: Kolhapur_P7_Rainfall_v3.tif
=============================================================
NOTE: CHIRPS native resolution is ~5.5km (5566m).
Export at 50m scale for GIS overlay compatibility.
Mean rainfall value ~1280mm for Kolhapur monsoon season.
=============================================================
"""

import ee

# Authenticate and Initialize
ee.Authenticate()
ee.Initialize(project='your-gee-project-id')  # Replace with your project ID

# ─────────────────────────────────────────
# 1. DEFINE KOLHAPUR BOUNDARY
# ─────────────────────────────────────────
kolhapur = ee.FeatureCollection("FAO/GAUL/2015/level2") \
    .filter(ee.Filter.eq('ADM2_NAME', 'Kolhapur')) \
    .geometry()

print("Kolhapur boundary loaded.")

# ─────────────────────────────────────────
# 2. CHIRPS RAINFALL — Monsoon 2021
# ─────────────────────────────────────────
rainfall = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY') \
    .filterBounds(kolhapur) \
    .filterDate('2021-06-01', '2021-09-30') \
    .sum() \
    .clip(kolhapur) \
    .rename('rainfall')

# Validate — should print ~1280mm
stats = rainfall.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=kolhapur,
    scale=5566
).getInfo()

print(f"Mean monsoon rainfall: {stats}")
print(f"Expected: ~1280mm for Kolhapur 2021 monsoon")

# ─────────────────────────────────────────
# 3. EXPORT TO GOOGLE DRIVE
# ─────────────────────────────────────────
# NOTE: Export at 50m scale
# Native CHIRPS resolution is 5566m
# 50m gives ~1MB file suitable for weighted overlay

task = ee.batch.Export.image.toDrive(
    image=rainfall,
    description='Kolhapur_P7_Rainfall_v3',
    folder='Kolhapur_P7',
    fileNamePrefix='Kolhapur_P7_Rainfall_v3',
    region=kolhapur.bounds(),
    scale=50,
    crs='EPSG:32643',
    maxPixels=1e13,
    fileFormat='GeoTIFF'
)

task.start()
print("\n✅ Rainfall export started!")
print("Scale: 50m (resampled from CHIRPS 5566m native)")
print("Expected file size: ~1MB")
print("Check: https://code.earthengine.google.com/tasks")
print("Output: Google Drive → Kolhapur_P7/Kolhapur_P7_Rainfall_v3.tif")
