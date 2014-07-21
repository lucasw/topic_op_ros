#!/usr/bin/env python

# Lucas Walter
# July 2014
# GPLv3

# Publish the derivative of a topic that has a single numerical value (all the float
# and int types

import sys
import string
import rospy
import time

# TBD have to import all message types with single data fields?
from std_msgs.msg import *
#from std_msgs.msg import Float32

class TopicOp:
    def __init__(self, input_topic, output_topic='/dxdt'): 
        self.sub_pre = None
        self.sub = None
        
        self.cur_value = None
        self.cur_time = None
        self.old_value = None
        self.old_time = None
       
        # just publish Float64 for now
        self.pub = rospy.Publisher(output_topic, Float64)
         
        self.sub_pre = rospy.Subscriber(input_topic, rospy.AnyMsg, self.callbackPre)

    # get knowedge of the topic type before subscribing in a way
    # that will deserialize it
    def callbackPre(self, msg):
        msg_type = msg._connection_header['type']
        msg_type_split =  string.split( msg_type, '/')
        if msg_type_split[0] != 'std_msgs':
            print 'unsupported type', msg_type, 'use a non-array std_msgs'
            return
        
        if msg_type_split[1] == 'Header' or \
                msg_type_split[1] == 'Empty' or \
                msg_type_split[1] == 'String' or \
                len(msg_type_split[1]) > 5 and msg_type_split[1][-5:] == 'Array':
            print 'unsupported type', msg_type
            return

        topic = msg._connection_header['topic']
        atype = msg_type_split[1]
        print 'topic and split', topic, atype 
        # need to unregister first, otherwise get errors
        self.sub_pre.unregister()
        self.sub = rospy.Subscriber(topic, 
                eval(atype),
                self.callback)
    
    # publish a derivative if have samples
    def callback(self, msg):
        #print msg._connection_header['type']
        topic = msg._connection_header['topic']
        #print topic, msg
        
        self.old_value = self.cur_value
        self.old_time = self.cur_time

        self.cur_value = msg.data
        # Really want there to be Float64Stamped etc.
        self.cur_time = time.time()
            
        if self.old_value is not None:
            dx = self.cur_value - self.old_value
            dt = self.cur_time - self.old_time

            if dt == 0:
                return
                
            msg = Float64()
            msg.data = dx / dt
            self.pub.publish(msg)

if __name__ == '__main__':
    rospy.init_node('topic_derivative')
    if len(sys.argv) < 2:
        print 'not enough parameters'
        sys.exit(0)

    input_topic = sys.argv[1]
    if len(sys.argv) == 3:
        output_topic = sys.argv[2]
        topic_op = TopicOp(input_topic, output_topic)
    else:
        topic_op = TopicOp(input_topic)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        None
