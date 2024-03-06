import numpy as np 
import matplotlib.pyplot as plt 
from config.Source_domain import SourceDomain
from models.StateSpaceModel import StateSpaceModel
from utils.utils import generate_inputs, generate_kfs, generate_outputs, generate_rhos, make_labels, make_dataset
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('save_path')
args = parser.parse_args()

source_domain = SourceDomain()

def main():
    t = np.arange(0, source_domain.n_data_points, source_domain.sampling_rate)

    c1_in, c2_in, vc = generate_inputs(
        t, 
        source_domain.input_amplitude, 
        source_domain.input_amplitude,
        source_domain.material_velocity,
        source_domain.fc1, 
        source_domain.fc2,
        source_domain.input_mean1,
        source_domain.input_mean2,
        source_domain.input_noise
    )

    labels, temperatures = make_labels()
    rhos = generate_rhos(source_domain.control_section, vc)
    kfs = generate_kfs(vc, temperatures, beta=source_domain.beta)

    dataset_generator =StateSpaceModel(rhos[0], kfs[0])

    outputs = generate_outputs(
        dataset_generator,
        kfs,
        rhos,
        c1_in, 
        c2_in, 
        source_domain.output_noise
    )

    df_ssm_dataset = make_dataset(c1_in, c2_in, outputs, labels, vc)
    df_ssm_dataset.to_hdf(args.save_path, key='data')

if __name__ == '__main__':
    main()
