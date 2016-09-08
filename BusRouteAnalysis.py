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
import googlemaps

# Define class to hold data/info on a given bus route
class BusRoute(object):

    def __init__(self, **kwargs):
        self._set_options(**kwargs)
        self._import_data()

    def _set_options(self, route_number=10, dimensions=3, **kwargs):
        # set options/inputs
        self.filename = 'data\\route-locations\\route%d.kml'%(route_number)
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
        # Note: kwargs are just passed to numpy's built-in savetxt function

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
                  printout=False, key='default', other={}):
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
        other       Dict containing other kwargs passes to the gmaps api

    Outputs:
        distance    Distance in meters between the (first) origin and
                    destination pair
        duration    Time in seconds to travel between the (first) origin and
                    destination pair

    '''

    # handle inputs
    if key == 'default':
        key = 'AIzaSyCVQRazNBAG1qpTQooiHg7DCb2OJE3g4mA'
    params = {'units': units, 'mode': mode}
    params.update(other)
    pointA, pointB = [list(c) if (type(c) is tuple) else c for c in (pointA, pointB)]

    # make request
    gmaps = googlemaps.Client(key=key)
    res = gmaps.distance_matrix(pointA, pointB, **params)

    # interpret response to return distance & duration measures
    if res['status']=='OK':

        # print each result to the screen
        if printout:
            o = 0
            for A in res['origin_addresses']:
                d = 0
                for B in res['destination_addresses']:
                    print '%s to %s: %s (%s %s)'%(A, B, \
                        res['rows'][o]['elements'][d]['distance']['text'], \
                        res['rows'][o]['elements'][d]['duration']['text'], \
                        params['mode'])
                    d += 1
                o += 1

        # return the set of distances and durations
        distances = [[a['distance']['value'] for a in b['elements']] for b in res['rows']]
        durations = [[a['duration']['value'] for a in b['elements']] for b in res['rows']]
        return (distances, durations)

    else:
        print 'Oops! hit a problem: ', res['status']
        return None

# Example instance
kwargs = {'route_number': 10}
route = BusRoute(**kwargs)
route.show_route()

# example distance calculation
#dist, dur = distance_time(('Ithaca, NY', 'Ithaca, NY'), ('New York City', 'Lansing, NY'), printout=True)


# note to self:
# http://stackoverflow.com/questions/10871085/viewing-a-polygon-read-from-shapefile-with-matplotlib




