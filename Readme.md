# Domain Shift Simulator:

This repository accompanies our paper "Which Time Series Domain Shifts Can Neural Networks Adapt To?" providing a simple chemical simulator for generating multivariate time series data via a State Space Model (SSM). It's designed for researchers to test domain adaptation methods against controlled domain shifts.

To know more about the domain generated shifts, please refer to our paper.

# Getting Started:

## Required libraries:
```bash
pip install numpy==1.21 pandas==1.4.4 pytables==3.6.1 matplotlib==3.5.2
```

# Generate Domain Shifts:

When the libraries have been installed, the following command calls all the scripts to generate the source dataset and all target dataset. 

```bash
./generate_domains.sh
```

# Structure:

The repository has several useful files:
- `config/Source_domain.py`: Contains the parameters of the source SSM that helps to generate the source dataset.
- `models/StateSpaceModel.py`: Contains the State Space Model.
- `utils`:
    - `chemical_reactions.py`: Contains the function that calculates $k_f$. 
    - `utils.py`: Contains all the useful function to generate the dataset.


# Contact
For any queries, please reach out to us at the provided contact details in the paper.