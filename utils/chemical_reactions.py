import numpy as np

def define_kf(v_material, temperature, beta=.85):
    alpha_1 = 0.03
    alpha_2 = 0.25
    max_temperature = 200

    if temperature >= max_temperature:
        raise(Exception(f"[!] ERROR: temperature {temperature} >= max temperature {max_temperature} \n Consider to change either the max temperature or the input temperature."))
    
    return np.exp((1-beta)*alpha_1*(temperature - max_temperature) - beta*alpha_2* v_material)