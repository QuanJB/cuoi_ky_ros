# Robot ROS 2 Simulation Project

## Giới thiệu
Đây là dự án nâng cấp toàn diện mô hình robot hai bánh vi sai (differential drive) có tích hợp tay máy 2 bậc tự do từ nền tảng ROS 1 sang ROS 2 (Humble). Robot được trang bị cảm biến LiDAR, IMU và có thể mô phỏng hoàn chỉnh cả chuyển động và đặc tính vật lý (trọng lực, ma sát, va chạm) trong môi trường Gazebo cũng như hiển thị dữ liệu (Visualization) trên RViz2.

## Tính năng nổi bật
- **Mô phỏng 3D chuẩn xác:** Các link, joint và mesh STL được cấu hình hoàn chỉnh, đã tối ưu góc tọa độ chuẩn ROS 2.
- **Di chuyển 2 bánh vi sai:** Tích hợp plugin `gazebo_ros_diff_drive`, xuất đủ dữ liệu Odometry (`/odom`) và TF.
- **Cảm biến:** LiDAR (LaserScan quét 360 độ) và IMU hoạt động mượt mà trong Gazebo, cho phép xây dựng bản đồ hoặc ứng dụng tự hành.
- **Tay máy:** Tay máy 2 bậc tự do sử dụng plugin `gazebo_ros_joint_pose_trajectory` với một Node điều khiển tự động bằng ngôn ngữ Python.

## Cài đặt (Installation)
Yêu cầu hệ thống:
- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Classic (phiên bản ROS 2 Humble hỗ trợ)

### 1. Cài đặt các gói ROS 2 phụ thuộc cơ bản:
Mở terminal và chạy lệnh:
```bash
sudo apt update
sudo apt install ros-humble-gazebo-ros-pkgs ros-humble-joint-state-publisher-gui ros-humble-xacro ros-humble-teleop-twist-keyboard
```

### 2. Biên dịch dự án:
```bash
cd ~/robot_ros_ws
colcon build --packages-select robot_ros_description
source install/setup.bash
```

## Hướng dẫn sử dụng (Usage)

### 1. Hiển thị Robot trên RViz2
Dùng để kiểm tra ngoại hình, trạng thái các khớp nối (Joints), cấu trúc cây TF và dữ liệu cảm biến thô.
```bash
ros2 launch robot_ros_description display.launch.py
```
*Ghi chú: Một cửa sổ nhỏ tên "Joint State Publisher" sẽ hiện lên, cho phép bạn kéo các thanh trượt để di chuyển tay máy và bánh xe bằng tay.*

### 2. Khởi động môi trường mô phỏng Gazebo
Dùng để giả lập robot trong một môi trường vật lý như ngoài đời thực.
```bash
ros2 launch robot_ros_description gazebo.launch.py
```

### 3. Điều khiển Robot di chuyển bằng bàn phím
Mở một terminal mới, tải lại môi trường và khởi chạy gói điều khiển bàn phím:
```bash
source ~/robot_ros_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
*Sử dụng các phím `I`, `J`, `K`, `L`, `,` để điều khiển hướng đi của xe.*

### 4. Điều khiển Tay máy tự động
Để khởi động Node Python điều khiển quỹ đạo tay máy tự động chuyển đổi qua lại giữa các tư thế:
```bash
source ~/robot_ros_ws/install/setup.bash
ros2 run robot_ros_description arm_controller.py
```
*Mẹo: Bạn có thể mở mã nguồn tại `scripts/arm_controller.py` để tùy biến góc xoay hoặc bổ sung thêm tính năng cho cánh tay.*

## Cấu trúc thư mục chính của Package
- `launch/`: Các file khởi chạy hệ thống như RViz (`display.launch.py`) và Gazebo (`gazebo.launch.py`).
- `urdf/`: Chứa file `robot_ros.xacro` (định nghĩa cấu trúc robot) và `robot_ros.gazebo` (thiết lập plugin vật lý và thông số cảm biến).
- `meshes/`: Chứa bản vẽ 3D (file .stl) của từng bộ phận robot.
- `scripts/`: Chứa các script Python, bao gồm Node điều khiển tay máy (`arm_controller.py`).
- `rviz/`: Chứa file cấu hình hiển thị đã được tinh chỉnh cho RViz2.
