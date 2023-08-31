#! /usr/bin/env python

import rospy
import os
from math import acos,atan,sqrt,pi,cos,sin
# Message 
from std_msgs.msg import Float64
# Server
from dynamic_reconfigure.server import Server
# TF
import tf2_ros
# CLass
from modelos_cinematicos.Cinematica_Inversa.cinematica_inversa_calculos import calculos_cinematica_inversa
from package_dynamixel.mover_openbot_dynamixel import mover_Dynamixel


class Inverse_Kinematics_3dof(object):
	
	def __init__(self):
		"""Initialisation of the object"""
		# Initilisation of the node 
		rospy.init_node('node_move_class')
		rospy.loginfo('Initialising openbot...')
		# Initalisation of the publisher 
		self.pub_arm1 = rospy.Publisher('/openbot_v1/arm1_arm2_joint_position_controller/command', Float64, queue_size=1)
		self.pub_arm2 = rospy.Publisher('/openbot_v1/arm2_arm3_joint_position_controller/command', Float64, queue_size=1)
		self.pub_arm3 = rospy.Publisher('/openbot_v1/arm3_arm4_joint_position_controller/command', Float64, queue_size=1)
		self.pub_arm4 = rospy.Publisher('/openbot_v1/arm4_clamp1_joint_position_controller/command', Float64, queue_size=1)
		self.pub_clamp = rospy.Publisher('/openbot_v1/clamp1_clamp2_joint_position_controller/command', Float64, queue_size=1)
		self.pub_base = rospy.Publisher('/openbot_v1/base_arm1_joint_position_controller/command', Float64, queue_size=1)
		rospy.on_shutdown(self.shutdownhook)

	def clearConsole(self):
		command = 'clear'
		if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
			command = 'cls'
		os.system(command)
	
	def shutdownhook(self):
		# works better than the rospy.is_shutdown()
		self.ctrl_c = True

	def move_init_pos(self):
		"""Move the robot to the init position during 3 iteration"""
		rate=rospy.Rate(1)

		rospy.loginfo('Moving openbot to the init position...')
		data=0
		angle_joints={"arm1":0,
				"arm2":0,
				"arm3":0,
				"arm4":0,
				"clamp":0,
				"base":0}
		# The robot goes to the init position during 3 sec
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
		cmd_clamp=Float64()
		cmd_base=Float64()

		# Command to move the Robot
		cmd_arm1.data=angle_joints["arm1"]
		cmd_arm2.data=angle_joints["arm2"]
		cmd_arm3.data=angle_joints["arm3"]
		cmd_arm4.data=angle_joints["arm4"]
		cmd_clamp.data=angle_joints["clamp"]
		cmd_base.data=angle_joints["base"]
		rospy.loginfo('Moving openbot...')
		
		# Publication of the command
		self.pub_arm1.publish(cmd_arm1)
		self.pub_arm2.publish(cmd_arm2)
		self.pub_arm3.publish(cmd_arm3)
		self.pub_arm4.publish(cmd_arm4)
		self.pub_clamp.publish(cmd_clamp)
		self.pub_base.publish(cmd_base)

  			
	def move_openbot_toposition(self,q1,q2,q3,x):
		""" Move the robot to the position (x,z,qy) with the angle we compute"""
		# Command to move the Robot
		angle_joints={"arm1":-q1,
					"arm2":-q2,
					"arm3":0,
					"arm4":-q3,
					"clamp":0,
					"base":0}
		rospy.loginfo('Moving openbot to the position (x,z,qy) ...')
		self.move_openbot(angle_joints)
		rospy.sleep(1)
		tfBuffer = tf2_ros.Buffer()    # To know the position of the effector
		listener = tf2_ros.TransformListener(tfBuffer) 
		trans = tfBuffer.lookup_transform('world', 'effector_link_tf', rospy.Time(),rospy.Duration(10))			
		rospy.loginfo("The position in x is : %.2f",-(trans.transform.translation.x)) # Print the position of the effector
		rospy.loginfo("The position in z is : %.2f",trans.transform.translation.z-0.16)
		if x<0:
				rospy.loginfo("The angle of qy is : %.2f",((pi/2-q1-q2-q3)*180/pi))
		else:
				rospy.loginfo("The angle of qy is : %.2f", (pi/2-q1-q2-q3)*180/pi)
	
	def parametros(self):
			try:
				x, z,qy= map (float, input ('Ingrese la coordenada en (X,Z) y el valor de qy: '). split ())
			
			except ValueError:
				print("Error. Digite nuevamente")
				openbot_object.parametros()

			L1=0.094
			L2=0.112
			L3=0.15
			codo=int(input("¿Codo arriba?(1) o ¿codo abajo?(2): "))
			if codo ==1  or codo == 2:
				parametros=[x,z,qy,L1,L2,L3,codo]
			else:
				print("Digite una opciòn valida")
				openbot_object.parametros()
			return parametros

	def calculos(self,parameters):
			x=parameters[0]
			z=parameters[1]
			qy=parameters[2]
			L1=parameters[3]
			L2=parameters[4]
			L3=parameters[5]
			codo=parameters[6]
			try:
				if codo == 1:
					result=calculos_cinematica_inversa.cal_3GDL_arri(x,z,qy,L1,L2,L3)
				if codo == 2:
					result=calculos_cinematica_inversa.cal_3GDL_aba(x,z,qy,L1,L2,L3)
			except ValueError :
				print("Error Matematico, Configuraciòn Inalcanzable")
				result="Error"
			return result


if __name__=="__main__":
	openbot_object=Inverse_Kinematics_3dof()
	dynamixel= mover_Dynamixel()
	try:
		openbot_object.clearConsole()
		parameters=openbot_object.parametros()
		result=openbot_object.calculos(parameters)
		if result == "Error":
			print("El robot no se moverà")
		else:
			openbot_object.move_init_pos()   
			openbot_object.move_openbot_toposition(result[0], result[1],result[2],parameters[0] )
			desicion=int(input('¿Desea  mover el Openbot_v1 real? (1)Si (2)No   '))
			if desicion == 1:
				dynamixel.main()
				x=parameters[0]
				if x > 0 and x >=0.15:
					q1=-result[0]+0.17
					q2=-result[1]+0.05

				elif x < 0 and x<= -0.15:
					q1=-result[0]-0.17
					q2=-result[1]-0.05

				else:
					q1=-result[0]
					q2=-result[1]

				dynamixel.movimiento_inicial('no', -q1 ,-q2 ,'no',result[2],'no')
	except rospy.ROSInterruptException:
		pass

