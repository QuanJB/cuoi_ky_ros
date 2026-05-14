import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # 1. Lấy đường dẫn tới package robot_map
    map_pkg_dir = get_package_share_directory('robot_map')

    # 2. Cài đặt các tham số (biến môi trường)
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    cartographer_config_dir = os.path.join(map_pkg_dir, 'config')
    configuration_basename = 'cartographer_2d.lua'

    # 3. Khởi tạo Node Cartographer (Bộ não vẽ Map)
    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        output='screen',
        parameters=[{'use_sim_time': True}],
        arguments=[
            '-configuration_directory', cartographer_config_dir,
            '-configuration_basename', configuration_basename
        ],
        # Nối topic /scan của ông giáo vào cho nó đọc
        remappings=[
            ('/scan', '/scan')
        ]
    )

    # 4. Khởi tạo Node Occupancy Grid (Biến dữ liệu Cartographer thành bản đồ đen trắng 2D)
    occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        name='cartographer_occupancy_grid_node',
        output='screen',
        parameters=[
            {'use_sim_time': True},
            {'resolution': 0.05} # Độ phân giải bản đồ: 5cm/pixel
        ]
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true', description='Dùng thời gian của Gazebo'),
        cartographer_node,
        occupancy_grid_node,
    ])