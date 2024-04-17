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
#Documentació node https://github.com/ros2/rclpy/blob/rolling/rclpy/rclpy/node.py
from rclpy.node import Node

from std_msgs.msg import String

default_parameters = {
    'motor_id' : '010',
    'can_port' : 'can0',
    }


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        
        
        # Inicialitzem parametres ( i aportem default value si no s'h introduït via launch o altre mètodes)
        from rcl_interfaces.msg import ParameterDescriptor
        
        my_parameter_descriptor = ParameterDescriptor(description='Id de la controladora a la qual es dirigeix el node')
        self.declare_parameter('board_id', default_parameters['motor_id'], my_parameter_descriptor)

        can_interface_descriptor = ParameterDescriptor(description="Direcció d'interfaç can (tant pot ser can0 com can1)")
        self.declare_parameter('can_port', default_parameters['can_port'], can_interface_descriptor)
        # ------
        
        #Obtenim la id del node a partir del parametre
        self.board_id=self.get_parameter('board_id').get_parameter_value().string_value
        
        self.subscription = self.create_subscription(
            String,
            '/mov_vel_'+self.board_id,
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        

    def listener_callback(self, msg):
        """Resposta a un nou missatge"""
        self.get_logger().info('I heard: "%s"' % msg.data)
        
        #Afegim la funció que executa comandes en bucle
        timer_period = 0.05  # seconds
            
        #Destruïm tots els timers abans de crear un de nou
        for timer in self.timers:      
            self.destroy_timer(timer)
           
        self.i = 0
        self.moviment = str(msg.data)
        #Guardem la dada en un atribut que perduri en el temps (msg.data es perd)
        #Creem el nou timer
        #Documentació timer https://github.com/ros2/rclpy/blob/rolling/rclpy/rclpy/timer.py
        self.timer = self.create_timer(timer_period, self.timer_callback)
        

    def timer_callback(self):
        """Crida iterada de moviment de robot"""
        
        #Obtenim la interfaç de can a partir del parametre
        can_port = self.get_parameter('can_port').get_parameter_value().string_value
        
        msg = String()
        msg.data = 'Motor ' + self.board_id + ' executa iterativament velocitat de ' + self.moviment 
        self.get_logger().info('Publicant: "%s"' % msg.data)
        self.i += 1
        
        #Enviem el missatge al robot
        #https://unix.stackexchange.com/questions/238180/execute-shell-commands-in-python
        
        os.system('cansend ' + can_port + ' '+ self.board_id + '#25.' + self.moviment + '.10')


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
