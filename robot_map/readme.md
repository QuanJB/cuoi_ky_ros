Sau khi sao chép các file vào thư mục src, thực hiện build lại workspace:
Bash

cd ~/ros2_ws
colcon build --packages-select my_worlds_pkg
source install/setup.bash

world 1: gz sim -r room_10x10.world
world 2: gz sim -r hallway.world
world 3: gz sim -r office_loop.world

Tọa độ xuất phát
world             x             y             z       yaw           vị trí
1               -4.0          -4.0           0.1      0.0 (east)    tây nam
2                 0            -7            0.1      1.57(North)   đầu hành lang
3                -7            -7            0.1      0.0(east)     điểm a(góc hàng lang)

