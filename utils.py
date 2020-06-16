import numpy as np
import pandas as pd

from us_state_abbrev import us_state_abbrev

try:
    from covid_case_scraper import create_covid_csv
    create_covid_csv()
except:
    print('Could not check for COVID case update.')


"""
Takes csv's and converts them into DataFrames.
"""
cases_df = pd.read_csv('us-counties.csv')
cases_df['state'] = [us_state_abbrev[state] for state in cases_df['state'].values]
cases_df = cases_df.set_index(['county', 'state'])

geocodes_df = pd.read_csv('Geocodes_USA_with_Counties.csv')
counties_df = geocodes_df.groupby(['county', 'state']).agg({
    'latitude': 'mean',
    'longitude': 'mean',
    'estimated_population': 'sum',
})


statistic_list = [
    'cases',
    'deaths',
    'confirmed_cases',
    'confirmed_deaths',
    'probable_cases',
    'probable_deaths',
]


earth_radius = 3958     # In miles
# earth_radius = 6371     # In kilometers


"""
Haversine formula for calculating great-circle distance between two points on a sphere using latitude and longitude.
Default units are in radians for latitude/longitude, and miles for distance.
"""
def get_distance(latitude_1, longitude_1, latitude_2, longitude_2):

    latitude_dist = latitude_2 - latitude_1
    longitude_dist = longitude_2 - longitude_1

    h = np.sin(latitude_dist / 2.) ** 2 + np.cos(latitude_1) * np.cos(latitude_2) * np.sin(longitude_dist / 2.) ** 2
    distance = 2 * earth_radius * np.arcsin(np.sqrt(h))

    return distance