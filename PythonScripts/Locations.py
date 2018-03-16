import pandas as pd
from geopy.geocoders import Nominatim

geolocator = Nominatim()
surveyDF = pd.read_csv('/home/mapper/SurveyMonkey/MapTheSeas/AllResponses/Data_All_Responses_180315/CSV/Location.csv', skiprows=0-2, header=0)

locationsDF = surveyDF.iloc[1:, 6]
locationsDF = pd.DataFrame(locationsDF)
locationsDF.columns = ['Survey Response']
locationsDF.dropna(axis=0, how='all')


locationsDF["Latitude"] = None
locationsDF["Longitude"] = None

for index, row in locationsDF.iterrows():
    geolocator = Nominatim()
    location = geolocator.geocode(row[0])
    row[1] = location.latitude
    row[2] = location.longitude
    print(index)

