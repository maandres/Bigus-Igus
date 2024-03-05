# Copyright 2011 Brown University Robotics.
# Copyright 2017 Open Source Robotics Foundation, Inc.
# All rights reserved.
#
# Software License Agreement (BSD License 2.0)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of the Willow Garage nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys
import threading
import os
import time

import geometry_msgs.msg
import rclpy

from std_msgs.msg import String   # -- ADDED

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


msg = """
This node takes keypresses from the keyboard and publishes them
as Twist/TwistStamped messages. It works best with a US keyboard layout.
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >

t : up (+z)
b : down (-z)

anything else : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

CTRL-C to quit
"""

# keypress down : ( motor id, hourly direction)
moveBindings = {
    'w': ('010', True),              # -- CHANGED
    'a': ('020', True),
    's': ('010', False),
    'd': ('020', False),
    'i': ('040', True),
    'j': ('050', True),
    'k': ('040', False),
    'l': ('050', False),
    'c': ('030', True),
    'v': ('030', False),
    'p': ('060', True),
    'ñ': ('060', False),
    ' ': ('000', False),      # 000 = All nodes; None = Break
}

speedBindings = {
    '1': ('00.10', 'FF.EF'),
    '2': ('00.30', 'FF.CF'),
    '3': ('00.60', 'FF.9F'),
    '4': ('00.F0', 'FF.0F'),
    '5': ('01.00', 'FE.FF'),
    '6': ('02.00', 'FD.FF'),
    '7': ('04.00', 'FB.FF'),
    '8': ('08.00', 'F9.FF'),
    '9': ('10.00', 'EF.FF'),
}


def getKey(settings):
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)


def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def vels(speed, turn):
    return 'currently:\tspeed %s\tturn %s ' % (speed, turn)


def stop_all_motors():
    for i in range(1,6):
        print('cansend can0 0' + str(i) + '0#01.0A')
        os.system('cansend can0 0' + str(i) + '0#01.0A')

def enable_reset_motor(motor, order):
    time.sleep(0.2)
    #print('cansend can0 ' + motor + order)
    os.system('cansend can0 ' + motor + order)

def main():
    settings = saveTerminalSettings()

    rclpy.init()

    node = rclpy.create_node('teleop_twist_keyboard')

    # parameters
    stamped = node.declare_parameter('stamped', False).value
    frame_id = node.declare_parameter('frame_id', '').value
    if not stamped and frame_id:
        raise Exception("'frame_id' can only be set when 'stamped' is True")

    if stamped:
        TwistMsg = geometry_msgs.msg.TwistStamped
    else:
        TwistMsg = geometry_msgs.msg.Twist

    pub = node.create_publisher(TwistMsg, 'bocata', 10)
    pub1 = node.create_publisher(String, 'mov_vel_010', 10)         # -- ADDED
    pub2 = node.create_publisher(String, 'mov_vel_020', 10)
    pub3 = node.create_publisher(String, 'mov_vel_030', 10)
    pub4 = node.create_publisher(String, 'mov_vel_040', 10)
    pub5 = node.create_publisher(String, 'mov_vel_050', 10)
    pub6 = node.create_publisher(String, 'mov_vel_060', 10)
    
    
    spinner = threading.Thread(target=rclpy.spin, args=(node,))
    spinner.start()

    speed = 0.5
    turn = 1.0
    x = 0.0
    y = 0.0
    z = 0.0
    th = 0.0
    status = 0.0

    twist_msg = TwistMsg()

    if stamped:
        twist = twist_msg.twist
        twist_msg.header.stamp = node.get_clock().now().to_msg()
        twist_msg.header.frame_id = frame_id
    else:
        twist = twist_msg

    try:
        print(msg)
        print(vels(speed, turn))
        velocity = ["00.00","FF.FF"]  # Iniciem les velocitats a 0
        while True:
            key = getKey(settings)
            print("Has presionat la tecla ["+key+"]")  # -- ADDED                      
            
            if key in moveBindings.keys() and moveBindings[key][0] == '000':
                stop_all_motors()
            elif key in moveBindings.keys():             # -- CHANED
                msgg = String()
                msgg.data = velocity[0] if moveBindings[key][1] == True else velocity[1]
                
                if moveBindings[key][0] == '010':
                    pub1.publish(msgg)                    
                elif moveBindings[key][0] == '020':
                    pub2.publish(msgg)
                elif moveBindings[key][0] == '030':
                    pub3.publish(msgg)
                elif moveBindings[key][0] == '040':
                    pub4.publish(msgg)
                elif moveBindings[key][0] == '050':
                    pub5.publish(msgg)
                elif moveBindings[key][0] == '060':     
                    pub6.publish(msgg)
                    
                enable_reset_motor(moveBindings[key][0],'#01.06')
                enable_reset_motor(moveBindings[key][0],'#01.09')
                
            elif key in speedBindings.keys():   # -- CHANGED
                velocity = speedBindings[key]
            
            
            
                #speed = speed * speedBindings[key][0] # -- CHANGED
                #turn = turn * speedBindings[key][1]

                #print(vels(speed, turn))
                #if (status == 14):
                #    print(msg)
                status = (status + 1) % 15
            else:
                #x = 0.0             # -- CHANGED
                #y = 0.0
                #z = 0.0
                #th = 0.0
                if (key == '\x03'):
                    # Disable all motors              #  -- ADDED
                    stop_all_motors()
                    break

            if stamped:
                twist_msg.header.stamp = node.get_clock().now().to_msg()

            #twist.linear.x = x * speed
            #twist.linear.y = y * speed
            #twist.linear.z = z * speed
            #twist.angular.x = 0.0
            #twist.angular.y = 0.0
            #twist.angular.z = th * turn
            #pub.publish(twist_msg)

    except Exception as e:
        print(e)

    finally:
        if stamped:
            twist_msg.header.stamp = node.get_clock().now().to_msg()

        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        pub.publish(twist_msg)
        rclpy.shutdown()
        spinner.join()

        restoreTerminalSettings(settings)


if __name__ == '__main__':
    main()
