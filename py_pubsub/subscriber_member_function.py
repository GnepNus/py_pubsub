import asyncio
import json
import threading
from typing import Generic

import rclpy
import uvicorn
from action_tutorials_interfaces.action import Fibonacci
from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel
from rclpy.action import ActionClient
from rclpy.node import Node
from rosidl_runtime_py import message_to_ordereddict
from starlette.websockets import WebSocket

from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        # 🔧 解决核心问题：为当前线程设置 event loop
        current_thread = threading.current_thread()
        print(f"当前线程: {current_thread}")
        self.loop = None
        self._get_result_future = None
        self._send_goal_future = None
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')
        self.ws = None

    def send_goal(self, order):
        logger.info(f"send_goal===========")
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        logger.info(f"goal_response_callback===========")
        current_thread = threading.current_thread()
        print(f"当前线程: {current_thread}")
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        logger.info(f"get_result_callback===========")
        current_thread = threading.current_thread()
        print(f"当前线程: {current_thread}")
        result = future.result().result
        self.loop.call_soon_threadsafe(lambda: asyncio.create_task(self.ws.send_text(json.dumps(message_to_ordereddict(result)))))
        self.get_logger().info('Result: {0}'.format(result.sequence))

    def feedback_callback(self, feedback_msg):
        logger.info(f"feedback_callback===========")
        current_thread = threading.current_thread()
        print(f"当前线程: {current_thread}")
        feedback = feedback_msg.feedback
        self.loop.call_soon_threadsafe(lambda: asyncio.create_task(self.ws.send_text(json.dumps(message_to_ordereddict(feedback)))))
        self.get_logger().info('Received feedback: {0}'.format(feedback.partial_sequence))

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

app3 = FastAPI()

MAP_POSE_CLIENT2: MinimalSubscriber = None

@app3.post("/pose", summary="导航地点")
async def to_pose(number: int):
    logger.info(f"pose: {number}")
    MAP_POSE_CLIENT2.send_goal(number)
    return {"status": "ok", "message": "Goal sent successfully"}

@app3.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    MAP_POSE_CLIENT2.ws = websocket
    try:
        while True:
            data = await websocket.receive_text()
            # 可以处理来自客户端的数据
    except Exception as e:
        websocket.close()

def run_loop():
    MAP_POSE_CLIENT2.loop = asyncio.new_event_loop()
    MAP_POSE_CLIENT2.loop.run_forever()

def main(args=None):
    global MAP_POSE_CLIENT2
    rclpy.init(args=args)
    try:
        MAP_POSE_CLIENT2 = MinimalSubscriber()
        threading.Thread(target=run_loop).start()
        threading.Thread(target=rclpy.spin,args=(MAP_POSE_CLIENT2,)).start()
        uvicorn.run(app3, host="0.0.0.0", port=9513)
    finally:
        if MAP_POSE_CLIENT2:
            MAP_POSE_CLIENT2.destroy_node()
        rclpy.shutdown()



if __name__ == '__main__':
    main()