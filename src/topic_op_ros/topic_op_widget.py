
import os
import rospkg

from python_qt_binding import loadUi
from python_qt_binding.QtCore import Qt, QTimer, qWarning, Slot
from python_qt_binding.QtGui import QAction, QIcon, QMenu, QWidget

import rospy

from rqt_py_common.topic_completer import TopicCompleter
from rqt_py_common.topic_helpers import is_slot_numeric



class TopicOpWidget(QWidget):

    def __init__(self):
        super(TopicOpWidget, self).__init__()
        self.setObjectName('TopicOpWidget')
