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
        self.waypoints = [(3.0, 3.0), (8.0, 3.0), (8.0, 8.0), (3.0, 8.0)]        
        self.spawn_wp()
        self.set_pen()
        self.draw_square()


    def spawn_wp(self):
        client = self.create_client(Spawn, "spawn")
        for i, (x, y) in enumerate(self.waypoints):
            request=Spawn.Request()
            request.x=x
            request.y=y
            request.theta=pi/4+i*pi/2
            request.name=f"turtle_{i}"
            while not client.wait_for_service(timeout_sec=2.0):
                self.get_logger().info("Waiting for service...")
            future = client.call_async(request)
            future.add_done_callback(self.callback_response)

    def set_pen(self):
        client = self.create_client(SetPen, "turtle_0/set_pen")
        request=SetPen.Request()
        request.r=100
        request.b=0
        request.g=0
        request.width=5

        while not client.wait_for_service(timeout_sec=2.0):
                self.get_logger().info("Waiting for service...")
        future = client.call_async(request)
        future.add_done_callback(self.callback_response)

    def draw_square(self):
        client = self.create_client(TeleportAbsolute, "turtle_0/teleport_absolute")
        request=TeleportAbsolute.Request()
        for i, (x, y) in enumerate(self.waypoints):
            request=TeleportAbsolute.Request()
            request.x=x
            request.y=y
            while not client.wait_for_service(timeout_sec=2.0):
                self.get_logger().info("Waiting for service...")
            future = client.call_async(request)
            future.add_done_callback(self.callback_response)
        request.x=self.waypoints[0][0]
        request.y=self.waypoints[0][1]
        while not client.wait_for_service(timeout_sec=2.0):
            self.get_logger().info("Waiting for service...")
        future = client.call_async(request)
        future.add_done_callback(self.callback_response)


    def callback_response(self, future):
        response = future.result()



def main(args=None):
    rclpy.init(args=args)
    node = SetWaypointClient()
    rclpy.shutdown()
    
    
if __name__ == "__main__":
    main()