#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist    
import math
    
class SetWayPointNode(Node):
    def __init__(self):
        super().__init__("sub_node")
        self.create_subscription(Pose, "turtle1/pose",self.get_turtle_pose_callback,10)
        self.publisher=self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.create_timer(0.03, self.publish_cmd_callback)
        self.get_logger().info("Subscriber has started")
        self.turtle_pose=Pose()
        self.waypoint=[7, 7]

    def get_turtle_pose_callback(self, msg):
        self.turtle_pose=msg
        print(self.turtle_pose.x)
    
    def compute_desired_theta(self):
        return math.atan2(self.waypoint[1]-self.turtle_pose.y, self.waypoint[0]-self.turtle_pose.x)
    
    def compute_heading_error(self):
        theta_desire=self.compute_desired_theta()
        return math.atan(math.tan((theta_desire-self.turtle_pose.theta/2)))
    
    def publish_cmd_callback(self):
        Kp=0.5
        error=self.compute_heading_error()
        msg=Twist()
        msg.angular.z=Kp*error
        self.publisher.publish(msg)
def main(args=None):
    rclpy.init(args=args)
    node = SetWayPointNode()
    rclpy.spin(node)
    rclpy.shutdown()
    
    
if __name__ == "__main__":
    main()