'''
Class to hold bus route info
- Read from KML
- Save to CSV
- Show route on a map
'''

# Imports
from bs4 import BeautifulSoup as BS
from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
import urllib2
import urllib
import json

# Define class to hold data/info on a given bus route
class BusRoute(object):

    def __init__(self, **kwargs):
        self._set_options(**kwargs)
        self._import_data()

    def _set_options(self, filename=None, dimensions=3, **kwargs):
        # set options/inputs
        self.filename = filename
        self.dimensions = dimensions

    def _import_data(self):
        # open the source KML file, ask for a new file if invalid
        if self.filename is None:
            Tk().withdraw() # keep the root window from appearing
            self.filename = askopenfilename()
        try:
            f = open(self.filename, 'r')
        except IOError:
            Tk().withdraw() # keep the root window from appearing
            self.filename = askopenfilename()
            f = open(self.filename, 'r')
        self.KMLdata = BS(f)
        f.close()

        # extract coordinate data from KML and convert to array
        coords_str = unicode(self.KMLdata.find(name='coordinates').contents[0])
        self.coordinates = _unicode_to_array(coords_str, num_cols=self.dimensions)

    def saveas_csv(self, filename=None, **kwargs):
        '''
        Save bus route coordinate data (lat, longitude, 0) as a csv file
        '''
        # Noe: kwargs are just passed to numpy's built-in savetxt function

        # get filename
        if filename is None:
            Tk().withdraw() # keep the root window from appearing
            filename = asksaveasfilename()

        # save using numpy's built-in function
        np.savetxt(filename, self.coordinates, **kwargs)

    def show_route(self):
        '''
        Display route on a map
        '''

        # plot basemap w/ state and county lines, etc
        fig = plt.figure()
        m = Basemap(llcrnrlon=-76.8, llcrnrlat=42.2, urcrnrlon=-76.2, \
            urcrnrlat=42.7, rsphere=(6378137.00,6356752.3142), resolution='l', \
            projection='merc')
        m.shadedrelief()
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()
        m.drawcounties()

        # plot route coordinates
        m.plot(self.coordinates[:,0], self.coordinates[:,1], 'k.-',
               latlon=True)

        # finalize and show plot
        fig.show()


# Other functions
def _unicode_to_array(string, num_cols=3):
    '''
    Take a string with coordinates in the form "lat,lon,0 "*N
    and return an N-by-3 numpy array containing the coordinates as floats
    '''
    #
    string = string.strip().split(' ')
    num_rows = len(string)

    # calculate how many rows and preallocate output
    array = np.empty((num_rows, num_cols), dtype=float)

    # convert from string to float
    for rr in xrange(num_rows):
        row = string[rr].split(',')
        for cc in xrange(num_cols):
            array[rr][cc] = float(row[cc])
    return array

def distance_time(pointA, pointB, units='imperial', mode='walking',
                  printout=False, key='default'):
    '''
    Use googlemaps API to return the distance (in meters) and travel time (in
    seconds) from the addresses or coordinate pairs in pointA to the addresses
    or coordinate pairs in pointB. Additional optional kwargs are used to set
    API parameters.

    Inputs:
        pointA      String or tuple of strings or (lat,lon) pairs specifying
                    origin address(es)
        pointB      String or tuple of strings or (lat,lon) pairs specifying
                    destination address(es)

    KWargs:
        units       'imperial' or 'metric', specifying the units for printed
                    quantities only. Default is 'imperial'
        mode        Mode of transportation, see googlemaps distance matrix API
                    documentation for a complete list of options. Default is
                    'walking'
        key         Key used for gaining API access. Default is [hidden]
        printout    Boolean specifying if the distance and time results should
                    be printed to the screen. Default is False

    Outputs:
        distance    Distance in meters between the (first) origin and
                    destination pair
        duration    Time in seconds to travel between the (first) origin and
                    destination pair

    '''
    # format url request of googlemaps api
    api_name = 'distancematrix'
    if key == 'default':
        key = 'AIzaSyCVQRazNBAG1qpTQooiHg7DCb2OJE3g4mA'
    params = {'origins': pointA, 'destinations': pointB, 'units': units,
              'mode': mode, 'key': key}
    base = 'https://maps.googleapis.com/maps/api/{0}/json?'.format(api_name)
    url = base + urllib.urlencode(params)

    # make url request and grab the distance & duration measures from the result
    response = urllib2.urlopen(url)
    html = response.read()
    out = json.loads(html)
    origin = out['origin_addresses'][0]
    destination = out['destination_addresses'][0]
    distance = out['rows'][0]['elements'][0]['distance']['value']
    distance_str = out['rows'][0]['elements'][0]['distance']['text']
    duration = out['rows'][0]['elements'][0]['duration']['value']
    duration_str = out['rows'][0]['elements'][0]['duration']['text']

    # display the result
    if printout:
        print '%s to %s: %s (%s %s)'%(
            origin, destination, distance_str, duration_str, params['mode'])

    # return the result
    return (distance, duration)


# Example instance
kwargs = {
    'filename':'data\\route-locations\\route10.kml'
    }
route10 = BusRoute(**kwargs)
route10.show_route()

# example distance calculation
distance_time('Ithaca, NY', 'Lansing, NY', printout=True)


# note to self:
# http://stackoverflow.com/questions/10871085/viewing-a-polygon-read-from-shapefile-with-matplotlib




