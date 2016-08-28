'''
Class to hold bus route info
- Read from KML
- Save to CSV
'''

# Imports
from bs4 import BeautifulSoup as BS
from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
import numpy as np

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

        # extract coordinate data from KML
        coords_str = unicode(self.KMLdata.find(name='coordinates').contents[0])
        coords_str = coords_str.split(' ')
        num_cols = self.dimensions
        num_rows = len(coords_str) / num_cols

        # convert from string to float
        self.coordinates = np.empty((num_rows, num_cols))
        for rr in xrange(num_rows):
            row = coords_str[rr].split(',')
            for cc in xrange(num_cols):
                self.coordinates[rr][cc] = float(row[cc])

    def saveas_csv(self, filename=None, **kwargs):
        # Noe: kwargs are just passed to numpy's built-in savetxt function

        # get filename
        if filename is None:
            Tk().withdraw() # keep the root window from appearing
            filename = asksaveasfilename()

        # save using numpy's built-in function
        np.savetxt(filename, self.coordinates, **kwargs)

# Example instance
kwargs = {
    'filename':'D:\\Users\\Lena\\Documents\\projects\\bus_routes_tcat\\bus_routes\\data\\route-locations\\route10.kml'
    }
test = BusRoute(**kwargs)
test.saveas_csv()







































