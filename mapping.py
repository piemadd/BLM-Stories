import geocoder

def getLoc(addy):
	g = geocoder.osm(addy)
	results = g.osm
	lon = results['y']
	lat = results['x']
	return lon, lat
