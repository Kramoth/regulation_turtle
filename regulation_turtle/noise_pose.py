#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from turtlesim.msg import Pose
import random
    
class NoiseNode(Node):
    def __init__(self):
        super().__init__("add_noise_node")
        self.create_subscription(Pose, "pose",self.sub_callback,10)
        self.publisher=self.create_publisher(Pose, "noisy_pose", 10)
        self.get_logger().info("Subscriber has started")
        self.declare_parameter("noise_min", 0.0)
        self.declare_parameter("noise_max", 0.5)
        self.noise_min = self.get_parameter("noise_min").value
        self.noise_max = self.get_parameter("noise_max").value

    def sub_callback(self, msg):
        noisy_pose=Pose()
        noisy_pose.x=msg.x+random.uniform(self.noise_min, self.noise_max)
        noisy_pose.y=msg.y+random.uniform(self.noise_min, self.noise_max)
        noisy_pose.theta=msg.theta+random.uniform(self.noise_min, self.noise_max)
        noisy_pose.angular_velocity=msg.angular_velocity
        noisy_pose.linear_velocity=msg.linear_velocity
        self.publisher.publish(noisy_pose)
    
def main(args=None):
    rclpy.init(args=args)
    node = NoiseNode()
    rclpy.spin(node)
    rclpy.shutdown()
