import numpy as np

class StateSpaceModel():
    def __init__(self, rho, kf, shift_in_unit_strength=0) -> None:

        self.define_matrices(rho, kf, shift_in_unit_strength)

        self.steady_state = np.dot(self.A, self.Xe) + np.dot(self.B, self.Ue)
        

    def define_matrices(self, rho, kf, shift_in_unit_strength):
        self.X = np.array([[0.],
                           [0.],
                           [0.],
                           [0.]])

        self.A = np.array([[3*rho*kf-3*kf , 0., 0., 0.],
                    [0., rho*kf-kf, 0., 0.],
                    [2*kf-2*rho*kf, 2*kf-2*rho*kf, 0.,0.],
                    [kf-rho*kf, kf-rho*kf, 0.,0.]])

        const = (1- rho)* shift_in_unit_strength + rho

        self.B = np.array([[const, 0., 0., 0.],
                [0., const, 0., 0.],
                [0., 0., const, 0.],
                [0., 0., 0., const]])


        self.C = np.identity(4)

        self.D = np.array([[0., 0., 0., 0.]])

        self.U = np.array([[0.],
                    [0.], 
                    [0.], 
                    [0.]])
        
        self.c_leak = np.array([
           [-rho, 0., 0., 0.],
           [0., -rho, 0., 0.],
           [0., 0., -rho, 0.],
           [0., 0., 0., -rho]
        ])

        self.Ue = np.array([[0.],
                    [0.],
                    [0.],
                    [0.]])

        self.Xe = np.array([[0.],
                    [0.],
                    [0.],
                    [0.]])

    def update_matrices(self, _kf, _rho, _strength=0):
        
        # self.A = np.array([
        #     [3*_rho*_kf-3*_kf , 0., 0., 0.],
        #     [0., _rho*_kf-_kf, 0., 0.],
        #     [2*_kf-2*_rho*_kf, 2*_kf-2*_rho*_kf, 0., 0.],
        #     [_kf-_rho*_kf, _kf-_rho*_kf, 0.,0.]])
        

        self.A = np.array([
            [3*_rho**2*_kf-3*_kf , 0., 0., 0.],
            [0., _rho**2*_kf-_kf, 0., 0.],
            [2*_kf-2*_rho**2*_kf, 2*_kf-2*_rho**2*_kf, 0., 0.],
            [_kf-_rho**2*_kf, _kf-_rho**2*_kf, 0.,0.]])
        
        rho_mat_b = (1- _rho)* _strength + _rho
        self.B = np.array([
           [rho_mat_b, 0., 0., 0.],
           [0., rho_mat_b, 0., 0.],
           [0., 0., rho_mat_b, 0.],
           [0., 0., 0., rho_mat_b]])

        self.c_leak = np.array([
           [-_rho, 0., 0., 0.],
           [0., -_rho, 0., 0.],
           [0., 0., -_rho, 0.],
           [0., 0., 0., -_rho]])
        
        

    def __call__(self, u):
        _u = u - self.Ue
        _x = self.X - self.Xe

        x_dot = np.dot(self.A, _x) + np.dot(self.B, _u) + self.steady_state + np.dot(self.c_leak, _x)

        self.X += x_dot
        y = np.dot(self.C, self.X) + np.dot(self.D, _u)
        return y