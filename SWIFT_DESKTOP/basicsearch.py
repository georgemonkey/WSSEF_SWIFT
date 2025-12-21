import numpy as np
import matplotlib.pyplot as plt

def generate_basic_route(area_width, area_height, num_drones, sweep_spacing):

    routes = []
    
    # Divide area into horizontal strips, one per drone
    strip_height = area_height / num_drones
    
    for drone_id in range(num_drones):
        waypoints = []
        
        # Starting y-position for this drone's strip
        y_start = drone_id * strip_height
        y_end = (drone_id + 1) * strip_height
        
        # Generate lawnmower pattern within strip
        y = y_start
        x = 0
        going_right = True
        
        while y <= y_end:
            if going_right:
                waypoints.append([x, y])
                waypoints.append([area_width, y])
            else:
                waypoints.append([area_width, y])
                waypoints.append([x, y])
            
            y += sweep_spacing
            going_right = not going_right
        
        routes.append(np.array(waypoints))
    
    return routes


def visualize_routes(routes, area_width, area_height):
    """Plot the routes for visualization."""
    plt.figure(figsize=(10, 8))
    
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    
    for i, route in enumerate(routes):
        color = colors[i % len(colors)]
        plt.plot(route[:, 0], route[:, 1], 
                marker='o', markersize=3, 
                label=f'Drone {i+1}', 
                color=color, linewidth=2)
        
        # Mark start point
        plt.plot(route[0, 0], route[0, 1], 
                marker='s', markersize=10, 
                color=color, markeredgecolor='black', markeredgewidth=2)
    
    plt.xlim(-10, area_width + 10)
    plt.ylim(-10, area_height + 10)
    plt.xlabel('X (meters)')
    plt.ylabel('Y (meters)')
    plt.title('Basic Drone Search Routes (Square = Start)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    AREA_WIDTH = 10   # meters
    AREA_HEIGHT = 4  # meters
    NUM_DRONES = 6
    SWEEP_SPACING = 0.5  # meters between parallel sweeps

    # Visualize
    visualize_routes(generate_basic_route(AREA_WIDTH, AREA_HEIGHT, NUM_DRONES, SWEEP_SPACING), AREA_WIDTH, AREA_HEIGHT)