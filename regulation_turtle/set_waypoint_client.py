#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtle_interfaces.srv import SetWayPoint
from std_msgs.msg import Bool
from functools import partial
    
    
class SetWaypointClient(Node):
    def __init__(self):
        super().__init__("set_waypoint_client")

        self.client = self.create_client(SetWayPoint, "set_way_point_server")
        self.create_subscription(Bool, "turtle1/is_moving", self.update_is_moving_state, 10)

        self.is_moving = None
        self.request_in_progress = False

        # Liste de waypoints
        self.waypoints = [(3.0, 3.0), (8.0, 3.0), (8.0, 8.0), (3.0, 8.0)]
        self.current_index = 0

        self.create_timer(0.2, self.main_loop)

    def update_is_moving_state(self, msg):
        self.is_moving = msg.data

    def main_loop(self):
        # 1. attendre état connu
        if self.is_moving is None:
            self.get_logger().info("Waiting for is_moving...")
            return

        # 2. attendre service
        if not self.client.wait_for_service(timeout_sec=0.0):
            self.get_logger().info("Waiting for service...")
            return

        # 3. si requête en cours → attendre réponse
        if self.request_in_progress:
            return

        # 4. si la tortue bouge → attendre
        if self.is_moving:
            self.get_logger().info("Turtle moving...")
            return

        # 5. envoyer waypoint suivant
        if self.current_index < len(self.waypoints):
            x, y = self.waypoints[self.current_index]
            self.send_request(x, y)
            self.request_in_progress = True
            self.get_logger().info(f"Sending waypoint {x}, {y}")
        else:
            self.current_index=0

    def send_request(self, x, y):
        request = SetWayPoint.Request()
        request.x = x
        request.y = y

        future = self.client.call_async(request)
        future.add_done_callback(self.callback_response)

    def callback_response(self, future):
        response = future.result()
        self.get_logger().info(f"Response: {response.res}")

        self.request_in_progress = False
        self.current_index += 1


def main(args=None):
    rclpy.init(args=args)
    node = SetWaypointClient()
    rclpy.spin(node)
    rclpy.shutdown()
    
    
if __name__ == "__main__":
    main()