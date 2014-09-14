#!/usr/bin/env python
__author__ = 'tanjaymal'
import rospy
from ardrone_autonomy.srv import LedAnim
import leap_interface
from leap_motion.msg import leap
from leap_motion.msg import leapros
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist


def ardrone_service():
   li = leap_interface.Runner()
   li.setDaemon(True)
   li.start()
   rospy.init_node('ardrone_service')
   #rospy.wait_for_service('/ardrone/setledanimation')
   #led = rospy.ServiceProxy('/ardrone/setledanimation',LedAnim)

   pubLand    = rospy.Publisher('/ardrone/land',Empty)
   pubTakeOff = rospy.Publisher('/ardrone/takeoff',Empty)
   pubCommand = rospy.Publisher('/cmd_vel',Twist)
   rospy.init_node('ardrone_service')
   x = Empty()
   vel=Twist()
   while not rospy.is_shutdown():
        hand_direction_   = li.get_hand_direction()
        hand_normal_      = li.get_hand_normal()
        hand_palm_pos_    = li.get_hand_palmpos()
        hand_pitch_       = li.get_hand_pitch()
        hand_roll_        = li.get_hand_roll()
        hand_yaw_         = li.get_hand_yaw()
        msg = leapros()
        msg.direction.x = hand_direction_[0]
        msg.direction.y = hand_direction_[1]
        msg.direction.z = hand_direction_[2]
        msg.normal.x = hand_normal_[0]
        msg.normal.y = hand_normal_[1]
        msg.normal.z = hand_normal_[2]
        msg.palmpos.x = hand_palm_pos_[0]
        msg.palmpos.y = hand_palm_pos_[1]
        msg.palmpos.z = hand_palm_pos_[2]
        msg.ypr.x = hand_yaw_
        msg.ypr.y = hand_pitch_
        msg.ypr.z = hand_roll_


        if hand_palm_pos_[1]>250:
           pubTakeOff.publish(x)
        else:
           vel.linear.x=0
           vel.linear.y=0
           vel.linear.z=0
           vel.angular.z=0
           pubCommand.publish(vel)

           pubLand.publish(x)

        if hand_pitch_<-25:
           vel.linear.x=0.45
           vel.linear.y=0
           vel.linear.z=0
           pubCommand.publish(vel)
        elif hand_pitch_>25:
           vel.linear.x=-0.45
           vel.linear.y=0
           vel.linear.z=0
           pubCommand.publish(vel)
        elif hand_normal_[0]<-0.65:
           vel.linear.x=0
           vel.linear.y=-0.45
           vel.linear.z=0
           #vel.angular.z=0.5
           pubCommand.publish(vel)
        elif hand_normal_[0]>0.65:
           vel.linear.x=0
           vel.linear.y=0.45
           vel.linear.z=0
           #vel.angular.z=-0.5
           pubCommand.publish(vel)
 
 
        else:
           vel.linear.x=0
           vel.linear.y=0
           vel.linear.z=0
           vel.angular.z=0
           pubCommand.publish(vel)

        rospy.sleep(0.1)
   #try:
     #led(4, 5, 6)
   #except rospy.ServiceException as exc:
     #print("Service did not process request: " + str(exc))

if __name__ == '__main__':
    try:
        ardrone_service()
    except rospy.ROSInterruptException:
        pass


   
