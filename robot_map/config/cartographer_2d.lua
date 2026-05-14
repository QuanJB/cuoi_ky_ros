include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  
  -- Các hệ quy chiếu (TF) cực kỳ quan trọng
  map_frame = "map",
  tracking_frame = "base_footprint", -- Gốc tọa độ của robot
  published_frame = "odom",     -- Cartographer sẽ nối map vào odom
  odom_frame = "odom",
  provide_odom_frame = false,   -- Tắt đi vì Gazebo (diff_drive) đã tự tính odom rồi
  publish_frame_projected_to_2d = true,

  -- Cài đặt cảm biến
  use_pose_extrapolator = true,
  use_odometry = true,          -- Bật cái này lên vì xe vi sai có odom rất xịn
  use_nav_sat = false,
  use_landmarks = false,
  num_laser_scans = 1,          -- Dùng 1 con LiDAR
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 0,
  
  -- Tần số cập nhật (giây)
  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,
  
  -- Tỷ lệ lấy mẫu
  rangefinder_sampling_ratio = 1.,
  odometry_sampling_ratio = 1.,
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 1.,
  landmarks_sampling_ratio = 1.,
}

-- Ép Cartographer chạy chế độ 2D (không bay lên trời)
MAP_BUILDER.use_trajectory_builder_2d = true

-- Cấu hình Trajectory Builder 2D
TRAJECTORY_BUILDER_2D.min_range = 0.12
TRAJECTORY_BUILDER_2D.max_range = 12.0
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 8.5
TRAJECTORY_BUILDER_2D.use_imu_data = false -- Tạm tắt IMU để chạy thuần Lidar + Odom cho dễ lên map
TRAJECTORY_BUILDER_2D.use_online_correlative_scan_matching = true
TRAJECTORY_BUILDER_2D.real_time_correlative_scan_matcher.linear_search_window = 0.1
TRAJECTORY_BUILDER_2D.real_time_correlative_scan_matcher.translation_delta_cost_weight = 10.
TRAJECTORY_BUILDER_2D.real_time_correlative_scan_matcher.rotation_delta_cost_weight = 1e-1

return options