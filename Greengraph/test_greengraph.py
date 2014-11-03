from greengraph import geolocate, map_at, is_green, count_green_in_png, show_green_in_png, location_sequence
from nose.tools import assert_equal, assert_raises, assert_true, assert_false, assert_almost_equal
import unittest

def test_geolocate():
    london_location = geolocate("London")
    assert_equal(london_location, (51.5073509, -0.1277583))
    
    
def test_map_at():
    map_response = map_at(51.5072, -0.1275, zoom=10)
    url = map_response.url
    assert_equal(url, 'http://maps.googleapis.com/maps/api/staticmap?style=feature%3Aall%7Celement%3Alabels%7Cvisibility%3Aoff&size=400x400&sensor=false&zoom=10&center=51.5072%2C-0.1275')
    
    
def test_is_green():
    rgb = (100, 111, 100)
    assert_true(is_green(*rgb))
    rgb = (100, 110, 100)
    assert_false(is_green(*rgb))
    
 
def test_count_green_in_png():
    london_location = (51.5073509, -0.1277583)
    assert_equal(count_green_in_png(map_at(*london_location)), 12004)
    
    
def test_show_green_in_png():
    pass
    
    
def test_location_sequence():
    london_location = (51.5073509, -0.1277583)
    birmingham_location = (52.486243, -1.890401)
    steps = 3
    expected_coords = [(51.507350899999999, -0.12775829999999999), (51.99679694999999, -1.0090796499999999), (52.486242999999988, -1.890401)]
    coords = location_sequence(london_location, birmingham_location, steps)
    
    for e_coords, coords in zip(expected_coords, coords):
        print e_coords, coords
        assert_almost_equal(e_coords, coords)
      