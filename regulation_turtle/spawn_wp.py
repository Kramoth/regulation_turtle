#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtle_interfaces.srv import SetWayPoint
from turtlesim.srv import Spawn
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import SetPen
from std_msgs.msg import Bool
from functools import partial
from math import pi
    
    
class SetWaypointClient(Node):
    def __init__(self):
        super().__init__("set_waypoint_client")

        self.client = self.create_client(Spawn, "spawn")
        self.waypoints = [(3.0, 3.0), (8.0, 3.0), (8.0, 8.0), (3.0, 8.0),(3.0, 3.0) ]
        counter=0
        for wp in self.waypoints:
            request=Spawn.Request()
            request.x=wp[0]
            request.y=wp[1]
            request.theta=pi/4+counter*pi/2
            counter=counter+1
            request.name=f"turtle_{counter}"
            while not self.client.wait_for_service(timeout_sec=2.0):
                self.get_logger().info("Waiting for service...")
            future = self.client.call_async(request)
            future.add_done_callback(self.callback_response)

        self.move_turtle_client = self.create_client(TeleportAbsolute, "turtle_1/teleport_absolute")
        self.pen_turtle_client = self.create_client(SetPen, "turtle_1/set_pen")
        request=SetPen.Request()
        request.r=100
        request.b=0
        request.g=0
        request.width=5

        while not self.pen_turtle_client.wait_for_service(timeout_sec=2.0):
                self.get_logger().info("Waiting for service...")
        future = self.pen_turtle_client.call_async(request)
        future.add_done_callback(self.pen_callback_response)

        counter=0
        for wp in self.waypoints:
            request=TeleportAbsolute.Request()
            request.x=wp[0]
            request.y=wp[1]
            request.theta=pi/4+counter*pi/2
            counter=counter+1
            while not self.move_turtle_client.wait_for_service(timeout_sec=2.0):
                self.get_logger().info("Waiting for service...")
            future = self.move_turtle_client.call_async(request)
            future.add_done_callback(self.move_callback_response)


        

    def callback_response(self, future):
        response = future.result()
    def move_callback_response(self, future):
        response = future.result()
    def pen_callback_response(self, future):
        response = future.result()


def main(args=None):
    rclpy.init(args=args)
    node = SetWaypointClient()
    rclpy.shutdown()
    
    
if __name__ == "__main__":
    main()