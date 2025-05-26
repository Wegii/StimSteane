import stim


class NoiseModel:
    """Applies noise to quantum circuits.

    Adds depolarizing noise after 1 and 2-qubit gates, measurement errors,
    and initialization errors based on typical superconducting qubit parameters.

    Implementation details and Error parameters taken from Table VI in "Realization of Real-Time Fault-Tolerant Quantum Error Correction":
    https://journals.aps.org/prx/pdf/10.1103/PhysRevX.11.041058
    """

    def __init__(self, meas_error = 2.4 * 1e-3, depolarize2 = 3.1 * 1e-3, depolarize1=7 * 1e-5, 
                 depolarize2_scaling = 1, depolarize1_scaling=1, scaling_general=1):
        self.init_error = 1.66 * 1e-6
        self.meas_error = meas_error
        self.depolarize1 = depolarize1
        self.depolarize1_scaling = depolarize2_scaling
        self.depolarize2 = depolarize2
        self.depolarize2_scaling = depolarize2_scaling
        self.scaling_general = scaling_general


    def apply(self, c: stim.Circuit) -> stim.Circuit:
        cn = stim.Circuit()
        for op in c:
            if not op.name in ["CX", "CZ"]:
                cn.append(op)
                if op.name in ["H", "X", "Y", "S", "S_DAG"]:
                    cn.append("DEPOLARIZE1", op.targets_copy(), self.depolarize1*self.depolarize1_scaling*self.scaling_general)
                if op.name in ["M", "MR"]:
                    cn.append("X_ERROR", op.targets_copy(), self.meas_error*self.scaling_general)
                if op.name == "R":
                    cn.append("X_ERROR", op.targets_copy(), self.init_error*self.scaling_general)
            elif op.name in ["CZ"]:
                targets = op.targets_copy()
                for i in range(0, len(targets), 2):
                    control = targets[i]
                    target = targets[i + 1]
                    cn.append("CZ", [control, target])
                    cn.append("DEPOLARIZE2", [control, target], self.depolarize2*self.depolarize2_scaling*self.scaling_general)
            else:
                targets = op.targets_copy()
                for i in range(0, len(targets), 2):
                    control = targets[i]
                    target = targets[i + 1]
                    cn.append("CX", [control, target])
                    cn.append("DEPOLARIZE2", [control, target], self.depolarize2*self.depolarize2_scaling*self.scaling_general)

        return cn