#Note to reader: I'm sorry

import pandas
import folium
import numpy as np

#html for the popups
html = """
<head>
<h4 style="margin-bottom:0px; padding-top:10px;">Volcano information:</h4>
<p>
Name: %s <br>
Type: %s <br>
Elevation: %s meters<br>
</p>
</head>

<style>
* {
    font-family:Helvetica;
    font-size:16;
}

</style>"""

data = pandas.read_csv("Volcanoes2.csv") #Opens the csv and sets it to the data variable

lat = list(data["LAT"])
lon = list(data["LON"])
names = list(data["Name"])
volc = list(data["Type"])
elev = list(data["Elevation"]) #Sets each variable to a list of all the points in a given column

def colorelev(elev): #For later, returns a color based on the value of the elevation
    if elev <0:
        return "darkblue"
    if elev <=1000:
        return "green"
    elif elev <=2000:
        return "blue"
    elif elev <=3000:
        return "purple"
    elif elev <=4000:
        return "orange"
    elif elev <=6000:
        return "red"

VolcanoMap = folium.Map(location=[39.38, -118.63], zoom_start = 4) #Creates the basemap
fgVolc = folium.FeatureGroup(name="Volcanoes") #Creates a feature group for the volcanoes
fgPop = folium.FeatureGroup(name="Population") #Creates a feature group for the population map

fgPop.add_child(folium.GeoJson(data=open('world.json', 'r', encoding="utf-8-sig").read(), #(2 lines) Creates popualation map using a GeoJson (Don't ask how this works)
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

for lat, lon, name, volc, elev in zip(lat, lon, names, volc, elev): #Creates the volcano map and adds it to the fgVolc feature group
    iframe = folium.IFrame(html=html % (name, volc, elev), width=300, height=122)
    fgVolc.add_child(folium.CircleMarker(location=[lat, lon], popup=folium.Popup(iframe), radius=7, fill=True, color='grey', 
    fill_opacity=0.7, fill_color=colorelev(elev)))

VolcanoMap.add_child(fgPop) #Adds population map to the final map
VolcanoMap.add_child(fgVolc) #Adds volcanoes to the final map
VolcanoMap.add_child(folium.LayerControl()) #Adds layer control, where you can toggle feature groups
VolcanoMap.save("VolcanoMap2.html") #Saves the map as an html file