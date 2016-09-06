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

    def show_map(self):
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
    # calculate how many rows and preallocate output
    string = string.strip().split(' ')
    num_rows = len(string)
    array = np.empty((num_rows, num_cols))

    # convert from string to float
    for rr in xrange(num_rows):
        row = string[rr].split(',')
        for cc in xrange(num_cols):
            array[rr][cc] = float(row[cc])
    return array

# Example instance
kwargs = {
    'filename':'data\\route-locations\\route10.kml'
    }
test = BusRoute(**kwargs)
test.show_map()


# note to self:
# http://stackoverflow.com/questions/10871085/viewing-a-polygon-read-from-shapefile-with-matplotlib


## Interpret & analyze address
#from pygeocoder import Geocoder
#address = Geocoder.geocode("102 W Falls, Ithaca")
#
## print full address info
#data = address.data[0]
#
#def dict_print(data, pre):
#    for k, v in data.iteritems():
#        if isinstance(v, dict):
#            dict_print(v, pre + ' > ' + k)
#
#        elif isinstance(v, list):
#            c = 0
#            for i in v:
#                if isinstance(i, dict):
#                    dict_print(i, pre + ' > ' + k + ' (%d)'%c)
#                else:
#                    print pre + ' > ' + k + ' (%d) > '%c + str(i)
#                c = c+1;
#        else:
#            print pre+' > ' + k + ' > ' + str(v)
#
#dict_print(data, 'data')
#




