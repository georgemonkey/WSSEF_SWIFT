from geopy.geocoders import Nominatim
import tkinter as tk
from tkintermapview import TkinterMapView
from tkinter import Image, Label, StringVar, messagebox
from shapely.geometry import Polygon
from pyproj import CRS, Transformer



def calculate_area(lat_long, target_epsg = "EPSG:3857"):
    source_crs = CRS("EPSG:4326")
    target_crs = CRS(target_epsg)
    transformer = Transformer.from_crs(source_crs,target_crs,always_xy=True)
    projected_points = [transformer.transform(lon,lat) for lat,lon in lat_long]
    polygon = Polygon(projected_points)
    area = polygon.area
    return area

def map_click(coordinates_tuple):
    global list1
    print(coordinates_tuple)
    list1.append(coordinates_tuple)
    print(list1)
    
    if len(list1)>=2:
        path1 = map_widget.set_polygon(list1,fill_color = None, border_width = 5,outline_color="red")
def area1():
    area = calculate_area(list1)
    print("area of selected polygon in sq meters: ", area)


geolocator = Nominatim(user_agent="my_geocoder_app")
list1 = []
def f1():
    global map_widget
    
    print(searchType)
    map_win=tk.Toplevel()
    b2=tk.Button(map_win,text="geofence", command=area1)
    b2.pack()
    map_widget = TkinterMapView(map_win, width=800, height=600, corner_radius=0)
    map_widget.pack(fill="both", expand=True)   
    if searchType.get() == "AD":
        address = t3.get("0.0","end")
        location = geolocator.geocode(address)
        map_widget.set_position(location.latitude,location.longitude)
        map_widget.add_left_click_map_command(map_click)

        
    elif searchType.get() == "LL":
        lat = float(t1.get())
        long = float(t2.get())
        map_widget.set_position(lat,long)
        coordinates = f"{lat},{long}"
        location = geolocator.reverse(coordinates) 
        address1 = location.address
        location = geolocator.geocode(address1)
        map_widget.set_position(location.latitude,location.longitude)
        map_widget.add_left_click_map_command(map_click)
    else:
        print("error please try selecting an option")
    
    map_widget.set_zoom(15)

    map_win.mainloop()
#TkinterMapView.add_left_click_map_command(label = "")


root=tk.Tk()
root.geometry("500x500")
frame1=tk.Frame(root,bd=5)
frame1.place(x=0,y=0)
b1=tk.Button(frame1,text="Map",command=f1)
b1.grid(row=8,column=3)

l1 = tk.Label(frame1,text="Latitude")
l1.grid(row=1,column=3)
t1 = tk.Entry(frame1)
t1.grid(row=1,column=4)


l2 = tk.Label(frame1,text="Longitude")
l2.grid(row=3,column=3)
t2 = tk.Entry(frame1)
t2.grid(row=3,column=4)

l3 = tk.Label(frame1,text="Address")
l3.grid(row=5,column=3)
t3 = tk.Text(frame1, width=25,height = 5)
t3.grid(row=5,column=4)
searchType = StringVar()
rb1 = tk.Radiobutton(frame1,text="Lat/Long",variable=searchType, value="LL")
rb1.grid(row=7,column=3)

rb2 = tk.Radiobutton(frame1,text="Address",variable=searchType, value="AD")
rb2.grid(row=7,column=4)




#62,361.06 m
#
#30,766.01 m²
root.mainloop()



