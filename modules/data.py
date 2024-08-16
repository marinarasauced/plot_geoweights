
import numpy as np
import pandas as pd


class GeoWeightData():
    """
    
    """
    def __init__(self, data):
        """
        
        """
        self.zip = data[:, 0]
        self.units = data[:, 1]
        self.quintile = data[:, 2]


class GeoWeightQuery():
    """
    
    """
    def __init__(self):
        """
        
        """
        self.postal_code = []
        self.country_code = []
        self.place_name = []
        self.state_name = []
        self.state_code = []
        self.county_name = []
        # self.county_code = []
        # self.community_name = []
        # self.community_code = []
        self.latitude = []
        self.longitude = []
        self.accuracy = []

    
    def query_append(self, data):
        """
        
        """
        self.postal_code.append(data[0])
        self.country_code.append(data[1])
        self.place_name.append(data[2])
        self.state_name.append(data[3])
        self.state_code.append(data[4])
        self.county_name.append(data[5])
        # self.county_code.append(data[6])
        # self.community_name.append(data[7])
        # self.community_code.append(data[8])
        self.latitude.append(data[9])
        self.longitude.append(data[10])
        self.accuracy.append(data[11])


    def query_format(self):
        """
        
        """
        self.postal_code = np.asarray(self.postal_code, dtype=str)
        self.postal_code = np.array([code.zfill(5) for code in self.postal_code])
        self.county_code = np.asarray(self.country_code, dtype=str)
        self.place_name = np.asarray(self.place_name, dtype=str)
        self.state_name = np.asarray(self.state_name, dtype=str)
        self.state_code = np.asarray(self.state_code, dtype=str)
        self.county_name = np.asarray(self.county_name, dtype=str)
        # self.county_code = np.asarray(self.county_code, dtype=str)
        # self.community_name = np.asarray(self.community_name, dtype=str)
        # self.community_code = np.asarray(self.community_code, dtype=str)
        self.latitude = np.asarray(self.latitude, dtype=np.float64)
        self.longitude = np.asarray(self.longitude, dtype=np.float64)
        self.accuracy = np.asarray(self.accuracy, dtype=np.float64)


