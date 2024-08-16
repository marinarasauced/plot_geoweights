import matplotlib.cm as cm
import matplotlib.lines as ml
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from os import path

class GeoWeightPlotter():
    """
    Class for plotting geographical data with weighted points and legends.
    """
    def __init__(self):
        """
        Initializes the GeoWeightPlotter instance.
        """
        self.plot_params = {
            "projection": "merc",
            "llcrnrlat": 23.75,
            "urcrnrlat": 52.5,
            "llcrnrlon": -130,
            "urcrnrlon": -60,
            "resolution": "l"
        }
    

    def create_basemap(self):
        """
        Creates and returns a new Basemap instance.
        """
        return Basemap(
            projection=self.plot_params["projection"],
            llcrnrlat=self.plot_params["llcrnrlat"],
            urcrnrlat=self.plot_params["urcrnrlat"],
            llcrnrlon=self.plot_params["llcrnrlon"],
            urcrnrlon=self.plot_params["urcrnrlon"],
            resolution=self.plot_params["resolution"]
        )


    def load_plot(self):
        """
        Sets up the map boundaries and draws initial map features.
        """
        self.plot = self.create_basemap()
        plt.figure()
        self.plot.drawcoastlines()
        self.plot.drawcountries()
        self.plot.drawmapboundary(fill_color="#D9F7FF")
        self.plot.fillcontinents(color="#CCCBCB", lake_color="#D9F7FF")
        
        self.plot.readshapefile(path.abspath(path.join(path.dirname(__file__), "../config/states")), "states", linewidth=0.5)
        for _, shape in zip(self.plot.states_info, self.plot.states):
            plt.fill(*zip(*shape), color="#F7EAD2", edgecolor="black")


    def prep_plot(self, longitudes, latitudes, units, quintiles):
        """
        Prepares data for plotting by scaling and categorizing.
        """
        longitudes_mask = ~np.isnan(longitudes)
        latitudes_mask = ~np.isnan(latitudes)
        masks = longitudes_mask & latitudes_mask
        indices = np.where(masks)[0]
        indices_ = np.where(units[indices] > 0)[0]

        self.excluded = np.setdiff1d(np.arange(len(longitudes)), indices_)

        longitudes_ = longitudes[indices_]
        latitudes_ = latitudes[indices_]
        units_ = units[indices_]
        quintiles_ = quintiles[indices_]

        scale = 1000
        normal_units = np.asarray(units_ / np.max(units_), dtype=np.float64)
        scaled_units = normal_units + (0.005 * np.log(normal_units + 3))
        scaled_units = scaled_units / np.max(scaled_units)

        scaled_weights = scaled_units * scale
        x1_, x2_ = self.plot(longitudes_, latitudes_)
        
        categories = np.unique(quintiles_)
        category_keys = {category: index for index, category in enumerate(categories)}

        vectorized = np.vectorize(category_keys.get)
        index_keys = vectorized(quintiles_)

        cmap = cm.get_cmap("winter")
        cmap_indices = np.arange(len(categories))
        cmap_indices = cmap_indices / np.max(cmap_indices)
        colors = cmap(cmap_indices)

        return categories, index_keys, x1_, x2_, scaled_weights, colors


    def generate_overall_plot(self, longitudes, latitudes, units, quintiles):
        """
        Generates a plot showing all categories combined.
        """
        self.load_plot()
        categories, index_keys, x1_, x2_, scaled_weights, colors = self.prep_plot(longitudes, latitudes, units, quintiles)

        handles = []
        labels = []
        for idx, category in enumerate(categories, start=0):
            index_keys_ = np.where(index_keys == idx)[0]
            self.plot.scatter(x1_[index_keys_], x2_[index_keys_], np.asarray(scaled_weights, dtype=np.float64)[index_keys_], color=colors[idx, :], alpha=0.5, linewidth=0)

            handle = ml.Line2D([], [], marker="o", color="w", markerfacecolor=colors[idx, :], markersize=10, linestyle="None", label=str(category), alpha=0.7)
            handles.append(handle)
            labels.append(str(category))

        plt.legend(handles=handles, labels=labels, title="Quintiles", loc="best", facecolor="#F7EAD2", edgecolor="black")
        
        self.save_plot("plots/Overall.png")


    def generate_quintile_plots(self, longitudes, latitudes, units, quintiles):
        """
        Generates individual plots for each category.
        """
        categories, index_keys, x1_, x2_, scaled_weights, colors = self.prep_plot(longitudes, latitudes, units, quintiles)

        for idx, category in enumerate(categories, start=0):
            self.load_plot()
            
            index_keys_ = np.where(index_keys == idx)[0]
            self.plot.scatter(x1_[index_keys_], x2_[index_keys_], np.asarray(scaled_weights, dtype=np.float64)[index_keys_], color=colors[idx, :], alpha=0.5, linewidth=0)

            handles = [ml.Line2D([], [], marker="o", color="w", markerfacecolor=colors[idx, :], markersize=10, linestyle="None", label=str(category))]
            labels = [str(category)]
            
            plt.legend(handles=handles, labels=labels, title="Quintiles", loc="best", facecolor="#F7EAD2", edgecolor="black")

            self.save_plot(f"plots/{category}.png")


    def generate_cumulative_quintile_plots(self, longitudes, latitudes, units, quintiles):
        """
        Generates cummulative individual plots for each category.
        """
        categories, index_keys, x1_, x2_, scaled_weights, colors = self.prep_plot(longitudes, latitudes, units, quintiles)

        for idx, category in enumerate(categories, start=0):
            self.load_plot()

            handles = []
            labels = []
            idx_range = np.arange(idx + 1)
            for idx_ in idx_range:
                index_keys_ = np.where(index_keys == idx_)[0]
                self.plot.scatter(x1_[index_keys_], x2_[index_keys_], np.asarray(scaled_weights, dtype=np.float64)[index_keys_], color=colors[idx_, :], alpha=0.5, linewidth=0)

                handle = ml.Line2D([], [], marker="o", color="w", markerfacecolor=colors[idx_, :], markersize=10, linestyle="None", label=str(category), alpha=0.7)
                handles.append(handle)
                labels.append(str(categories[idx_]))
            
            plt.legend(handles=handles, labels=labels, title="Quintiles", loc="best", facecolor="#F7EAD2", edgecolor="black")
            
            self.save_plot(f"plots/{category}_Cummulative.png")


    def save_plot(self, name):
        """
        Saves the plot as a PNG file.
        """
        plt.title("Unit Concentration by ZIP and Quintile")
        plt.savefig(name, dpi=300, bbox_inches="tight")
        plt.close()
