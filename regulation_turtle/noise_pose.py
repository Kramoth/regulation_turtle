#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from turtlesim.msg import Pose
import random
    
class NoiseNode(Node):
    def __init__(self):
        super().__init__("sub_node")
        self.create_subscription(Pose, "subscribed_topic",self.sub_callback,10)
        self.publisher=self.create_publisher(Pose, "noisy_pose", 10)
        self.get_logger().info("Subscriber has started")

    def sub_callback(self, msg):
        noisy_pose=Pose()
        noisy_pose.x=msg.x+random.uniform(0, 0.5)
        noisy_pose.y=msg.y+random.uniform(0, 0.5)
        noisy_pose.theta=msg.theta+random.uniform(0, 0.5)
        noisy_pose.angular_velocity=msg.angular_velocity
        noisy_pose.linear_velocity=msg.linear_velocity
        self.publisher.publish(noisy_pose)

    
def main(args=None):
    rclpy.init(args=args)
    node = NoiseNode()
    rclpy.spin(node)
    rclpy.shutdown()
