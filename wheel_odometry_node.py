
import rclpy
from rcplpy.node import Node
class WheelOdometryNode(Node):
    def __init__(self):
        super().__init__('wheel_odometry_node')
        self.declare_parameter('drive_type','DiffDriveKinematics')
        self.declare_parameter('track_width',0.2)
        self.declare_parameter('wheelbase',0.2)
        self.declare_parameter('wheel_radius',0.2)
        self.x = 0.0
        self.y = 0.0
        self.yaw=0.0
        self.time = self.get_clock().now()
        self.drive_type = self.get_parameter('drive_type').value
        self.track_width = self.get_parameter('track_width').value
        self.wheelbase = self.get_parameter('wheelbase').value
        self.wheel_radius = self.get_parameter('wheel_radius').value