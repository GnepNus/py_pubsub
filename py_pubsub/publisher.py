import rclpy
from rclpy.node import Node
from my_package.msg import CustomMessage



class CustomPublisher(Node):
    def __init__(self):
        super().__init__('custom_publisher')
        self.publisher_ = self.create_publisher(CustomMessage, 'custom_topic', 10)
        self.timer = self.create_timer(1.0, self.publish_message)

    def publish_message(self):
        msg = CustomMessage(name="sdf", age=234, height=6.2)
        msg.name = "Bob"
        msg.age = 30
        msg.height = 6.2
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published: {msg}")

def main():
    rclpy.init()
    node = CustomPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
