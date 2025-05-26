import stim
from noise.noise_module import NoiseModel


def get_steane_713_noisy_code(meas_error=None, depolarize2=None, depolarize1=None, depolarize2_scaling=1, depolarize1_scaling=1, scaling_general=1):
    """
    [[7, 1, 3]] Steane Code with added Noise by a noise model
    """
    
    noise = NoiseModel(meas_error, depolarize2, depolarize1, depolarize2_scaling, depolarize1_scaling, scaling_general)

    steane_circuit = get_steane_713_code()
    
    noisy_steane_circuit = stim.Circuit()
    noisy_steane_circuit += noise.apply(steane_circuit)
    
    return noisy_steane_circuit


def get_steane_713_x_error_code():
    """
    [[7, 1, 3]] Steane Code with X_Error on Qubit 1 after state preparation
    """
    
    circuit = get_steane_713_code()

    circuit_w_error = circuit[:8]
    # Add X_error after state preparation
    circuit_w_error.append("X_ERROR", 1, 0.5)
    circuit_w_error.append(circuit[8:])

    return circuit_w_error


def get_steane_713_code():
    """
    Create the [[7, 1, 3]] Steane Code from a pre-defined circuit file
    """
    
    return stim.Circuit.from_file("codes/713.stim")


if __name__ == "__main__":
    circuit = get_steane_713_code()