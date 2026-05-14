# 🤖 Mobile Manipulator - ROS 2 Final Project

## 1. Mô tả
Dự án mô phỏng một hệ thống robot di động kết hợp tay máy (Mobile Manipulator) trên môi trường ROS 2 Humble. Robot được thiết kế tối ưu cho bài toán di chuyển và lập bản đồ trong các không gian trong nhà (Văn phòng, Hành lang).
- **Hệ truyền động:** Cơ cấu lái Vi sai (Differential Drive) với 2 bánh truyền động và bánh xe phụ (caster) cân bằng.
- **Tay máy:** 2 bậc tự do dạng xoay - xoay (2-DOF R-R).
- **Hệ thống cảm biến:**
  - **LiDAR:** Quét 360 độ phục vụ bài toán SLAM và tránh vật cản.
  - **IMU:** Gắn trực tiếp lên base, cung cấp dữ liệu định hướng và gia tốc.

## 2. Cấu trúc Package
Dự án được chia thành 4 package chính để đảm bảo tính module hóa:

```
├── 📦 robot_bringup            # Khởi chạy tổng của hệ thống
    ├── 📁 launch               
        ├── 🚀 sim.launch.py    # Khởi chạy Gazebo, RViz2 và spawn robot
        └── 🚀 display.launch.py # Xem trước mô hình URDF trên RViz (Không dùng Gazebo)
 
├── 📦 robot_controller         # Package chứa các node điều khiển (Python)
    ├── 📁 robot_controller     
        ├── 📄 arm_controller.py      # Node điều khiển góc xoay tay máy
        ├── 📄 teleop_base_control.py # Điều khiển base mặc định
 
├── 📦 robot_description        # Package chứa mô hình và mô phỏng 3D
    ├── 📁 meshes               # Chứa các file 3D (.stl) của khung và bánh xe
    ├── 📁 rviz                 # Cấu hình giao diện RViz2 (config.rviz)
    └── 📁 urdf                 
        ├── 📄 robot_ros.xacro  # File lắp ráp robot tổng hợp
        ├── 📄 robot_ros.gazebo # Chứa các plugin cảm biến (LiDAR, IMU, Diff Drive)
        └── 📄 materials.xacro  # Định nghĩa vật liệu hiển thị
 
└── 📦 robot_map                # Quản lý hệ thống SLAM và Môi trường
    ├── 📁 config               # Chứa cấu hình thuật toán (cartographer_2d.lua)
    ├── 📁 launch               
        └── 🚀 slam.launch.py   # Gọi node Cartographer và biến đổi TF
    ├── 📁 map                  # Thư mục lưu trữ bản đồ đã quét (hallway, office_loop, room10x10)
    └── 📁 worlds               # Các môi trường Gazebo (hallway.world, office_loop.world...)
```
## 3. Môi trường
- Hệ điều hành: Ubuntu 22.04 LTS
- Phiên bản ROS: ROS 2 Humble
- Trình mô phỏng: Gazebo Classic
- Giao diện trực quan: RViz2

## 4. Cài đặt
Yêu cầu đã cài đặt sẵn ROS 2 Humble.
```
# 1. Tạo workspace và tải mã nguồn

mkdir -p ~/giua_ky_ws/src
cd ~/giua_ky_ws/src
git clone https://github.com/QuanJB/giua_ky_ros.git
cd ..

# 2. Cài đặt công cụ quản lý thư viện rosdep

sudo apt update
sudo apt install python3-rosdep
sudo rosdep init
rosdep update

# 3. Tự động cài đặt toàn bộ dependencies của dự án

rosdep install --from-paths src -y --ignore-src

# 4. Biên dịch hệ thống

colcon build --symlink-install
source install/setup.bash
```
## 5. Cách chạy
Mở các terminal riêng biệt và nạp môi trường (```source install/setup.bash```) trước khi thực hiện:
- Khởi chạy mô phỏng (Gazebo + RViz2 + Controllers):
```
ros2 launch robot_description sim.launch.py
```
- Điều khiển base của robot sử dụng bàn phím:
```
ros2 run robot_controller teleop_base_control.py
```
- Điều khiển tay máy:
```
ros2 run robot_controller arm_controller.py
```
- Chạy CartographerSLAM_2D:
```
ros2 launch robot_map slam.launch.py
```

## 6. Ghi chú kỹ thuật (chưa sửa)
- Dự án áp dụng phương pháp thiết kế Code-First bằng Xacro, cho phép tham số hóa toàn bộ kích thước robot.
- Bộ điều khiển lái Ackermann đã được tinh chỉnh PID ($K_p=100, K_d=20$) để loại bỏ hiện tượng rung bánh xe trong Gazebo.
- Sử dụng lệnh colcon build --symlink-install giúp cập nhật ngay lập tức các thay đổi trong file Xacro hoặc Script Python mà không cần biên dịch lại nhiều lần.
