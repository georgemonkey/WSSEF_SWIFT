
import tkinter as tk
from tkintermapview import TkinterMapView
from tkinter import *
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my_geocoder_app")
root=tk.Tk()
root.geometry("500x500")

map_widget = TkinterMapView(root, width=800, height=600, corner_radius=0)
map_widget.pack(fill="both", expand=True)   

address = "Eiffel Tower, Paris, France"
location = geolocator.geocode(address)
print(address)
print(location.latitude)
print(location.longitude)
map_widget.set_position(location.latitude,location.longitude) # Los Angeles coordinates

root.mainloop()



