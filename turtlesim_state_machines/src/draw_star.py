#!/usr/bin/env python

import time

import rospy
import smach
import smach_ros

from geometry_msgs.msg import Twist


# constants
_180_DEGREES = 3.14159
_360_DEGREES = 2 * _180_DEGREES

# our constants
LINE_LENGTH = 3.14
MAX_LINES = 6
YAW_VALUE = _180_DEGREES - _360_DEGREES / 10


# define state Draw_Line
class Draw_Line(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','aborted'])

        self.cmd_vel_pub = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size=1)
        self.twist_msg = Twist()
        self.twist_msg.linear.x = LINE_LENGTH

        self.lines_drawn = 0


    def execute(self, userdata):
        rospy.loginfo('Executing state DRAW_LINE')

        if self.lines_drawn < MAX_LINES:
            self.cmd_vel_pub.publish(self.twist_msg)
            time.sleep(2)
            self.lines_drawn += 1
            return 'succeeded'
        else:
            return 'aborted'


# define state Rotate
class Rotate(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded'])

        self.cmd_vel_pub = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size=1)
        self.twist_msg = Twist()
        self.twist_msg.angular.z = YAW_VALUE

    def execute(self, userdata):
        rospy.loginfo('Executing state ROTATE')
        self.cmd_vel_pub.publish(self.twist_msg)
        time.sleep(2)
        return 'succeeded'


# main
def main():
    rospy.init_node('draw_shape_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['succeeded'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('DRAW_LINE', Draw_Line(), 
                               transitions={'succeeded':'ROTATE', 
                                            'aborted':'succeeded'})
        smach.StateMachine.add('ROTATE', Rotate(), 
                               transitions={'succeeded':'DRAW_LINE'})

    # Introspection Server
    #smach_introspection_server = smach_ros.IntrospectionServer('sm_server', sm,
    #        'DRAW_SHAPE_SM_ROOT')
    #smach_introspection_server.start()

    # Execute SMACH plan
    outcome = sm.execute()


if __name__ == '__main__':
    main()

