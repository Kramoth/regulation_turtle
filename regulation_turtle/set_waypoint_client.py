#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtle_interfaces.srv import SetWayPoint
from functools import partial
    
    
class SetWaypointClient(Node):
    def __init__(self):
        super().__init__("set_waypoint_client")
        self.client=self.create_client(SetWayPoint, "set_way_point_server")

    def setwaypoint(self, x, y):
        while not self.client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for the service to be available")
        request=SetWayPoint.Request()
        request.x=x
        request.y=y
        
        future=self.client.call_async(request)

        future.add_done_callback(self.set_way_point_callback)

    def set_way_point_callback(self, future):
        response=future.result()
        self.get_logger().info(f"server responds with: {response.sum}")

def main(args=None):
    rclpy.init(args=args)
    node = SetWaypointClient()
    node.setwaypoint(4.0,4.0)
    rclpy.shutdown()
    
    
if __name__ == "__main__":
    main()