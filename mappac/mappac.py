#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
import numpy as np
import iris
import iris.coord_categorisation
import iris.quickplot as qplt
import cartopy
import cartopy.feature as cfeat
import cartopy.crs as ccrs
    
class Map:
    """
    Returns a heat map of oceanic currents
    """
    def __init__(self, data, **kwargs):
        self.data = data 
        self.params = {
           'latmin' : -91,
           'latmax' : 91,
           'longmin': -181,
           'longmax': 181,
        }
        self.params.update(kwargs)
        
        self.__load__()
        self.__define__()
        
    
    
    def __load__(self):
        """
        Loads gridded cubes from data source.
        """
        self.current_cube = iris.load(self.data)
        self.ocean_surface_meridonal_currents = self.current_cube[2]
        self.ocean_surface_zonal_currents = self.current_cube[0]
        
    
    
    def __define__(self):
        """
        Defines individual cubes for the zonal and meridonal directions that are gridded by longitude and latitude.
        """
       
        self.U_Meridonal = self.ocean_surface_meridonal_currents[0,0,:,:]
        self.V_Zonal = self.ocean_surface_zonal_currents[0,0,:,:]
        self.y = self.U_Meridonal.coord('latitude').points
        self.x = self.U_Meridonal.coord('longitude').points
         
            
              
    def zonal_map(self):
        """
        Creates a contour map of the speed of currents in the zonal direction. 
        """
        qplt.contourf(self.V_Zonal, 25)
        plt.gca().coastlines()
        plt.show()
            
            
    def meridonal_map(self):
        """
        Creates a contour map fo the speed of currents in the meridonal direction. 
        """
        qplt.contourf(self.U_Meridonal, 25)
        plt.gca().coastlines()
        plt.show()
        
    
    def current_map(self):
        """
        Creates a contour map of current speeds. Current speeds are calculated through vector math. 
        """
        
        # Calculates Current Speed
        currentspeed = (self.U_Meridonal ** 2 + self.V_Zonal ** 2) ** 0.5
        currentspeed.rename('currentspeed')

        # Creates a map with subsetted axes
        ax = plt.axes(projection = ccrs.PlateCarree())
        ax.set_xlim(self.params['longmin'],self.params['longmax'])
        ax.set_ylim(self.params['latmin'], self.params['latmax'])
        ax.coastlines()
        
        # Creates the contour map with 75 layers of depth
        qplt.contourf(currentspeed, 75)
        plt.title("Global Current Speed")
        qplt.show()   
