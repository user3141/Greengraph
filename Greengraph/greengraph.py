"""greengraph.pyplot
   Calculates the amount of green between London and Birmingham using google maps.
"""
import geopy
import requests
import png
from itertools import izip
from numpy import linspace
from StringIO import StringIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

########################################

def geolocate(place):
  """Return latitude and longitude of a place."""
  geocoder = geopy.geocoders.GoogleV3(domain="maps.google.co.uk")
  return geocoder.geocode(place, exactly_one=False)[0][1]

  
def map_at(lat, long, satellite=False, zoom=12, size=(400,400), sensor=False):
    """Get static map from google maps."""
    base = "http://maps.googleapis.com/maps/api/staticmap?"
    params = dict(
        sensor=str(sensor).lower(),
        zoom=zoom,
        size="x".join(map(str,size)),
        center=",".join(map(str,(lat,long))),
        style="feature:all|element:labels|visibility:off")
    if satellite:
        params["maptype"] = "satellite"
    return requests.get(base, params=params)

    
def is_green(r, g, b):
  """Is pixel green?"""
  threshold = 1.1
  return g > r*threshold and g > b*threshold


def count_green_in_png(data):
    """Count the number of green pixels in static map."""
    image = png.Reader(file=StringIO(data.content)).asRGB()
    count = 0
    for row in image[2]:
        pixels = izip(*[iter(row)]*3)
        count += sum(1 for pixel in pixels if is_green(*pixel))
    return count


def show_green_in_png(data):
    """Show only green parts of map"""
    image = png.Reader(file=StringIO(data.content)).asRGB()
    count = 0
    out = []
    for row in image[2]:
        outrow = []
        pixels = izip(*[iter(row)] * 3)
        for pixel in pixels:
            outrow.append(0)
            if is_green(*pixel):
                outrow.append(255)
            else:
                outrow.append(0)
            outrow.append(0)
        out.append(outrow)
    buffer = StringIO()
    result = png.from_array(out, mode='RGB')
    result.save(buffer)
    return buffer.getvalue()


def location_sequence(start, end, steps):
  """Coordinates on a line between start and end."""
  # Would actually prefer this if steps
  # were deduced from zoom level
  # But need projection code for that
  lats = linspace(start[0], end[0], steps)
  longs = linspace(start[1], end[1], steps)
  return zip(lats, longs)


def greengraph():
    """Produce a figure with the amount of green between London and Birmingham."""
    london_location = geolocate("London")
    
    with open('green.png','w') as green:
        green.write(show_green_in_png(map_at(*london_location, zoom=10, satellite=True)))
    green_spots = [count_green_in_png(map_at(*location, zoom=10, satellite=True))
                      for location in location_sequence(
                          geolocate("London"),
                          geolocate("Birmingham"), 10)]             
    print green_spots
    plt.plot(green_spots)
    plt.savefig('greengraph.png')

    
if __name__ == "__main__":
    greengraph()
