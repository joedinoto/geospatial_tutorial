#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 17:11:12 2024

@author: linuxlaptop
"""
# following instructions from
# https://towardsdatascience.com/visualizing-geospatial-data-in-python-e070374fe621

# Import Packages
import geoplot as gplt
import geopandas as gpd
import geoplot.crs as gcrs
import imageio
import pandas as pd
import matplotlib.pyplot as plt
import mapclassify as mc
import numpy as np
import seaborn as sns

# load the shapefile
usa = gpd.read_file("maps/cb_2018_us_state_20m.shp")
usa.head()

# load US Census data as a pandas dataframe
state_pop = pd.read_csv("data/nst-est2018-alldata.csv")
state_pop.head()

# merge shapefile with population data
# join on state names

pop_states = usa.merge(state_pop, left_on="NAME", right_on = "NAME")
pop_states.head()

# plot shapes by specifying state names
pop_states[pop_states.NAME=="California"].plot()
pop_states[pop_states.NAME=="Alabama"].plot()

# plot a map of the USA
path = gplt.datasets.get_path("contiguous_usa")
contiguous_usa = gpd.read_file(path)
gplt.polyplot(contiguous_usa)

# load data for US cities
path = gplt.datasets.get_path("usa_cities")
usa_cities = gpd.read_file(path)

# plot the locations of the cities
continental_usa_cities = usa_cities.query('STATE not in ["HI","AK","PR"]')
gplt.pointplot(continental_usa_cities)

# overplot the state outlines and cities into one map
#ax = gplt.polyplot(contiguous_usa) # stretched out
# use Albers Equal Area projection instead
ax = gplt.polyplot(contiguous_usa, projection=gcrs.AlbersEqualArea())
gplt.pointplot(continental_usa_cities, ax=ax)

# hue = city's elevation, add a legend to interpret the hue
ax = gplt.polyplot(contiguous_usa, projection = gcrs.AlbersEqualArea())
gplt.pointplot(
    continental_usa_cities,
    ax = ax,
    hue = "ELEV_IN_FT",
    legend = True)

# radius of point = elevation of city
ax = gplt.polyplot(
    contiguous_usa,
    edgecolor = "white",
    facecolor = "lightgray",
    figsize = (12,8),
    projection = gcrs.AlbersEqualArea()
    )

gplt.pointplot(
    continental_usa_cities,
    ax = ax,
    hue = "ELEV_IN_FT",
    cmap = "Blues",
    scheme = "quantiles",
    scale = "ELEV_IN_FT",
    limits = (1,10),
    legend = True,
    legend_var = "scale",
    legend_kwargs={"frameon": False},
    legend_values = [-110,1750,3600,5500,7400],
    legend_labels = ["-110 ft","1750 ft","3600 ft", "5500 ft", "7400 ft"]
    )

ax.set_title("Cities in the continental USA, by elevation", fontsize = 16)

# use choropleth for state population
ax = gplt.polyplot(contiguous_usa, projection = gcrs.AlbersEqualArea())
gplt.choropleth(
    contiguous_usa,
    hue = "population",
    edgecolor = "white",
    linewidth = 1,
    cmap = "Greens",
    legend = True,
    scheme = "FisherJenks",
    legend_labels = ["< 3m", "3m-6.7m", "6.7m-12.8m", "12.8m-25m", "25-37m"],
    projection = gcrs.AlbersEqualArea(),
    ax = ax
    )

# =============================================================================
# for some reason this did not work. I went to microsoft copilot and it worked
# CTRL 4 to comment a block of code
# # kernel densinty estimate (KDE) for contours on traffic collisions in NYC
# boroughs = gpd.read_file(gplt.datasets.get_path("nyc_boroughs"))
# collisions = gpd.read_file(gplt.datasets.get_path("nyc_collision_factors"))
# ax = gplt.polyplot(boroughs, projection = gcrs.AlbersEqualArea())
# gplt.kdeplot(
#     collisions, 
#     cmap="Reds", 
#     fill = True, 
#     clip = boroughs, 
#     #projection = gcrs.AlbersEqualArea(),
#     ax = ax
#     )
# =============================================================================


# Load datasets
boroughs = gpd.read_file(gplt.datasets.get_path("nyc_boroughs"))
collisions = gpd.read_file(gplt.datasets.get_path("nyc_collision_factors"))

# Plot boroughs
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
boroughs.plot(ax=ax, color='white', edgecolor='black')

# Extract coordinates from collisions
collisions['coords'] = collisions['geometry'].apply(lambda x: x.coords[0])
collisions_df = pd.DataFrame(
    collisions['coords'].to_list(), 
    columns=['Longitude', 'Latitude']
    )

# Plot KDE for the boroughs of NYC
sns.kdeplot(
    data=collisions_df, 
    x='Longitude', y='Latitude',
    fill=True, 
    cmap='Reds', 
    ax=ax
)

plt.title("KDE of Collisions in NYC Boroughs")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

# =============================================================================
# # KDE for major US Population centers
# ax = gplt.polyplot(
#     contiguous_usa, 
#     projection = gcrs.AlbersEqualArea()
#     )
# 
# gplt.kdeplot(
#     continental_usa_cities,
#     x = 'LONGITUDE', y = "LATITUDE",
#     cmap = "Reds",
#     shade = True,
#     clip = contiguous_usa,
#     ax = ax
#     )
# 
# =============================================================================
# =============================================================================
# 
# # Plot the USA map with AlbersEqualArea projection
# fig, ax = plt.subplots(1, 1, figsize=(15, 15), subplot_kw={'projection': gcrs.AlbersEqualArea()})
# gplt.polyplot(contiguous_usa, ax=ax)
# 
# # Plot KDE for major US population centers
# gplt.kdeplot(
#     continental_usa_cities,
#     cmap='Reds',
#     fill=True,
#     clip=contiguous_usa,
#     ax=ax
# )
# 
# plt.title("KDE of Major US Population Centers")
# plt.show()
# 
# =============================================================================

# Load datasets
contiguous_usa = gpd.read_file(gplt.datasets.get_path("contiguous_usa"))
usa_cities = gpd.read_file(gplt.datasets.get_path("usa_cities"))

# Filter out non-continental US cities
continental_usa_cities = usa_cities.query('STATE not in ["HI", "AK", "PR"]')

# Extract coordinates from cities
continental_usa_cities['Longitude'] = continental_usa_cities.geometry.x
continental_usa_cities['Latitude'] = continental_usa_cities.geometry.y
cities_df = continental_usa_cities[['Longitude', 'Latitude']]

# Plot the USA map
fig, ax = plt.subplots(figsize=(15, 15))
contiguous_usa.plot(ax=ax, color='white', edgecolor='black')

# Plot KDE
sns.kdeplot(
    data=cities_df,
    x='Longitude', y='Latitude',
    fill=True, alpha = .5,
    cmap='Reds',
    ax=ax
)

plt.title("KDE of Major US Population Centers")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

# inspecting obesity rates
obesity = pd.read_csv(
    gplt.datasets.get_path("obesity_by_state"), 
    sep="\t"
    )
obesity.head()

# convert to GeoDataFrame using joins. 
geo_obesity = contiguous_usa.set_index("state").join(obesity.set_index("State"))
geo_obesity.head()

# plot obesity rates using a cartogram
gplt.cartogram(
    geo_obesity,
    scale="Percent",
    projection=gcrs.AlbersEqualArea()
    )

# bin data into quantiles (k = 10)
scheme = mc.Quantiles(continental_usa_cities["ELEV_IN_FT"], k = 10)

# assign a hue to each of the 10 quantiles
gplt.pointplot(
    continental_usa_cities,
    projection = gcrs.AlbersEqualArea(),
    hue = "ELEV_IN_FT",
    scheme = scheme,
    cmap = "inferno_r",
    legend = True
    )

# add a filter for warnings (why?)
# appears fo ignore warnings about NaNs?
import warnings
warnings.filterwarnings("ignore", "GeoSeries.isna", UserWarning)

# use a voronoi map to analyze 
# primary school clustering in Melbourne, Australia
melbourne = gpd.read_file(gplt.datasets.get_path("melbourne"))
df = gpd.read_file(gplt.datasets.get_path("melbourne_schools"))
# the syntax of df.query() involves single quotes and double quotes
melbourne_primary_schools = df.query('School_Type == "Primary"')

ax = gplt.voronoi(
    melbourne_primary_schools,
    clip = melbourne,
    linewidth = 0.5,
    edgecolor = "white",
    projection = gcrs.Mercator() # why Mercator and not Albers?
    # answer, Albers stretches horizontally and squashes vertically
    )

gplt.polyplot(
    melbourne,
    edgecolor = "None",
    facecolor = "lightgray",
    ax = ax
    )

gplt.pointplot(
    melbourne_primary_schools,
    color = "black",
    ax = ax,
    s = 1,
    extent = melbourne.total_bounds
    )

plt.title("Primary schools in Greater Melbourne, 2018")