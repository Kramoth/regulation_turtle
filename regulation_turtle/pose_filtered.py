#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
import random
    
class NoiseNode(Node):
    def __init__(self):
        super().__init__("sub_node")
        self.create_subscription(Pose, "turtle1/noisy_pose",self.sub_callback,10)
        self.publisher=self.create_publisher(Pose, "turtle1/pose_filtered", 10)
        self.get_logger().info("Subscriber has started")
        self.declare_parameter("alpha", 0.2)
        self.alpha = self.get_parameter("alpha").value
        self.old_pose=Pose()
        self.init_old_pose=False

    def sub_callback(self, msg):
        if not self.init_old_pose:
            self.old_pose=msg
            self.init_old_pose=True
            return
        
        filtered_pose=Pose()
        filtered_pose.x=self.alpha*msg.x+(1-self.alpha)*self.old_pose.x
        filtered_pose.y=self.alpha*msg.y+(1-self.alpha)*self.old_pose.y
        filtered_pose.theta=self.alpha*msg.x+(1-self.alpha)*self.old_pose.theta
        self.old_pose=filtered_pose
        self.publisher.publish(filtered_pose)
    
def main(args=None):
    rclpy.init(args=args)
    node = NoiseNode()
    rclpy.spin(node)
    rclpy.shutdown()
