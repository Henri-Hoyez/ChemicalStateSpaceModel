import numpy as np

class SourceDomain:
    def __init__(self) -> None:
        self.beta=0.5
        self.input_amplitude=2.5
        self.input_noise=0.25
        self.output_noise=0.0
        self.fc1=3.5
        self.fc2=4.5
        self.input_mean1=5
        self.input_mean2=5
        
        self.time_shift=0
        self.injective_non_linearity=0
        self.surjective_non_linearity=0

        self.n_data_points = 10000
        self.sampling_rate=0.01


        # SSM global parameters
        self.radius = 1.
        self.control_section= np.pi * self.radius**2
        self.material_velocity = 0.1 # in m.s^-1

