#!/usr/bin/env python
__author__ = 'jay patravali ,tanvir parhar , srikanth malla'


import rospy
from skeleton_markers.msg import Skeleton
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist

from std_msgs.msg import String

p = Point()
y_left =0.00
x_left=0.00
y_right=0.00
x_right=0.00
y_torso=0.00
x_torso=0.00
pose=Twist()
st=String()
lt=String()
def callback(msg):
   for joint in msg.name:           
            global st
            st=msg.name[0]
           
            p = msg.position[msg.name.index(joint)]
            global x_left
            global y_left
            global x_right
            global y_right
            global x_torso
            global y_torso
            if joint=="left_hand":
              y_left=10*p.y
              x_left=10*p.x
              z_left=10*p.z
             # rospy.loginfo(joint)
            elif joint=="right_hand":
              y_right=10*p.y
              x_right=10*p.x
              z_right=10*p.z
             
            
            elif joint=="torso":
              x_torso=10*p.x
              y_torso=10*p.y
              z_torso=10*p.z
                    
              
            
            x_right=x_right - x_torso
            rospy.loginfo(10*x_right) 

   #rospy.loginfo(m)
    
def apm_kinect():
  #pub2=rospy.Publisher('/send_rc',RC)
  pub=rospy.Publisher('/turtle1/cmd_vel',Twist)
  rospy.init_node('apm_kinect')
  rospy.Subscriber("/skeleton", Skeleton, callback)
  global x_left
  global y_left
  global x_right
  global y_right
  global x_torso
  global y_torso
  lt="left_hand"
  r = rospy.Rate(10) # 10hz
  while not rospy.is_shutdown():
       
       x=Twist()
        
       
       if 10*y_left > 67:
                x.linear.x=4
                x.linear.y=0
                x.linear.z=0
                x.angular.z=0
                pub.publish(x)
       elif 10*y_left < -19.9:
                x.linear.x=-4
                x.linear.y=0
                x.linear.z=0
                x.angular.z=0
                pub.publish(x)
       elif 10*x_right> 74:
                x.linear.x=0
                x.linear.y=0
                x.linear.z=0
                x.angular.z=-3
                pub.publish(x)

       elif 10*x_right< -40:
                x.linear.x=0
                x.linear.y=0
                x.linear.z=0
                x.angular.z=3
                pub.publish(x)
       else:
                x.linear.x=0
                x.linear.y=0
                x.linear.z=0
                x.angular.z=0
                pub.publish(x)
 
       rospy.sleep(0.1)



if __name__ == '__main__':
    try:
        apm_kinect()
    except rospy.ROSInterruptException: 
        pass
