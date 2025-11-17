import requests

def get_location():
    try:
        response = requests.get('http://ip-api.com/json/')
        data = response.json()
        
        if data['status'] == 'success':
            lat = data.get('lat')
            lon = data.get('lon')
            return (lat, lon)
        else:
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    coords = get_location()
    if coords:
        lat, lon = coords
        print(f"Latitude: {lat}")
        print(f"Longitude: {lon}")
    else:
        print("Could not get coordinates")