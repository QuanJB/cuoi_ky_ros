#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty

msg = """
🕹️ BẢNG ĐIỀU KHIỂN ROBOT (PHONG CÁCH WASD) 🕹️
-----------------------------------------------
       W
    A  S  D

W / S : Tiến / Lùi
A / D : Xoay trái / Phải
Space : Phanh gấp (Dừng lại)

TÙY CHỈNH TỐC ĐỘ:
Q / Z : Tăng / Giảm tốc độ tịnh tiến (+/- 0.05)
E / C : Tăng / Giảm tốc độ xoay (+/- 0.1)

CTRL-C để thoát!
-----------------------------------------------
"""

# Lưu lại cài đặt của terminal để trả về nguyên trạng khi thoát
settings = termios.tcgetattr(sys.stdin)

def get_key():
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('teleop_base_control_node')
    
    # Tạo publisher bắn dữ liệu vào topic /cmd_vel
    pub = node.create_publisher(Twist, 'cmd_vel', 10)

    # TỐC ĐỘ MẶC ĐỊNH (Vừa phải để chạy SLAM)
    speed = 0.2 
    turn = 0.5

    x = 0.0
    th = 0.0

    try:
        print(msg)
        print(f"🚀 Tốc độ hiện tại: Thẳng {speed:.2f} m/s | Xoay {turn:.2f} rad/s")
        
        while True:
            key = get_key()
            
            # Xử lý phím điều hướng
            if key == 'w':
                x = 1.0; th = 0.0
            elif key == 's':
                x = -1.0; th = 0.0
            elif key == 'a':
                x = 0.0; th = 1.0
            elif key == 'd':
                x = 0.0; th = -1.0
            elif key == ' ':
                x = 0.0; th = 0.0
                
            # Xử lý phím tăng giảm tốc độ
            elif key == 'q':
                speed = min(1.0, speed + 0.05)
                print(f"🚀 Tốc độ hiện tại: Thẳng {speed:.2f} m/s | Xoay {turn:.2f} rad/s")
            elif key == 'z':
                speed = max(0.05, speed - 0.05)
                print(f"🚀 Tốc độ hiện tại: Thẳng {speed:.2f} m/s | Xoay {turn:.2f} rad/s")
            elif key == 'e':
                turn = min(2.0, turn + 0.1)
                print(f"🚀 Tốc độ hiện tại: Thẳng {speed:.2f} m/s | Xoay {turn:.2f} rad/s")
            elif key == 'c':
                turn = max(0.1, turn - 0.1)
                print(f"🚀 Tốc độ hiện tại: Thẳng {speed:.2f} m/s | Xoay {turn:.2f} rad/s")
                
            # Thoát vòng lặp nếu nhấn Ctrl+C
            elif key == '\x03': 
                break
            else:
                x = 0.0; th = 0.0

            # Đóng gói và gửi lệnh
            twist = Twist()
            twist.linear.x = x * speed
            twist.angular.z = th * turn
            pub.publish(twist)

    except Exception as e:
        print(e)
        
    finally:
        # Nhả phím / Thoát chương trình thì xe phải dừng lại
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        pub.publish(twist)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()