import numpy as np
import pandas as pd

from utils import cases_df, counties_df, statistic_list, get_distance
from us_state_abbrev import us_state_abbrev

class CovidTrace:
    """
    Class that narrows COVID cases to a specified mile-radius within a specified county.

    Parameters
    ----------
    US_county : str
        The county name specified as center of the trace.
    US_state : str
        The state the county is located in. Required due to multiple counties existing with same name.
        Both full name and abbreviated state name are acceptable values.
    statistic : str
        Specification of which column data to calculate the "density" for.
        Allowed values are "cases", "deaths", "confirmed_cases", "confirmed_deaths", "probable_cases", "probable_deaths".
    num_miles : int, float
        Radius in miles of trace using the specified county as the center.
    """
    def __init__ (self, US_county, US_state, statistic, num_miles):
        self.data = None
        self.center = [US_county, US_state]
        self.num_miles = num_miles
        self.updated_last = cases_df['date'].values[0]

        if statistic not in statistic_list:
            raise ValueError('{} not a valid column.'.format(statistic))

        if len(US_state) > 2:
            try:
                US_state = us_state_abbrev[US_state]
            except:
                raise ValueError('{} not a valid state name.'.format(US_state))

        try:
            cases_df.loc[US_county, US_state]
        except:
            raise ValueError('{}, {} not a valid county, state entry.'.format(US_county, US_state))

        """
        Latitudes and longitudes of all counties.
        """
        latitude_1 = counties_df['latitude'].values * np.pi / 180.
        longitude_1 = counties_df['longitude'].values * np.pi / 180.

        """
        Latitude and longitude of specified county.
        """
        latitude_2 = counties_df.loc[US_county, US_state]['latitude'] * np.pi / 180.
        longitude_2 = counties_df.loc[US_county, US_state]['longitude'] * np.pi / 180.

        distances = get_distance(latitude_1, longitude_1, latitude_2, longitude_2)

        self.data = counties_df[distances <= num_miles]
        self.data = self.data.join(cases_df[statistic_list])

        self.data.fillna(0, inplace=True)

        self.data['density'] = self.data[statistic] / self.data['estimated_population']
        self.data.replace([np.inf, -np.inf], np.nan, inplace=True)
        self.data.dropna(inplace=True)

    def retrieve_corners(self):
        """
        Method that retrieves the lower left and upper right latitude and longitude positions (with a predetermined buffer) of covid trace search.

        Parameters
        ----------
        None
        """
        margin_buffer = 20

        lower_left_lat = self.data.loc[self.center]['latitude'] - (self.num_miles + margin_buffer) / 69.
        lower_left_lon = self.data.loc[self.center]['longitude'] - (self.num_miles + margin_buffer) / 69.
        upper_right_lat = self.data.loc[self.center]['latitude'] + (self.num_miles + margin_buffer) / 69.
        upper_right_lon = self.data.loc[self.center]['longitude'] + (self.num_miles + margin_buffer) / 69.

        return [
            (lower_left_lat, lower_left_lon),
            (upper_right_lat, upper_right_lon),
        ]


"""
Solo test.
"""
if __name__ == '__main__':
    
    US_county = 'Alameda'
    US_state = 'CA'
    num_miles = 100
    statistic = 'cases'

    trace = CovidTrace(US_county, US_state, statistic, num_miles)
    # print(trace.data)