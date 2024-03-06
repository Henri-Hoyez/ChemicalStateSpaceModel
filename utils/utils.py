import numpy as np
import pandas as pd
from config.Source_domain import SourceDomain
from utils.chemical_reactions import define_kf
from models.StateSpaceModel import StateSpaceModel
import os

SOURCE_DOMAIN=SourceDomain()

def make_labels(source_domain=SOURCE_DOMAIN, amplitude=50, sig_mean=50, f=0.1, sr=0.01):
    t = np.arange(0, source_domain.n_data_points, sr)
    labels = np.zeros_like(t)

    temperatures = amplitude* np.sin(2* np.pi* f* t) + sig_mean

    labels[(temperatures > 20.) & (temperatures <= 40.)] = 1.
    labels[(temperatures > 40.) & (temperatures <= 60.)] = 2.
    labels[(temperatures > 60.) & (temperatures <= 80.)] = 3.
    labels[(temperatures > 80.) & (temperatures <= 100)] = 4.

    return labels, temperatures


def generate_inputs(
    t, c1, c2,
    material_velocity,
    fc1=SOURCE_DOMAIN.fc1,
    fc2=SOURCE_DOMAIN.fc2,
    mean_1=SOURCE_DOMAIN.input_mean1,
    mean_2=SOURCE_DOMAIN.input_mean2,
    input_noise=SOURCE_DOMAIN.input_noise):


    n1 = np.random.normal(size=t.shape[0], scale=input_noise)
    n2 = np.random.normal(size=t.shape[0], scale=input_noise)

    c1_in = mean_1+ c1*np.sin(2*np.pi*fc1*t)+ n1
    c2_in = mean_2+ c2*np.sin(2*np.pi*fc2*t)+ n2

    c1_in[c1_in < 0] = 0.
    c2_in[c2_in < 0] = 0.

    # Define the velocity thanks to time
    fvc = 0.5
    vc = material_velocity + 0.3*material_velocity* np.sin(2*np.pi*fvc*t)

    return c1_in, c2_in, vc


def generate_kfs(vc, temperatures, beta=SOURCE_DOMAIN.beta):
    kfs = []
    for _vs, _temp in zip(vc, temperatures):
        kfs.append(define_kf(_vs, _temp, beta=beta))

    return np.array(kfs)


def generate_rhos(control_section, vc):
    return control_section*vc


def generate_outputs(
        dataset_generator:StateSpaceModel,
        kfs, 
        rhos,
        c1_in,
        c2_in,
        noise_scale=SOURCE_DOMAIN.output_noise):
    
    outputs = []
    dataset_generator.update_matrices(kfs[0], rhos[0])

    for _kf, _rho, in_c1, in_c2 in zip(kfs, rhos, c1_in, c2_in):
        _u = np.array([[in_c1],
                    [in_c2], 
                    [0.], 
                    [0.]])
        dataset_generator.update_matrices(_kf, _rho)
        _outs = dataset_generator(_u)
        outputs.append(_outs.reshape((-1,)))

    outputs = np.array(outputs)

    # Make Output noise
    for c in range(outputs.shape[1]):
        noise = np.random.normal(size=outputs.shape[0], scale=noise_scale)
        outputs[:, c]= outputs[:, c]+ noise 

    return outputs


def make_dataset(c1_in, c2_in, ssm_outputs, labels, vc):
    cols = ["in_c1", "in_c2", "out_c1", "out_c2", "out_c3", "out_c4", "material velocity", "labels"]

    inputs = np.array([c1_in, c2_in]).T
    data = np.hstack((inputs, ssm_outputs, vc.reshape((-1, 1)), labels.reshape((-1, 1))))

    df = pd.DataFrame(data, columns=cols)
    return df

def make_folder(path:str):
    folders_path = path.split("/")[:-1]
    folders_path = "/".join(folders_path)

    if not os.path.exists(folders_path):
        print(f"[+] Create a folder at {folders_path}")
        os.makedirs(folders_path)
