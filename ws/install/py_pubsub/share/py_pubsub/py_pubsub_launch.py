from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='py_pubsub',
            namespace='namespace_1',
            executable='talker',
            name='talker_move',
            output="screen",
            emulate_tty=True,
        ),
        Node(
            package='py_pubsub',
            namespace='namespace_1',
            executable='listener',
            name='mov_vel_010',
            output="screen",
            emulate_tty=True,
            parameters=[
                {'board_id': '010'}
            ]
        ),
        Node(
            package='py_pubsub',
	        namespace='namespace_1',
            executable='listener',
            name='mov_vel_020',
            output="screen",
            emulate_tty=True,
            parameters=[
                {'board_id': '020'}
            ]
        )
    ])
