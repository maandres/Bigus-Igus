from launch import LaunchDescription
from launch_ros.actions import Node


#Proba de portar arguments
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='py_pubsub',
            #namespace='namespace_1',
            executable='listener',
            name='mov_vel_010',
            output="screen",
            emulate_tty=True,
            parameters=[
                {'board_id': '010'},
                {'can_port': LaunchConfiguration("can_port")}
            ]
        ),
        Node(
            package='py_pubsub',
	        #namespace='namespace_1',
            executable='listener',
            name='mov_vel_020',
            output="screen",
            emulate_tty=True,
            parameters=[
                {'board_id': '020'},
                {'can_port': LaunchConfiguration("can_port")}
            ]
        ),
        Node(
            package='py_pubsub',
            #namespace='namespace_1',
            executable='listener',
            name='mov_vel_030',
            output="screen",
            emulate_tty=True,
            parameters=[
                {'board_id': '030'},
                {'can_port': LaunchConfiguration("can_port")}
            ]
        ),
        Node(
            package='py_pubsub',
            #namespace='namespace_1',
            executable='listener',
            name='mov_vel_040',
            output="screen",
            emulate_tty=True,
            parameters=[
                {'board_id': '040'},
                {'can_port': LaunchConfiguration("can_port")}
            ]
        ),
        Node(
            package='py_pubsub',
            #namespace='namespace_1',
            executable='listener',
            name='mov_vel_050',
            output="screen",
            emulate_tty=True,
            parameters=[
                {'board_id': '050'},
                {'can_port': LaunchConfiguration("can_port")}
            ]
        ),
        Node(
            package='py_pubsub',
            #namespace='namespace_1',
            executable='listener',
            name='mov_vel_060',
            output="screen",
            emulate_tty=True,
            parameters=[
                {'board_id': '060'},
                {'can_port': LaunchConfiguration("can_port")}
            ]
        ),
        DeclareLaunchArgument(
        "can_port",
        default_value="can0",
        choices=["can0", "can1"],
        description="Selected can port",
    )
    ])
