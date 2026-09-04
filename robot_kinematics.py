import numpy as np

class Kinematics:
    def __init__(self, L, W, R):
        self.L = L
        self.W = W
        self.R = R
        self.M_forward = 0
        self.M_inverse = 0


class MecanumKinematics(Kinematics):
    def __init__(self, L, W, R):
        super().__init__(L, W, R)

        self.M_inverse = (1/self.R) * np.array([
            [1, -1, -(self.L + self.W)],
            [1,  1,  (self.W + self.L)],
            [1,  1, -(self.W + self.L)],
            [1, -1,  (self.W + self.L)]
        ])

        self.M_forward = np.linalg.pinv(self.M_inverse)

    def inverse(self, vx, vy, vz):
        vel = np.array([vx, vy, vz])

        wheels = np.dot(self.M_inverse, vel)
        return list(wheels)


class FourWheelOmniKinematics(Kinematics):
    def __init__(self, L, W, R):
        super().__init__(L, W, R)

        angle = np.pi/4
        self.M_inverse = (1/R) *  np.array([
        [-np.sin(angle), np.cos(angle), self.L],
        [-np.sin(3*angle), np.cos(3*angle), self.L],
        [-np.sin(5*angle), np.cos(5*angle), self.L],
        [-np.sin(7*angle), np.cos(7*angle), self.L]
        ])

        self.M_forward = np.linalg.pinv(self.M_inverse)

    def inverse(self, vx, vy, vz):
        vel = np.array([vx, vy, vz])

        wheels = np.dot(self.M_inverse, vel)
        return list(wheels)


class ThreeWheelOmniKinematics(Kinematics):
    ... #TODO


class DiffDriveKinematics(Kinematics):
    ... #TODO