topic_op_ros
============

Math expressions on ROS topics (and later parameters too?)


Test it out:
  rosrun topic_op_ros topic_op.py "{'a': '/a', 'b': '/b'}" '(a + b)' /result1 &
  rostopic pub "a" std_msgs/Float32 "data: 0.5" &
  rostopic pub "b" std_msgs/UInt8 "data: 14" &
  rostopic echo /result1

Misc
----

Can this be done already?

https://github.com/ros-visualization/rqt_common_plugins/issues/88 is an open issue

Check out rqt_plot parsing of fields names for type independence subscribing:
https://github.com/ros-visualization/rqt_common_plugins/blob/groovy-devel/rqt_plot/src/rqt_plot/plot.py

Don't need to know the topic type with type rospy.AnyMsg




