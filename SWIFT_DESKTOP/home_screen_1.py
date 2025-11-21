import tkinter as tk
from tkinter import ttk
import tkintermapview as tkmap
import requests

# Setup window
root = tk.Tk()
root.title("Geofence Creator")
root.geometry("1000x700")

# Store points
points = []
markers = []
drawing = False
polygon = None

# Create map
map_widget = tkmap.TkinterMapView(root, corner_radius=0)
map_widget.pack(fill=tk.BOTH, expand=True)
map_widget.set_position(40.7128, -74.0060)
map_widget.set_zoom(12)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

def click_map(coords):
    global polygon
    if not drawing:
        return

    lat, lon = coords
    points.append((lat, lon))

    marker = map_widget.set_marker(lat, lon, text="", marker_color_circle="red", marker_color_outside="white")
    markers.append(marker)

    # reorder points to avoid self‑intersection
    if len(points) >= 3:
        # compute centroid
        cx = sum(p[0] for p in points) / len(points)
        cy = sum(p[1] for p in points) / len(points)

        # sort points by angle
        import math
        ordered = sorted(points, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
    else:
        ordered = points

    if polygon:
        polygon.delete()

    if len(ordered) >= 3:
        polygon = map_widget.set_path(ordered + [ordered[0]], color="yellow", width=3)
    else:
        polygon = map_widget.set_path(ordered, color="yellow", width=3)

def toggle_draw():
    global drawing
    drawing = not drawing
    btn_draw.config(text="Stop" if drawing else "Draw")

def clear():
    global polygon, points, markers
    points = []
    markers = []
    if polygon:
        polygon.delete()
    for marker in map_widget.canvas_marker_list:
        marker.delete()


def go_location():
    try:
        lat = float(entry_lat.get())
        lon = float(entry_lon.get())
        map_widget.set_position(lat, lon) 
        map_widget.set_zoom(14)
    except:
        pass


def auto_locate():
    try:
        data = requests.get("https://ipinfo.io/json").json()
        lat, lon = map(float, data["loc"].split(","))
        entry_lat.delete(0, tk.END)
        entry_lat.insert(0, str(lat))
        entry_lon.delete(0, tk.END)
        entry_lon.insert(0, str(lon))
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(14)
    except:
        print("could not auto detect location")

# Area calculation function
def geofence_area_ft2():
    if len(points) < 3:
        return 0.0

    # compute area with the shoelace formula
    area = 0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        area += x1 * y2 - x2 * y1

    area = abs(area) / 2

    # rough conversion assuming degrees to feet (not accurate but simple)
    # 1 degree lat ≈ 364000 ft, 1 degree lon ≈ 288200 ft at mid‑latitudes
    converted_area = area * (364000 * 288200)

    return converted_area

# Top bar
frame = ttk.Frame(root)
frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

btn_draw = ttk.Button(frame, text="Draw", command=toggle_draw, width=8)
btn_draw.pack(side=tk.LEFT, padx=5)

ttk.Button(frame, text="Clear", command=clear, width=8).pack(side=tk.LEFT, padx=5)

ttk.Label(frame, text="Lat:").pack(side=tk.LEFT, padx=(20,5))
entry_lat = ttk.Entry(frame, width=12)
entry_lat.pack(side=tk.LEFT, padx=5)
entry_lat.insert(0, "40.7128")

ttk.Label(frame, text="Lon:").pack(side=tk.LEFT, padx=5)
entry_lon = ttk.Entry(frame, width=12)
entry_lon.pack(side=tk.LEFT, padx=5)
entry_lon.insert(0, "-74.0060")

ttk.Button(frame, text="Go", command=go_location, width=6).pack(side=tk.LEFT, padx=5)
ttk.Button(frame, text="Auto‑Locate", command=auto_locate, width=10).pack(side=tk.LEFT, padx=5)

map_widget.add_left_click_map_command(click_map)

root.mainloop()