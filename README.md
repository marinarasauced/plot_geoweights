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

Add your `.xlsx` dataset to the `data/` subdirectory. It should be formatted 

| Zip   | Units | Quintile |
| 00001 | 12345 | Q3       |
| 00002 | 67890 | Q2       |
