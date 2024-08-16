# plot_geoweights
Plot weights by ZIP on a map of the Contiguous United States.

## Installation
Install the repository:

```
git clone https://github.com/marinarasauced/plot_geoweights
```
Create a virtual environment and install dependencies:

```
pip install -r /path/to/requirements.txt
```

Add your `.xlsx` dataset to the `data/` subdirectory. It should be formatted as:

| Zip | Units | Quintile |
| --- | --- | --- |
| 00001 | 12345 | Q3 |
| 00003 | 67890 | Q2 |
| 00002 | 00001 | Q3 |

Run `main.py` with the name of the dataset as the argument:

```
python3 /path/to/main.py --file-name placeholder.xlsx
```

The script will generate individual and cummulative plots in the `plots/` subdirectory. If you have a large number of quintiles, considering changing the colormap to increase color diversity.
