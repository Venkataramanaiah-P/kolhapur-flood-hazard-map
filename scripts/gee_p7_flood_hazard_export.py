"""
=============================================================
P7 - Kolhapur Multi-Criteria Flood Hazard Map
GEE Export Script - All 5 Layers
Author: Venkataramanaiah Poliboyina
Date: June 2026
GitHub: github.com/Venkataramanaiah-P
=============================================================
Layers Exported:
1. SRTM DEM (Elevation)
2. Sentinel-1 SAR Flood Extent (2021)
3. WorldPop Population Density (2020)
4. Sentinel-2 NDVI
5. Slope (derived from SRTM)

CRS: EPSG:32643 (WGS 84 / UTM Zone 43N)
Output Folder: Kolhapur_P7 (Google Drive)
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
# 2. DEM — SRTM 30m
# ─────────────────────────────────────────
dem = ee.Image('USGS/SRTMGL1_003') \
    .select('elevation') \
    .clip(kolhapur) \
    .rename('elevation')

print("DEM stats:", dem.reduceRegion(
    reducer=ee.Reducer.minMax(),
    geometry=kolhapur,
    scale=30
).getInfo())

# ─────────────────────────────────────────
# 3. SLOPE — Derived from SRTM
# ─────────────────────────────────────────
slope = ee.Terrain.slope(dem) \
    .clip(kolhapur) \
    .rename('slope')

print("Slope stats:", slope.reduceRegion(
    reducer=ee.Reducer.minMax(),
    geometry=kolhapur,
    scale=30
).getInfo())

# ─────────────────────────────────────────
# 4. FLOOD EXTENT — Sentinel-1 SAR (2021)
# ─────────────────────────────────────────
# July-August 2021 Kolhapur flood event
s1_before = ee.ImageCollection('COPERNICUS/S1_GRD') \
    .filterBounds(kolhapur) \
    .filterDate('2021-05-01', '2021-06-30') \
    .filter(ee.Filter.eq('instrumentMode', 'IW')) \
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
    .select('VV') \
    .mean()

s1_after = ee.ImageCollection('COPERNICUS/S1_GRD') \
    .filterBounds(kolhapur) \
    .filterDate('2021-07-20', '2021-08-20') \
    .filter(ee.Filter.eq('instrumentMode', 'IW')) \
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
    .select('VV') \
    .mean()

# Flood = areas where backscatter dropped significantly
flood_diff = s1_before.subtract(s1_after)
flood_extent = flood_diff.gt(3).clip(kolhapur).rename('flood_extent')

print("Flood extent stats:", flood_extent.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=kolhapur,
    scale=10
).getInfo())

# ─────────────────────────────────────────
# 5. POPULATION DENSITY — WorldPop 2020
# ─────────────────────────────────────────
population = ee.ImageCollection('WorldPop/GP/100m/pop') \
    .filter(ee.Filter.eq('country', 'IND')) \
    .filter(ee.Filter.eq('year', 2020)) \
    .first() \
    .clip(kolhapur) \
    .rename('population')

print("Population stats:", population.reduceRegion(
    reducer=ee.Reducer.minMax(),
    geometry=kolhapur,
    scale=100
).getInfo())

# ─────────────────────────────────────────
# 6. NDVI — Sentinel-2 (2021 pre-flood)
# ─────────────────────────────────────────
s2 = ee.ImageCollection('COPERNICUS/S2_SR') \
    .filterBounds(kolhapur) \
    .filterDate('2021-01-01', '2021-05-31') \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)) \
    .median()

ndvi = s2.normalizedDifference(['B8', 'B4']) \
    .clip(kolhapur) \
    .rename('ndvi')

print("NDVI stats:", ndvi.reduceRegion(
    reducer=ee.Reducer.minMax(),
    geometry=kolhapur,
    scale=10
).getInfo())

# ─────────────────────────────────────────
# 7. EXPORT ALL LAYERS TO GOOGLE DRIVE
# ─────────────────────────────────────────
export_params = [
    (dem,          'Kolhapur_P7_DEM',      30),
    (slope,        'Kolhapur_P7_Slope',    30),
    (flood_extent, 'Kolhapur_P7_Flood',    10),
    (population,   'Kolhapur_P7_WorldPop', 100),
    (ndvi,         'Kolhapur_P7_NDVI',     10),
]

tasks = []
for image, name, scale in export_params:
    task = ee.batch.Export.image.toDrive(
        image=image,
        description=name,
        folder='Kolhapur_P7',
        fileNamePrefix=name,
        region=kolhapur.bounds(),
        scale=scale,
        crs='EPSG:32643',
        maxPixels=1e13,
        fileFormat='GeoTIFF'
    )
    task.start()
    tasks.append((name, task))
    print(f"✅ Export started: {name} at {scale}m resolution")

print("\n🚀 All 5 export tasks started!")
print("Check progress: https://code.earthengine.google.com/tasks")
print("Output folder: Google Drive → Kolhapur_P7/")
