cmake_minimum_required(VERSION 3.0.2)
project(turtlesim_state_machines)


find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  rospy
  std_msgs
)

# add_message_files(
#   FILES
# )

catkin_package(
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

