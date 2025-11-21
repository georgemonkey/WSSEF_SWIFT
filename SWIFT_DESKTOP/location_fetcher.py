import requests

def get_location():
    import requests

    response = requests.get('https://ipapi.co/json/')
    data = response.json()

    lat = data['latitude']
    lon = data['longitude']
    return lat, lon