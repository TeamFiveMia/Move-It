
import rclpy
from rclpy.node import Node
<<<<<<< HEAD
from robot_kinematics import DiffDriveKinematics,MecanumKinematics,ThreeWheelOmniKinematics,FourWheelOmniKinematics
=======
from moveIt.robot_kinematics import DiffDriveKinematics,MecanumKinematics,ThreeWheelOmniKinematics,FourWheelOmniKinematics
>>>>>>> 1a774a7 (fixed)
from std_msgs.msg import Float64MultiArray
from nav_msgs.msg import Odometry
from math import sin,cos
from geometry_msgs.msg import TransformStamped
<<<<<<< HEAD
=======
from tf2_ros import TransformBroadcaster
>>>>>>> 1a774a7 (fixed)
class WheelOdometryNode(Node):
    def __init__(self):
        super().__init__('wheel_odometry_node')
        # parameters
        self.declare_parameter('drive_type','DiffDriveKinematics')
        self.declare_parameter('track_width',0.2)
        self.declare_parameter('wheelbase',0.2)
        self.declare_parameter('wheel_radius',0.2)
        # x,y,yaw location of robot
        self.x = 0.0
        self.y = 0.0
        self.yaw=0.0
        # time
        self.time = self.get_clock().now()
        # get the parameters -> variales
        self.drive_type = self.get_parameter('drive_type').value
        self.track_width = self.get_parameter('track_width').value
        self.wheelbase = self.get_parameter('wheelbase').value
        self.wheel_radius = self.get_parameter('wheel_radius').value
        # check whick kinematics is used
        if self.drive_type == 'DiffDriveKinematics':
            self.kinematics = DiffDriveKinematics(self.track_width,self.wheelbase,self.wheel_radius)
        elif self.drive_type == 'MecanumKinematics':
            self.kinematics = MecanumKinematics(self.track_width,self.wheelbase,self.wheel_radius)
        elif self.drive_type == 'ThreeWheelOmniKinematics':
            self.kinematics = ThreeWheelOmniKinematics(self.track_width,self.wheelbase,self.wheel_radius)
        elif self.drive_type == 'FourWheelOmniKinematics':
            self.kinematics = FourWheelOmniKinematics(self.track_width,self.wheelbase,self.wheel_radius)
        else:
            self.get_logger().error('Wrong type')
        #subscriber + publisher
        self.subscribe = self.create_subscription(Float64MultiArray,'/encoder_speeds',self.encoder_callback,10)
        self.pub = self.create_publisher(Odometry,'/odom',10)
        self.broad = TransformBroadcaster(self)
    def encoder_callback(self,msg):
        #current time
        curr = self.get_clock().now()
        # difference
        diff  = (curr - self.time).nanoseconds * 1e-9
        self.time = curr
        if diff <=0:
            return
        #get forward kinematics 
        vx,vy,w=self.kinematics.forward(msg.data)
        # pose integration
        dx = (vx * cos(self.yaw) - vy * sin(self.yaw)) * diff
        dy = (vx * sin(self.yaw) + vy * cos(self.yaw)) * diff
        dyaw = w * diff
        #put in odom vars
        self.x += dx
        self.y += dy
        self.yaw += dyaw
        #publish new values
        omsg = Odometry()
        omsg.header.stamp = self.get_clock().now().to_msg()
        omsg.header.frame_id = 'odom'
        omsg.pose.pose.position.x = self.x
        omsg.pose.pose.position.y = self.y
        omsg.pose.pose.orientation.z = sin(self.yaw/2.0)
        omsg.pose.pose.orientation.w = cos(self.yaw/2.0)
        omsg.child_frame_id = 'base_link'
        omsg.twist.twist.linear.x = vx
        omsg.twist.twist.linear.y = vy
        omsg.twist.twist.angular.z = w
        self.pub.publish(omsg)
        # TF broadcast (ig)
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.rotation.z = sin(self.yaw/2.0)
        t.transform.rotation.w = cos(self.yaw/2.0)
        self.broad.sendTransform(t)

        
<<<<<<< HEAD
    def main(args=None):
        rclpy.init(args = args)
        node = WheelOdemetryNode()
        rclpy.spin(node)
        node.distroy_node()
        rclpy.shutdown()
=======
def main(args=None):
    rclpy.init(args = args)
    node = WheelOdometryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
>>>>>>> 1a774a7 (fixed)

        

        
<<<<<<< HEAD

=======
if __name__ == '__main__':
    main()
>>>>>>> 1a774a7 (fixed)
