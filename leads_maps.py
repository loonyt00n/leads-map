import requests

def get_static_map(api_key, origin, destination):
    # Define the base URL for the Static Maps API
    static_map_url = "https://maps.googleapis.com/maps/api/staticmap?"

    # Prepare parameters for the directions API
    directions_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
    
    # Get directions
    response = requests.get(directions_url)
    if response.status_code != 200:
        print("Error fetching directions:", response.json())
        return
    
    directions_data = response.json()
    
    # Extract encoded polyline from directions data
    if 'routes' not in directions_data or not directions_data['routes']:
        print("No routes found.")
        return
    
    polyline = directions_data['routes'][0]['overview_polyline']['points']
    
    # Define parameters for the static map
    map_params = {
        'size': '800x600',  # Size of the image
        'maptype': 'roadmap',
        'markers': f"color:blue|label:A|{origin}|color:red|label:B|{destination}",
        'path': f"enc:{polyline}",  # Encoded polyline for the route
        'key': api_key  # Your API key
    }
    
    # Create the full URL for the static map request
    map_request_url = static_map_url + '&'.join([f"{key}={value}" for key, value in map_params.items()])
    
    # Fetch the map image
    map_response = requests.get(map_request_url)
    
    if map_response.status_code == 200:
        # Save the image to a file
        with open('output/directions_map.png', 'wb') as f:
            f.write(map_response.content)
        print("Map image saved as 'directions_map.png'")
    else:
        print("Error fetching map image:", map_response.content)

# Example usage
if __name__ == "__main__":
    api_key = "<Google Static Maps API Key>"  # Replace with your actual API key
    origin = "40.7128,-74.0060"  # Latitude and longitude for New York City (Alice's location)
    destination = "34.0522,-118.2437"  # Latitude and longitude for Los Angeles (Bob's location)

    get_static_map(api_key, origin, destination)
