#!/usr/bin/env python

# Lucas Walter
# July 2014
# GPLv3

import sys
import rospy

# TBD have to import all message types with single data fields?
from std_msgs.msg import Float32

class TopicOp:
    def __init__(self, topics):
        self.subs = {}
        self.data = {}
        for i, topic in enumerate(topics):
            print i, topic
            self.subs[topic] = rospy.Subscriber(topic, Float32, self.callback)
            self.data[topic] = None

    def doOp(self):
        acc = 0
        for key in self.data:
            if self.data[key] is None:
                continue
                # or return
            acc += self.data[key]
        print 'result', acc

    def callback(self, msg):
        topic = msg._connection_header['topic']
        print topic, msg.data
        self.data[topic] = msg.data
        
        self.doOp()

if __name__ == '__main__':
    rospy.init_node('topic_op')
    topic_op = TopicOp(sys.argv[1:])

    try:
        rospy.spin()
    except KeyboardInterrupt:
        None
