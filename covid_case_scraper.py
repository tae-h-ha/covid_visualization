import numpy as np
import pandas as pd
from urllib.request import urlopen

full_string = urlopen("https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv").read().decode('utf-8')
full_string = full_string.replace('\n', '')
updated_date = full_string.split('probable_deaths')[1].split(',')[0]

def create_covid_csv():
    """
    Method that checks NYTimes COVID data GitHub repository for live data and overwrites case data if outdated.

    Parameters
    ----------
    None
    """
    write_file = False

    """
    Checks latest COVID case csv and compares to existing csv. If no local csv exists, new one is written.
    """
    try:
        cases_df = pd.read_csv('us-counties.csv')
        if cases_df['date'].values[0] == updated_date:
            print('Existing csv is up to date.')
        else:
            write_file = True
    except:
        write_file = True

    if write_file == False:
        pass
    else:
        case_list = full_string.split('probable_deaths')[1].split(updated_date+',')[1:]
        cases_array = [ [ None for y in range(10) ] for x in range(len(case_list)) ]

        for ind,case in enumerate(case_list):
            cases_array[ind][0] = updated_date
            for column in np.arange(9):
                try:
                    entry = case.split(',')[column]
                    if entry == '' or '\n' in entry:
                        entry = 0.
                except:
                    entry = 0.
                cases_array[ind][column+1] = entry

        column_names = [
            'date', 
            'county', 
            'state', 
            'fips', 
            'cases', 
            'deaths', 
            'confirmed_cases', 
            'confirmed_deaths', 
            'probable_cases', 
            'probable_deaths',
            ]

        pd.DataFrame(cases_array, columns=column_names).to_csv('us-counties.csv', index=False)
    
        print('COVID case csv written.')