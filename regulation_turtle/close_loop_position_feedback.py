#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import TeleportAbsolute
from math import sqrt, pi, atan, tan, sin, cos
    
class MoveSquareNode(Node):
    def __init__(self):
        super().__init__("move_square")
        self.teleport_turtle()
        self.state="forward"
        self.square_length=5
        self.start_x=3
        self.start_y=3
        self.square_heading = 0.0
        self.x=None
        self.y=None
        self.start_theta=None
        self.theta=0
        self.dt=0.03
        self.cmd_pub=self.create_publisher(Twist, "cmd_vel", 10) 
        self.pose_sub=self.create_subscription(Pose,"pose",self.update_pose, 10 )
        self.create_timer(self.dt, self.move_turtle)

    
    def move_turtle(self):
        cmd_msg=Twist()
        if self.x is None:
            return
        
        if self.state=="forward":
            v = 3.0
            distance = sqrt((self.x - self.start_x)**2 + (self.y - self.start_y)**2)
            if distance<self.square_length:
                cmd_msg.linear.x=v
            else:
                cmd_msg.linear.x=0.0
                cmd_msg.angular.z=0.0
                self.start_x=self.x
                self.start_y=self.y
                self.start_theta=self.theta

                self.square_heading +=pi/2
                self.square_heading = (self.square_heading + pi) % (2*pi) - pi
                self.state="turn"
                
        if self.state=="turn":
            omega = 2.0
            angle_diff = self.theta - self.square_heading
            angle_diff = (angle_diff + pi) % (2 * pi) - pi
            if abs(angle_diff)>0.05:
                cmd_msg.angular.z=omega
            else:
                self.state="forward"
                self.start_theta=self.theta
                cmd_msg.linear.x=0.0
                cmd_msg.angular.z=0.0

        self.cmd_pub.publish(cmd_msg)

    def teleport_turtle(self):
        client = self.create_client(TeleportAbsolute, "teleport_absolute")
        request=TeleportAbsolute.Request()
        request.x=3.0
        request.y=3.0
        while not client.wait_for_service(timeout_sec=2.0):
            self.get_logger().info("Waiting for service...")
        future = client.call_async(request)
        future.add_done_callback(self.callback_response)

    def callback_response(self, future):
        response = future.result()

    def update_pose(self, msg):
        self.x=msg.x
        self.y=msg.y
        self.theta=msg.theta
    
def main(args=None):
    rclpy.init(args=args)
    node = MoveSquareNode()
    rclpy.spin(node)
    rclpy.shutdown()
    
    
if __name__ == "__main__":
    main()