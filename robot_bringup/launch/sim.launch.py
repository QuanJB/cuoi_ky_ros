import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration

def generate_launch_description():
    # 1. Đường dẫn tới các package
    pkg_description = get_package_share_directory('robot_description')
    pkg_map = get_package_share_directory('robot_map') # Gọi package chứa world của ông
    gazebo_ros_share = get_package_share_directory('gazebo_ros')
    
    # 2. Đường dẫn tới file Xacro và RViz
    xacro_file = os.path.join(pkg_description, 'urdf', 'robot_ros.xacro')
    rviz_config_file = os.path.join(pkg_description, 'rviz', 'config.rviz')

    # 3. Khai báo biến tham số cho World (Mặc định mở room_10x10)
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=os.path.join(pkg_map, 'worlds', 'office_loop.world'),
        description='Path to Gazebo world file'
    )

    # 4. Gọi Gazebo và nạp file world vào
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_share, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': LaunchConfiguration('world')}.items()
    )

    # 5. Dịch Xacro và phát TF (Quan trọng: use_sim_time = True)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': Command(['xacro ', xacro_file]), 'use_sim_time': True}]
    )

    # 6. Thả robot vào Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments = ['-entity', 'robot_ros',
                     '-topic', 'robot_description',
                     '-x', '0',
                     '-y', '0',
                     '-z', '0.08'],
        output='screen'
    )
    
    # 7. Mở luôn RViz2 để tiện debug (Cũng xài giờ mô phỏng)
    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[{'use_sim_time': True}],
        arguments=['-d', rviz_config_file]
    )

    return LaunchDescription([
        world_arg,
        gazebo,
        robot_state_publisher,
        spawn_entity,
        rviz2
    ])