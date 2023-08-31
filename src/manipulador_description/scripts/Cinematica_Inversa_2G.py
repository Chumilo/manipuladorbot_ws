#! /usr/bin/env python
import rospy
import os
# Computing 
from math import acos,atan,sqrt,pi 
# Message 
from std_msgs.msg import Float64
# TF
import tf2_ros
# CLass
from modelos_cinematicos.Cinematica_Inversa.cinematica_inversa_calculos import calculos_cinematica_inversa


class InverseKinematics_2dof(object):
    def __init__(self):
        """Initialisation of the object"""
		# Initilisation of the node 
        rospy.init_node('node_move_class')
        rospy.loginfo('Initialising openbot...')
        # Initalisation of the publisher 
        self.pub_arm1 = rospy.Publisher('/manipulador_description/joint_1_controller/command', Float64, queue_size=1)
        self.pub_arm2 = rospy.Publisher('/manipulador_description/joint_2_controller/command', Float64, queue_size=1)
        self.pub_arm3 = rospy.Publisher('/manipulador_description/joint_3_controller/command', Float64, queue_size=1)
        self.pub_arm4 = rospy.Publisher('/manipulador_description/joint_4_controller/command', Float64, queue_size=1)
        rospy.on_shutdown(self.shutdownhook)


    def shutdownhook(self):
		# works better than the rospy.is_shutdown()
        self.ctrl_c = True
    
    def clearConsole(self):
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)


    def move_init_pos(self):
        """Move the robot to the init position during 3 iteration"""
        rate=rospy.Rate(1)
        rospy.loginfo('Moving openbot to the init position...')
        data=0
        angle_joints={"arm1":0,
				"arm2":0,
				"arm3":0,
				"arm4":0}
		
        while data!=3:
            self.move_openbot(angle_joints)
            data=data+1
            rate.sleep()
        rospy.loginfo('Ending of the init position')


    def move_openbot(self, angle_joints):
        """ Move the robot to the angle we want"""
		# Initialisation of command
        cmd_arm1=Float64()
        cmd_arm2=Float64()
        cmd_arm3=Float64()
        cmd_arm4=Float64()

		# Command to move the Robot
        cmd_arm1.data=angle_joints["arm1"]
        cmd_arm2.data=angle_joints["arm2"]
        cmd_arm3.data=angle_joints["arm3"]
        cmd_arm4.data=angle_joints["arm4"]
        rospy.loginfo('Moving openbot...')
		
		# Publication of the command
        self.pub_arm1.publish(cmd_arm1)
        self.pub_arm2.publish(cmd_arm2)
        self.pub_arm3.publish(cmd_arm3)
        self.pub_arm4.publish(cmd_arm4)


    def move_openbot_toposition(self,q1,q2):
        """ Move the robot to the position (x,z)"""
		# Command to move the Robot
        angle_joints={"arm1":-q1,
					"arm2":-q2,
					"arm3":0,
					"arm4":0}
        rospy.loginfo('Moving openbot to the position (x,z) ...')
        self.move_openbot(angle_joints)
        rospy.sleep(1)
        tfBuffer = tf2_ros.Buffer()    # To know the position of the effector
        listener = tf2_ros.TransformListener(tfBuffer) 
        trans = tfBuffer.lookup_transform('world', 'effector_link_tf', rospy.Time(),rospy.Duration(10))			
        rospy.loginfo("The position in x is : %.2f",-(trans.transform.translation.x)) # Print the position of the effector
        rospy.loginfo("The position in z is : %.2f",trans.transform.translation.z-0.16)
    
    def parametros(self):
        try:
            x, z= map (float, input ('Ingrese la coordenada en X y en Z: '). split ())
          
        except ValueError:
            print("Error. Digite nuevamente")
            openbot_object.parametros()

        L1=0.094
        L2=0.262
        codo=int(input("¿Codo arriba?(1) o ¿codo abajo?(2):   "))
        if codo ==1  or codo == 2:
            parametros=[x,z,L1,L2,codo]
        else:
            print("Digite una opciòn valida")
            openbot_object.parametros()
        return parametros

    def calculos(self,parameters):
        x=parameters[0]
        z=parameters[1]
        L1=parameters[2]
        L2=parameters[3]
        codo=parameters[4]
        try:
            if codo == 1:
                result=calculos_cinematica_inversa.cal_2GDL_arri(x,z,L1,L2)
            if codo == 2:
                result=calculos_cinematica_inversa.cal_2GDL_aba(x,z,L1,L2)
        
        except ValueError :
            print("Error Matematico, Configuraciòn Inalcanzable")
            result="Error"
        return result


if __name__=="__main__":
    openbot_object=InverseKinematics_2dof()
    dynamixel=mover_Dynamixel()
    try:
            openbot_object.clearConsole()
            parameters=openbot_object.parametros()
            result=openbot_object.calculos(parameters) #Calculos de Cinematica Inversa
            if result == "Error":
                print("El robot no se moverà")
            else:
                """ penbot_object.move_init_pos()   #Movimiento a posicion inicial  """
                openbot_object.move_openbot_toposition(result[0], result[1] ) #El robot se mueve segun q1 y q2
                desicion=int(input('¿Desea  mover el Openbot_v1 real? (1)Si (2)No   '))
                if desicion == 1:
                    x=parameters[0]
                    if x > 0 and x >=0.15:
                        q1=-result[0]+0.17 # Correcciòn del movimiento del robot
                        q2=-result[1]+0.05
                    elif x < 0 and x<= -0.15:
                        q1=-result[0]-0.17
                        q2=-result[1]-0.05
                    else:
                        q1=-result[0]
                        q2=-result[1]
    except rospy.ROSInterruptException:
	    pass

