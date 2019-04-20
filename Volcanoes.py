import pandas
import folium
import numpy as np

html = """
<head">
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

data = pandas.read_csv("Volcanoes2.csv")

lat = list(data["LAT"])
lon = list(data["LON"])
names = list(data["Name"])
volc = list(data["Type"])
elev = list(data["Elevation"])

def colorelev(elev):
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

VolcanoMap = folium.Map(location=[39.38, -118.63], zoom_start = 4)
fg = folium.FeatureGroup(name="My Map")
for lat, lon, name, volc, elev in zip(lat, lon, names, volc, elev):
    iframe = folium.IFrame(html=html % (name, volc, elev), width=300, height=122)
    fg.add_child(folium.Marker(location=[lat, lon], popup=folium.Popup(iframe), icon=folium.Icon(color=colorelev(elev), icon='asterisk')))

VolcanoMap.add_child(fg)
VolcanoMap.save("VolcanoMap2.html")