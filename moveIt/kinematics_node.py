import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray

from .robot_kinematics import ( DiffDriveKinematics,MecanumKinematics,ThreeWheelOmniKinematics,FourWheelOmniKinematics)

class KinematicsNode(Node):
    def __init__(self):
        super().__init__('kinematics_node')
        self.declare_parameter('drive_type', 'DiffDriveKinematics')
        self.declare_parameter('track_width', 0.2)
        self.declare_parameter('wheelbase', 0.2)
        self.declare_parameter('wheel_radius', 0.03)
        # Get parameter values
        drive_type = self.get_parameter('drive_type').value
        track_width = self.get_parameter('track_width').value
        wheelbase = self.get_parameter('wheelbase').value
        wheel_radius = self.get_parameter('wheel_radius').value

        if drive_type == 'DiffDriveKinematics':
            self.kinematics = DiffDriveKinematics(track_width,wheelbase,wheel_radius)
            
        elif drive_type == 'MecanumKinematics':
            self.kinematics = MecanumKinematics(track_width,wheelbase,wheel_radius)
            
        elif drive_type == 'ThreeWheelOmniKinematics':
            self.kinematics = ThreeWheelOmniKinematics(track_width,wheelbase,wheel_radius)
            
        elif drive_type == 'FourWheelOmniKinematics':
            self.kinematics = FourWheelOmniKinematics(track_width,wheelbase,wheel_radius)
        else:
            self.get_logger().error( f'Unknown type')  
        self.cmd_vel_sub = self.create_subscription( Twist, '/cmd_vel',  self.cmd_vel_callback,10)  #create subscriber

        self.wheel_setpoints_pub = self.create_publisher(Float64MultiArray,'/wheel_setpoints',10) #create publisher
    def cmd_vel_callback(self, msg):
        vx = msg.linear.x
        vy = msg.linear.y
        wz = msg.angular.z

        # Calculate wheel angular velocities
        wheel_speeds = self.kinematics.inverse( vx,vy, wz)
        wheel_msg = Float64MultiArray()
        wheel_msg.data = list(wheel_speeds)
        self.wheel_setpoints_pub.publish(wheel_msg)  # Publish wheel setpoints


def main(args=None):

    # Initialize ROS 2
    rclpy.init(args=args)
    node = KinematicsNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

    
        
