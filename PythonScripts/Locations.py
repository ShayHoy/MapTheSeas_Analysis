''' Code used to process Question 2 of Map the Seas Survey. This code was written by Shannon Hoy to translate
 text responses from online survey into point locations. March 2018'''

# Import Necessary Libraries
import pandas as pd
from geopy.geocoders import Nominatim
from shapely.geometry import Point
import geopandas as gpd
import folium

# Geocode text to points using Nominatim geocoder
geolocator = Nominatim()
# Set up Pandas Data Frame
csv = '/home/mapper/SurveyMonkey/MapTheSeas/EditedData/Location.csv'
surveyDF = pd.read_csv(csv, skiprows=0-2, header=0)
locationsDF = surveyDF.iloc[1:, 6]
locationsDF = pd.DataFrame(locationsDF)
locationsDF.columns = ['Survey Response']
locationsDF.dropna(axis=0, how='all')
locationsDF["Latitude"] = None
locationsDF["Longitude"] = None
# Geocode Text Responses to Latitude and Longitude
for index, row in locationsDF.iterrows():
    geolocator = Nominatim()
    location = geolocator.geocode(row[0])
    row[1] = location.latitude
    row[2] = location.longitude
    print(index)
# Export CSV
locationsDF.to_csv('/home/mapper/SurveyMonkey/MapTheSeas/EditedData/Location_geocode.csv')

# Plot locations on Folium Map
# Set up locations
locations = locationsDF[['Latitude', 'Longitude']]
locationlist = locations.values.tolist()
labels = locationsDF['Survey Response'].values.tolist()
# Make Folium Map
map = folium.Map(location=[38.9, -77.05], tiles='CartoDB positron', zoom_start=11)

marker_cluster = folium.MarkerCluster().add_to(map)

for point in range(0, len(locationlist)):
    folium.Marker(locationlist[point], popup=folium.Popup(labels[point])).add_to(marker_cluster)
# Export Map
map.save('/home/mapper/SurveyMonkey/MapTheSeas/Products/LocationsMap.html')


# Export Locations to Shapefile
geometry = [Point(xy) for xy in zip(locationsDF.Longitude, locationsDF.Latitude)]
# Set coordinate system to WGS84
crs = {'init': 'epsg:4326'}
GDF = gpd.GeoDataFrame(locationsDF, crs=crs, geometry=geometry)
GDF.crs = {'init': 'epsg:4326'}
# Write Shapefile
GDF.to_file('/home/mapper/SurveyMonkey/MapTheSeas/Products/Locations.shp')
