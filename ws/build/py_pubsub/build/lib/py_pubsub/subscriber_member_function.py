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

#Afegim la llibreria de tota la vida. TODO: aprendre com afegir altres llibreries
import os

import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        
        
        # Aquesta declaració és obligatoria per inicia parametre, encara que usem launchfile per assignar valors als parametres
        from rcl_interfaces.msg import ParameterDescriptor
        my_parameter_descriptor = ParameterDescriptor(description='Id de la controladora a la qual es dirigeix el node')
        self.declare_parameter('board_id', '010', my_parameter_descriptor)
        # ------
        
        self.board_id=self.get_parameter('board_id').get_parameter_value().string_value
        
        self.subscription = self.create_subscription(
            String,
            'mov_vel_'+self.board_id,
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        

    def listener_callback(self, msg):
        """Resposta a un nou missatge"""
        self.get_logger().info('I heard: "%s"' % msg.data)
        
        #Afegim la funció que executa comandes en bucle
        timer_period = 0.05  # seconds
            
        #https://github.com/ros2/rclpy/blob/rolling/rclpy/rclpy/node.py
        #Destruïm tots els timers abans de crear un de nou
        for timer in self.timers:      
            self.destroy_timer(timer)
           
        self.i = 0
        
        #Guardem la dada en un atribut que perduri en el temps (msg.data es perd)
        self.moviment = msg.data
        
        #Creem el nou timer
        self.timer = self.create_timer(timer_period, self.timer_callback)
        

    def timer_callback(self):
        """Crida iterada de moviment de robot"""
        msg = String()
        msg.data = 'Motor ' + self.board_id + ' executa iterativament velocitat de ' + self.moviment 
        self.get_logger().info('Publicant: "%s"' % msg.data)
        self.i += 1
        
        #Enviem el missatge al robot
        #https://unix.stackexchange.com/questions/238180/execute-shell-commands-in-python
        
        os.system('cansend can0 '+ self.board_id + '#' + self.moviment)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
