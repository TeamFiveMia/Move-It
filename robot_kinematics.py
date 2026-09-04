import numpy as np

class Kinematics:
    def __init__(self, L, W, R):
        # Track width (distance between left and right wheels)
        self.L = L
        # Wheel base length
        self.W = W
        # Wheel radius
        self.R = R
        self.M_forward = None
        self.M_inverse = None
    # Define the interface used functions in the parent class
    def inverse(self, vx, vy, vz):
        ...
    def forward(self, w):
        ...

class MecanumKinematics(Kinematics):
    def __init__(self, L, W, R):
        super().__init__(L, W, R)

        self.M_inverse = (1/self.R) * np.array([
            [1, -1, -(self.L + self.W)],
            [1,  1,  (self.W + self.L)],
            [1,  1, -(self.W + self.L)],
            [1, -1,  (self.W + self.L)]
        ])

        # Forward matrix is obtained using "pseudo inverse" from the inverse matrix
        self.M_forward = np.linalg.pinv(self.M_inverse)

    def inverse(self, vx, vy, vz):
        vel = np.array([vx, vy, vz])

        wheels = np.dot(self.M_inverse, vel)
        return list(wheels)

    def forward(self, w):
        wheels = np.array(w)

        return self.M_forward @ wheels

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

    def forward(self, w):
        wheels = np.array(w)

        return self.M_forward @ wheels

class ThreeWheelOmniKinematics(Kinematics):

    def __init__(self, L, W, R):
        super().__init__(L, W, R)

        # Distance from the center of the chassis to the wheels
        L_node = (2 / 3) * self.W

        # Inverse Kinematics matrix
        self.M_inverse = (1 / R) * np.array([
            [0, -1, L_node]
            [np.sqrt(3) / 2, 0.5 ,L_node]
            [-np.sqrt(3) /2, 0.5, L_node]
        ])
        # Forward matrix obtained using psuedo inverse 
        self.M_forward = np.linalg.pinv(self.M_inverse)

    # Inverse kinematics for three-omni wheels
    def inverse(self, vx, vy, vz):
        vel = np.array([vx, vy, vz])

        return self.M_inverse @ vel

    # Forward kinematics for three-omni wheels
    def forward(self, w):
        wheels = np.array(w)

        return self.M_forward @ wheels

class DiffDriveKinematics(Kinematics):
    def __init__(self, L, W, R):
        super().__init__(L, W, R)

        # Define the kinematic matrices for the sub-class
        # Inverse Kinematics matrix
        self.M_inverse = (1/R) * np.array([
            [1, 0, -self.W/2]
            [1, 0, self.W/2]
            [1, 0, -self.W/2]
            [1, 0, self.W/2]
        ])
        # Forward Kinematics matrix (Inverse Matrix of Inverse)
        self.M_forward = R * np.array([
            [1/4, 1/4, 1/4, 1/4],
            [0, 0, 0, 0],
            [-1/ (2*self.W), 1/ (2*self.W), -1/ (2*self.W), 1/ (2*self.W)]
        ])

    def inverse(self, vx, vy, vz):
        vel = np.array([vx, vy, vz])

        # Return the multiplication of the two matrices
        return self.M_inverse @ vel

    def forward(self, w):
        # Store the wheel speeds in an array/matrix
        wheels = np.array(w)

        # Order of multiplication matters
        return self.M_forward @ wheels