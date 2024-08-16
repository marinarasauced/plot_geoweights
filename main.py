
import argparse
from modules.loader import GeoWeightLoader
from modules.plotter import GeoWeightPlotter

def get_args():
    """
    
    """
    parser = argparse.ArgumentParser(description="generate plot of weights by zip code from an Excel file")
    parser.add_argument("--file-name", type=str, help="the name of the Excel file in the data/ subdir")
    args = parser.parse_args()
    return args


def main():
    """
    
    """
    args = get_args()

    loader = GeoWeightLoader(args.file_name)
    loader.query_data()
    
    plotter = GeoWeightPlotter()
    plotter.generate_overall_plot(loader.query.longitude, loader.query.latitude, loader.data.units, loader.data.quintile)
    plotter.generate_quintile_plots(loader.query.longitude, loader.query.latitude, loader.data.units, loader.data.quintile)
    plotter.generate_cumulative_quintile_plots(loader.query.longitude, loader.query.latitude, loader.data.units, loader.data.quintile)

    print(f"Excluded ZIPs: \n{loader.query.postal_code[plotter.excluded]}")


if __name__=="__main__":
    main()
