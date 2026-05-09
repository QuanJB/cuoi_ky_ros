#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class ArmControllerNode(Node):
    def __init__(self):
        super().__init__('arm_controller_node')
        # Publisher gửi lệnh đến topic điều khiển tay máy trong Gazebo
        self.publisher_ = self.create_publisher(JointTrajectory, '/set_joint_trajectory', 10)
        
        # Timer lặp lại mỗi 3 giây để chuyển đổi trạng thái (tư thế) của tay máy
        self.timer_ = self.create_timer(3.0, self.timer_callback)
        self.state = 0
        
        self.get_logger().info("Arm Controller Node started. Moving arm...")

    def timer_callback(self):
        msg = JointTrajectory()
        # Khai báo tên 2 khớp của tay máy
        msg.joint_names = ['Revolute 10', 'Revolute 11']
        
        point = JointTrajectoryPoint()
        
        # Tạo chuỗi các tư thế liên tiếp cho tay máy
        if self.state == 0:
            # Tư thế mặc định (thẳng đứng)
            point.positions = [0.0, 0.0]
            self.get_logger().info('State 0: Moving to Home [0.0, 0.0]')
            self.state = 1
        elif self.state == 1:
            # Vươn tay về phía trước
            point.positions = [0.0, 1.57]
            self.get_logger().info('State 1: Reaching Forward [0.0, 1.57]')
            self.state = 2
        elif self.state == 2:
            # Xoay khớp gốc xuống dưới
            point.positions = [-1.57, 1.57]
            self.get_logger().info('State 2: Lowering Arm [-1.57, 1.57]')
            self.state = 3
        elif self.state == 3:
            # Gập gọn tay máy lại
            point.positions = [-1.57, 3.14]
            self.get_logger().info('State 3: Folding Arm [-1.57, 3.14]')
            self.state = 0
            
        # Đặt thời gian để tay máy đi đến vị trí yêu cầu (2 giây)
        point.time_from_start.sec = 2
        point.time_from_start.nanosec = 0
        
        msg.points = [point]
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ArmControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Stopping arm controller...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
