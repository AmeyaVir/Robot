#!/usr/bin/env python
import rospy
from sensor_msgs.msg import JointState

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.name[1])
    
def listener():
    
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("joint_state", JointState, callback)

    rospy.spin()
if __name__ == '__main__':   
    listener()
