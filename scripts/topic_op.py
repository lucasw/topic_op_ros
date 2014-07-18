#!/usr/bin/env python

# Lucas Walter
# July 2014
# GPLv3

import sys
import rospy

from ast import literal_eval

# TBD have to import all message types with single data fields?
from std_msgs.msg import Float32

class TopicOp:
    def __init__(self, params, expr): # topics):
        self.subs = {}
        self.data = {}
        
        print literal_eval(params)

        if False:
        #for i, topic in enumerate(topics):
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
    if len(sys.argv) < 3:
        print 'not enough parameters'
        sys.exit(0)

    params = sys.argv[1]
    expr = sys.argv[2]
    topic_op = TopicOp(params, expr)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        None
