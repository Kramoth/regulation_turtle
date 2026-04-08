#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtle_interfaces.srv import SetWayPoint 
from std_msgs.msg import Bool   
import math
    
class SetWayPointNode(Node):
    def __init__(self):
        super().__init__("sub_node")
        self.create_subscription(Pose, "turtle1/pose",self.get_turtle_pose_callback,10)
        self.publisher=self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.moving_publisher=self.create_publisher(Bool, "turtle1/is_moving", 10)

        self.add_two_int_service=self.create_service(SetWayPoint, "set_way_point_server",
                                                      self.set_way_point_callback)

        self.create_timer(0.03, self.publish_cmd_callback)
        self.get_logger().info("Subscriber has started")
        self.turtle_pose=Pose()
        # self.waypoint=[7, 7]
        self.waypoint=[0,0]
        self.is_waypoint_set=False
        self.distance_tolerance=0.5

        self.declare_parameter("Kp", 5.0)
        self.declare_parameter("Kpl", 0.8)
        self.Kp = self.get_parameter("Kp").value
        self.Kpl = self.get_parameter("Kpl").value

    def get_turtle_pose_callback(self, msg):
        self.turtle_pose=msg
        # print(self.turtle_pose.x)
    
    def compute_desired_theta(self):
        return math.atan2(self.waypoint[1]-self.turtle_pose.y, self.waypoint[0]-self.turtle_pose.x)
    
    def compute_heading_error(self):
        theta_desire=self.compute_desired_theta()
        return math.atan(math.tan((theta_desire-self.turtle_pose.theta)/2))
    
    def compute_linear_error(self):
        return math.sqrt((self.waypoint[0]-self.turtle_pose.x)**2+(self.waypoint[1]-self.turtle_pose.y)**2)
    
    def publish_cmd_callback(self):

        is_moving_msg=Bool()
        msg=Twist()
        if self.is_waypoint_set:
            error_head  =self.compute_heading_error()
            error_dist=self.compute_linear_error()
            # print(error_dist)
            msg=Twist()
            is_moving_msg=Bool()
            if(error_dist>self.distance_tolerance):
                msg.angular.z=self.Kp*error_head
                msg.linear.x=self.Kpl*error_dist
                is_moving_msg.data=True
        self.publisher.publish(msg)
        self.moving_publisher.publish(is_moving_msg)

    def set_way_point_callback(self,request, response):
        self.is_waypoint_set=True
        self.waypoint[0]=request.x
        self.waypoint[1]=request.y
        response.res=True
        self.get_logger().info(f"request receive: ({request.x}, {request.y}, {self.Kp}, {self.Kpl})")

        return response

def main(args=None):
    rclpy.init(args=args)
    node = SetWayPointNode()
    rclpy.spin(node)
    rclpy.shutdown()
    
    
if __name__ == "__main__":
    main()