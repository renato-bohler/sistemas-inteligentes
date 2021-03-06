from Robot import Robot
from Simulator import Simulator
from vrep import *
import time

sleep_time = 1 / 1000

class RobotControl:

	components = {
		'robot_name': 'bubbleRob',
		'ultrasonic': [
			'Left_ultrasonic',
			'LM_ultrasonic',
			'Middle_ultrasonic',
			'RM_ultrasonic',
			'Right_ultrasonic',
		],
		'vision': [
			'Left_Vision_sensor',
			'LM_Vision_sensor',
			'Middle_Vision_sensor',
			'RM_Vision_sensor',
			'Right_Vision_sensor',
		],
		'motor': [
			'bubbleRob_leftMotor',
			'bubbleRob_rightMotor',
		]
	}

	def __init__(self):
		self.simulator = Simulator('127.0.0.1', 19997)
		self.simulator.connect()
		self.robot = Robot(components=self.components, simulator=self.simulator)


	def isInCrossing(self, robot):
		reading_vision, data_vision = robot.readVisionSensor(robot.components.vision)
		intensities = robot.visionAvarageIntensity(data_vision)

		left_vision = intensities['Left_Vision_sensor']
		middle_vision = intensities['Middle_Vision_sensor']
		right_vision = intensities['Right_Vision_sensor']

		if (left_vision and middle_vision) or (middle_vision and right_vision):
			return True
		elif not ((left_vision and middle_vision) or (middle_vision and right_vision)):
			return False

	def setMotorSpeeds(self, left_motor_speed, right_motor_speed):
		self.robot.setMotorSpeed(self.robot.components.motor['bubbleRob_leftMotor'], left_motor_speed)
		self.robot.setMotorSpeed(self.robot.components.motor['bubbleRob_rightMotor'], right_motor_speed)


	def run(self, direction):

		object_in_front = self.robot.objectInFrontOfProximitySensor(self.robot.components.ultrasonic['Middle_ultrasonic'])

		if direction == 'straight' and object_in_front is False:
			self.goStraight()
		elif direction == 'right':
			self.turnRight()
		elif direction == 'left':
			self.turnLeft()

		self.setMotorSpeeds(0, 0)
		time.sleep(sleep_time)

	def goStraight(self):

		turn_right = 1
		turn_left = 0

		object_in_front = self.robot.objectInFrontOfProximitySensor(
			self.robot.components.ultrasonic['Middle_ultrasonic'])

		while self.isInCrossing(self.robot) is True and object_in_front is False:
			self.setMotorSpeeds(self.robot.VEL_MOT, self.robot.VEL_MOT)

			object_in_front, detected_object_middle_ultrasonic, detected_object_handle_middle_ultrasonic, detected_surface_middle_ultrasonic \
				= self.robot.readProximitySensor(self.robot.components.ultrasonic['Middle_ultrasonic'])
			time.sleep(sleep_time)

		while self.isInCrossing(self.robot) is False and object_in_front is False:

			# anda ate os sensores captarem a linha ou obstaculo
			self.setMotorSpeeds(self.robot.VEL_MOT, self.robot.VEL_MOT)

			reading_vision, data_vision = self.robot.readVisionSensor(self.robot.components.vision)
			intensities = self.robot.visionAvarageIntensity(data_vision)

			left_vision = intensities['Left_Vision_sensor']
			left_middle_vision = intensities['LM_Vision_sensor']
			middle_vision = intensities['Middle_Vision_sensor']
			right_middle_vision = intensities['RM_Vision_sensor']
			right_vision = intensities['Right_Vision_sensor']

			if right_vision is True:
				self.setMotorSpeeds(self.robot.VEL_MOT, self.robot.VEL_MOT / 4)

				turn_right = 1
				turn_left = 0
			elif right_middle_vision is True:
				self.setMotorSpeeds(self.robot.VEL_MOT, self.robot.VEL_MOT / 2)

				turn_right = 1
				turn_left = 0

			elif left_middle_vision is True:  # robo ta desviando para a direita, gira esquerda
				self.setMotorSpeeds(self.robot.VEL_MOT / 2, self.robot.VEL_MOT)

				turn_right = 0
				turn_left = 1
			elif left_vision is True:  # robo ta desviando para a direita, gira esquerda
				self.setMotorSpeeds(self.robot.VEL_MOT / 4, self.robot.VEL_MOT)

				turn_right = 0
				turn_left = 1

			elif (not (
					left_vision or left_middle_vision or middle_vision or right_middle_vision or right_middle_vision)):
				if (turn_right):
					self.setMotorSpeeds(self.robot.VEL_MOT, self.robot.VEL_MOT / 4)

				elif (turn_left):
					self.setMotorSpeeds(self.robot.VEL_MOT / 4, self.robot.VEL_MOT)

			time.sleep(sleep_time)

		position = self.robot.getPosition()
		x_inicial = position[0]
		y_inicial = position[1]
		dx = 0
		dy = 0

		while ((dx < self.robot.DIS_RETO and dy < self.robot.DIS_RETO) and object_in_front is False):  # chegar na linha
			self.setMotorSpeeds(self.robot.VEL_MOT, self.robot.VEL_MOT)
			position = self.robot.getPosition()

			object_in_front, detected_object_middle_ultrasonic, detected_object_handle_middle_ultrasonic, detected_surface_middle_ultrasonic \
				= self.robot.readProximitySensor(self.robot.components.ultrasonic['Middle_ultrasonic'])

			dx = abs(position[0] - x_inicial)
			dy = abs(position[1] - y_inicial)

			time.sleep(sleep_time)

	def turnRight(self):

		d_ang = 0.0
		angle = self.robot.getOrientation()
		initial_angle = angle[2]

		while (d_ang < (3.14159265359 / 4 - self.robot.DIS_CURVA)): # escapar do estado de verificacao dos sensores

			self.setMotorSpeeds(self.robot.VEL_MOT / 1.5, -self.robot.VEL_MOT / 1.5)

			angle = self.robot.getOrientation()

			ang = angle[2]
			d_ang = abs(ang - initial_angle)
			# se houve salto da atan, ignora colocando o salto na posicao normal.Como abs, mas funciona melhor
			if (d_ang > (3.14159265359 / 2 - self.robot.D_ANG)):
				ang = -ang
				d_ang = abs(ang - initial_angle)

			time.sleep(sleep_time)

		reading_vision, data_vision = self.robot.readVisionSensor(self.robot.components.vision)
		intensities = self.robot.visionAvarageIntensity(data_vision)

		middle_vision = intensities['Middle_Vision_sensor']

		while (middle_vision): # verificar se ta no mesmo estado, tecnicamente inutil devido a funcao acima

			self.setMotorSpeeds(self.robot.VEL_MOT / 1.5, -self.robot.VEL_MOT / 1.5)

			reading_vision, data_vision = self.robot.readVisionSensor(self.robot.components.vision)
			intensities = self.robot.visionAvarageIntensity(data_vision)

			middle_vision = intensities['Middle_Vision_sensor']
			time.sleep(sleep_time)

		while not middle_vision: # gira ate os sensores captarem a linha
			self.setMotorSpeeds(self.robot.VEL_MOT / 1.5, -self.robot.VEL_MOT / 1.5)

			reading_vision, data_vision = self.robot.readVisionSensor(self.robot.components.vision)
			intensities = self.robot.visionAvarageIntensity(data_vision)

			middle_vision = intensities['Middle_Vision_sensor']
			time.sleep(sleep_time)

	def turnLeft(self):
		d_ang = 0.0
		angle = self.robot.getOrientation()
		initial_angle = angle[2]

		while d_ang < (3.14159265359 / 4 - self.robot.DIS_CURVA): # escapar do estado de verificacao dos sensores
			self.setMotorSpeeds(-self.robot.VEL_MOT / 1.5, self.robot.VEL_MOT / 1.5)

			angle = self.robot.getOrientation()

			ang = angle[2]
			d_ang = abs(ang - initial_angle)
			# se houve salto da atan, ignora colocando o salto na posicao normal.Como abs, mas funciona melhor
			if (d_ang > (3.14159265359 / 2 - self.robot.D_ANG)):
				ang = -ang
				d_ang = abs(ang - initial_angle)
			time.sleep(sleep_time)

		reading_vision, data_vision = self.robot.readVisionSensor(self.robot.components.vision)
		intensities = self.robot.visionAvarageIntensity(data_vision)

		middle_vision = intensities['Middle_Vision_sensor']

		while middle_vision: # verificar se ta no mesmo estado, tecnicamente inutil devido a funcao acima
			self.setMotorSpeeds(-self.robot.VEL_MOT / 1.5, self.robot.VEL_MOT / 1.5)

			reading_vision, data_vision = self.robot.readVisionSensor(self.robot.components.vision)
			intensities = self.robot.visionAvarageIntensity(data_vision)

			middle_vision = intensities['Middle_Vision_sensor']
			time.sleep(sleep_time)

		while not middle_vision: #gira ate os sensores captarem a linha
			self.setMotorSpeeds(-self.robot.VEL_MOT / 1.5, self.robot.VEL_MOT / 1.5)
			reading_vision, data_vision = self.robot.readVisionSensor(self.robot.components.vision)
			intensities = self.robot.visionAvarageIntensity(data_vision)
			middle_vision = intensities['Middle_Vision_sensor']
			time.sleep(sleep_time)

	def isWalking(self):
		if self.isInCrossing(self.robot):
			return True

		return False