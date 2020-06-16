import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

class CovidViz:
    """
    Visualization class for CovidTrace instances.

    Parameters
    ----------
    None
    """
    def __init__(self):

        plt.figure(figsize=(12,8))
        plt.subplot(2,1,1)
        self.us_map = Basemap(
            projection='cyl',
            llcrnrlat=23.2368,
            llcrnrlon=-126.845,
            urcrnrlat=50.1926,
            urcrnrlon=-63.6515,
            resolution='l',
            )
        self.us_map.drawcoastlines()
        self.us_map.drawcountries()
        self.us_map.drawstates(color='gray')


    def plot(self, *args, zoom_index=1, resolution='low', text='estimated_population', ascending=False):
        """
        Method that takes in CovidTrace instances to plot covid data onto US map, as well as zoomed in map with corresponding text.

        Parameters
        ----------
        args* : CovidTrace
            CovidTrace instances to be plotted.
        zoom : int
            Index of which CovidTrace inputted in args* to plot zoomed in, default is first.
        resolution : str
            Resolution of the zoomed in map, default is "low". 
            Allowed values are "crude", "low", "intermediate", "high", and "full".
            Values "intermediate" or higher require additional packages to be installed.
        text : str
            Specification of which column data to show as text alongside zoomed in graph. Default is "estimated_population".
            Allowed values are "latitude", "longitude", "cases", "deaths", "confirmed_cases", "confirmed_deaths", "probable_cases", "probable_deaths".
        ascending : bool
            Order in which to show text based on density value.
            Default is False.
        """
        vmin = 1.
        vmax = 0.

        if zoom_index < 1:
            raise ValueError('Zoom indexing starts at 1.')
        else:
            zoom_index = zoom_index - 1

        resolution_map = {
            'crude': 'c',
            'low': 'l',
            'intermediate': 'i',
            'high': 'h',
            'full': 'f',
        }

        for trace in args:
            if trace.data['density'].max() > vmax:
                vmax = trace.data['density'].max()
            if trace.data['density'].min() < vmin:
                vmin = trace.data['density'].min()

        for ind, trace in enumerate(args):
            """
            Plot on main US map.
            """
            plt.subplot(2,1,1)
            self.us_map.scatter(
                trace.data['longitude'],
                trace.data['latitude'], 
                latlon = True,
                c=trace.data['density'],
                s=trace.data['estimated_population']*(10**-4.5),
                cmap='Reds',
                vmin=vmin,
                vmax=vmax,
                alpha=0.5,
                linewidths=1.5,
            )

            if ind == 0:
                plt.colorbar(label='statistic density')
                plt.title('Covid density map (Last updated: {})'.format(trace.updated_last))

            if ind == zoom_index:
                """
                Plot zoomed-in map with data.
                """
                corners = trace.retrieve_corners()

                plt.subplot(2,2,3)
                map = Basemap(
                    projection='cyl',
                    llcrnrlat=corners[0][0],
                    llcrnrlon=corners[0][1],
                    urcrnrlat=corners[1][0],
                    urcrnrlon=corners[1][1],
                    resolution=resolution_map[resolution],
                    )
                map.drawcoastlines()
                map.drawcountries()
                map.drawstates(color='gray')

                map.scatter(
                    trace.data['longitude'],
                    trace.data['latitude'], 
                    latlon = True,
                    c=trace.data['density'],
                    s=trace.data['estimated_population']*(10**-3),
                    cmap='Reds',
                    vmin=vmin,
                    vmax=vmax,
                    alpha=0.8,
                    linewidths=3.,
                )

                """
                Display text data. If list of counties is too long, it is automatically truncated to fit size.
                """
                table = trace.data.sort_values(by=['density'], ascending=ascending).reset_index()[['county', 'state', text]].to_numpy()
                if table.shape[0] > 15:
                    table = table[:15, :]
                    table = np.concatenate([table, np.array([['...', '...', '...']])])

                ax = plt.subplot(2,2,4)
                ax.axis('off')
                ax.table(
                    cellText=table,
                    colLabels=['County', 'State', 'Population'],
                    loc='center',
                    edges='open',
                )

        plt.show()