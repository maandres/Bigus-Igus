# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        
        self.i = 0
        timer_period = 5  # seconds
        
        self.publisher_ = self.create_publisher(String, 'mov_vel_010', 10)
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.publisher1_ = self.create_publisher(String, 'mov_vel_020', 10)
        self.timer1 = self.create_timer(timer_period, self.timer_callback1)

    def timer_callback(self):
        msg = String()
        #msg.data = 'Hello World: %d' % self.i
        msg.data = '00.00'
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

        #Enviem el missatge al robot
        #https://unix.stackexchange.com/questions/238180/execute-shell-commands-in-python
        os.system('cansend can0 111#11.11')
        
    def timer_callback1(self):
        msg = String()
        #msg.data = 'Hello World: %d' % self.i
        msg.data = '00.00'
        self.publisher1_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

        #Enviem el missatge al robot
        #https://unix.stackexchange.com/questions/238180/execute-shell-commands-in-python
        os.system('cansend can0 111#11.11')


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
