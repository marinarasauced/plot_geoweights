
import pgeocode
import numpy as np
from os import path
import pandas as pd

from modules.data import GeoWeightData, GeoWeightQuery

class GeoWeightLoader():
    """
    
    """
    def __init__(self, file_name):
        """
        
        """
        file_path = path.abspath(path.join(path.dirname(__file__), f"../data/{file_name}"))
        self.data = self.load_data(file_path)
        self.query = GeoWeightQuery()
        self.nomi = pgeocode.Nominatim("us")


    def load_data(self, file_path):
        """
        
        """
        file_data = pd.read_excel(file_path).to_numpy()
        data = GeoWeightData(file_data)
        return data
    

    def query_data(self):
        """
        
        """
        for zip in self.data.zip:
            query = self.nomi.query_postal_code(zip)
            data = query.to_numpy()
            self.query.query_append(data)
        self.query.query_format()
