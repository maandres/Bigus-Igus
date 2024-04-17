# Bigus-Igus
Run an Igus robot (Rebel 6DoF) for automation aplicacion pick and place
Use RoboDK to program and write the script routine

## Scope
Learn the basics of robotics and create a simple and funcitonal aplication

## Demo

### Enable CAN interface
Make executable the script file
```
sudo chmod +x repo/debug/candump.sh
```
Execute the file
```
. repo/debug/candump.sh
```

### Install (Linux)
Create workspace
```
TODO
```
Go to source directory
```
TODO
```
Clone repo
```
TODO
```
Go back to workspace
```
TODO
```
Source the underlying ros environment
```
source /opt/ros/install/setup.bash
```
Install dependendencies
```
rosdep install -i --from-path src --rosdistro iron -y
```
Build packages
```
colcon build --packages-select py_pubsub teleop_twist_keyboard
```

### Launch motor nodes
Open new terminal and source the outerlayer environment
```
source <work_space_created>/install/local_setup.bash
```
Launch de py_pubsub launch file
```
ros2 launch py_pubsub py_pubsub_launch.py can_port:=can0
```

### Run and test the keyboard control
Run
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p can_port:=can0
```
*  --ros-args -r __ns:=/namespace_1

Teleoperate the robot using the keyboards:
 * Direction (WASD CV IJKL PÑ)
 * Velocity (123456789; from slowest to fastest; logarithmic curve)
 
First set a velocity pressing a number and then use the direction to move joint

