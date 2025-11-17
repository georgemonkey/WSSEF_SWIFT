import tkinter as tk
from tkintermapview import TkinterMapView
from location_fetcher import get_location

def open_map():
    map_win = tk.Toplevel()
    map_win.geometry("800x800")
    map_win["bg"] = "black"
    map_win.attributes("-alpha",0.95)
    geofence_button = tk.Button(map_win, text = "Create Geofence",width=10,height=3)
    geofence_button.pack()
    map_widget = TkinterMapView(map_win,width=800,height = 600,corner_radius=0)
    map_widget.pack(fill = "both",expand=True)
    map_widget.set_position(get_location)
    print(get_location)
    map_widget.set_zoom(15)

    map_win.mainloop()


root = tk.Tk()
root.geometry("500x500")
root["bg"] = "black"
root.attributes("-alpha",0.85)
frame1 = tk.Frame(root, bg = "red", bd = 5)
frame1.place(x=50,y=0)

map_button = tk.Button(frame1, text = "2D Map",command=open_map)
# map_button.pack()
map_button.grid(row=0,column=0)
root.mainloop()