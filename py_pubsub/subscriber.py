import rclpy
from rclpy.node import Node
from my_package.msg import CustomMessage

class CustomSubscriber(Node):
    def __init__(self):
        super().__init__('custom_subscriber')
        self.subscription = self.create_subscription(
            CustomMessage,
            'custom_topic',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        self.get_logger().info(f"Received: name={msg.name}, age={msg.age}, height={msg.height}")

def main():
    rclpy.init()
    node = CustomSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
