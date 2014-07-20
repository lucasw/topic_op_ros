topic_op_ros
============

Math expressions on ROS topics (and later parameters too?)


Test it out:
  rostopic pub "test1" std_msgs/Float32 "data: 0.5" &
  rostopic pub "test2" std_msgs/Float32 "data: 1.0" &
  rosrun topic_op_ros topiop.py "{'a': '/test1', 'b': '/test2'}" '(a + b)


  #./topic_op.py "{'a': '/test1', 'b': '/test2'}" '(a + b)'

Misc
----

Can this be done already?

https://github.com/ros-visualization/rqt_common_plugins/issues/88 is an open issue

Check out rqt_plot parsing of fields names for type independence subscribing:
https://github.com/ros-visualization/rqt_common_plugins/blob/groovy-devel/rqt_plot/src/rqt_plot/plot.py

Don't need to know the topic type with AnyMsg, but is connection header still there?
http://docs.ros.org/diamondback/api/rospy/html/rospy.msg.AnyMsg-class.html




