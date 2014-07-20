#!/usr/bin/env python

# Lucas Walter
# July 2014
# GPLv3

import ast
import sys
import string
import rospy

from ast import literal_eval

# TBD have to import all message types with single data fields?
from std_msgs.msg import *
#from std_msgs.msg import Float32

class TopicOp:
    def __init__(self, params, expr): # topics):
        self.subs_pre = {}
        self.subs = {}
        self.data = {}
        self.var = {}
        self.params = literal_eval(params)
        self.expr = expr
       
        #print self.params
        for var in self.params:
            #print var 
            topic = self.params[var]

            #print i, topic
            self.var[topic] = var
            #self.subs[topic] = rospy.Subscriber(topic, Float32, self.callback)
            self.subs_pre[topic] = rospy.Subscriber(topic, rospy.AnyMsg, self.callbackPre)
            self.data[topic] = None

    def doOp(self):
        acc = 0
        thismodule = sys.modules[__name__]
        #print thismodule

        # this doesn't work
        #ns = {'__builtins__': None}
        # Not sure if this is any safer
        ns = {'__builtins__': thismodule}

        for key in self.data:
            if self.data[key] is None:
                #continue
                return
            setattr(thismodule, self.var[key], self.data[key])
            
            #print key, self.var[key], '=', eval(self.var[key], ns)
        # eval is super unsafe, use something limited to math expressions
        # http://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
        print eval(self.expr, ns)

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
        print 'topic and split', topic, msg_type_split
        self.subs[topic] = rospy.Subscriber(topic, 
                eval(msg_type_split[1]), self.callback)
        self.subs_pre[topic].unregister()

    def callback(self, msg):
        print msg._connection_header['type']
        topic = msg._connection_header['topic']
        #print topic, msg.data
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
