from covid_trace import CovidTrace
from covid_viz import CovidViz

"""
Main user inputs for creating and plotting COVID data.

Create CovidTrace instance and input US_county, US_state, num_miles, and statistic as inputs.
"""

US_county = 'Alameda'
US_state = 'CA'
num_miles = 60
statistic = 'cases'

trace1 = CovidTrace(US_county, US_state, statistic, num_miles)


US_county = 'Los Angeles'
US_state = 'CA'
num_miles = 100
statistic = 'cases'

trace2 = CovidTrace(US_county, US_state, statistic, num_miles)


US_county = 'Clark'
US_state = 'NV'
num_miles = 100
statistic = 'cases'

trace3 = CovidTrace(US_county, US_state, statistic, num_miles)


US_county = 'Wayne'
US_state = 'MI'
num_miles = 75
statistic = 'cases'

trace4 = CovidTrace(US_county, US_state, statistic, num_miles)


"""
Create CovidViz class, and plot any arbitrary number of CovidTrace instances.
Zoom specifies which CovidTrace to zoom in on for plot, number corresponds with order of CovidTrace inputs.
"""

viz = CovidViz()
viz.plot(
    trace1, 
    trace2, 
    trace3, 
    # trace4, 
    zoom_index=1, resolution='low'
    )