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
        self.x=3.0
        self.y=3.0
        self.start_theta=0
        self.theta=0.0
        self.dt=0.03
        self.cmd_pub=self.create_publisher(Twist, "cmd_vel", 10) 
        self.pose_estm_pub=self.create_publisher(Pose, "pose_estimate", 10) 
        self.create_timer(self.dt, self.move_turtle)

    def update_pose(self, msg:Pose):
        self.turtle_pose=msg   
    
    def move_turtle(self):
        cmd_msg=Twist()
        if self.state=="forward":
            v = 3.0
            self.x += v*cos(self.theta) * self.dt
            self.y += v*sin(self.theta) * self.dt
            distance = sqrt((self.x - self.start_x)**2 + (self.y - self.start_y)**2)

            if distance<self.square_length:
                cmd_msg.linear.x=v
                
            else:
                cmd_msg.linear.x=0.0
                cmd_msg.angular.z=0.0
                self.start_x=self.x
                self.start_y=self.y
                self.start_theta=self.theta
                self.state="turn"
                
        if self.state=="turn":
            omega = 2.0
            self.theta += omega * self.dt
            angle_diff = self.theta - self.start_theta
            angle_diff = (angle_diff + pi) % (2*pi) - pi
            if abs(angle_diff)<pi/2:
                cmd_msg.angular.z=omega
            else:
                self.state="forward"
                self.start_theta=self.theta
                cmd_msg.linear.x=0.0
                cmd_msg.angular.z=0.0
        pose_estimate=Pose()
        pose_estimate.x=self.x
        pose_estimate.y=self.y
        pose_estimate.theta=(self.theta + pi) % (2*pi) - pi
        self.cmd_pub.publish(cmd_msg)
        self.pose_estm_pub.publish(pose_estimate)

    def teleport_turtle(self):
        client = self.create_client(TeleportAbsolute, "turtle1/teleport_absolute")
        request=TeleportAbsolute.Request()
        request.x=3.0
        request.y=3.0
        while not client.wait_for_service(timeout_sec=2.0):
            self.get_logger().info("Waiting for service...")
        future = client.call_async(request)
        future.add_done_callback(self.callback_response)

    def callback_response(self, future):
        response = future.result()
        
    
def main(args=None):
    rclpy.init(args=args)
    node = MoveSquareNode()
    rclpy.spin(node)
    rclpy.shutdown()
    
    
if __name__ == "__main__":
    main()