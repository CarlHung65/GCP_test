import googlemaps

gmaps = googlemaps.Client(key="AIzaSyD3_9x9JK7SZWIgNYP0izWScv6JT3otE2I")

geocode_result = gmaps.geocode("饒河夜市")

print(geocode_result)