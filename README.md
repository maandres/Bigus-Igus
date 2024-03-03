# Bigus-Igus
Run an Igus robot (Rebel 6DoF) for automation aplicacion pick and place
Use RoboDK to program and write the script routine

## Scope
Learn the basics of robotics and create a simple and funcitonal aplication

## Demo

### Install
Build workspace
Go to source directory
Clone repo
Go back to workspace
Install dependendencies
```
rosdep install -i --from-path src --rosdistro iron -y
```
Build packages
```
colcon build --packages-select py_pusbub teleop_twist_keyboard
```

### Launch motor nodes
Launch de py_pubsub launch file
```
ros2 launch py_pubsub py_pubsub_launch.py
```

### Run and test the keyboard control
Run
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r __ns:=/namespace_1
```
Teleoperate the robot using the keyboards:
 * Direction (WASD CV IJKL PÑ)
 * Velocity (123456789; from slowest to fastest; logarithmic curve)
 
First set a velocity pressing a number and then use the direction to move joint

