from Simulator import Simulator

class Robot:

	def __init__(self, components, simulator):
		self.simulator = simulator
		self.components = simulator.loadRobot(components)
		self.robot = self.components.robot
		self.VEL_MOT = 4.25  # tecnicamente em rad/s
		self.DIS_RETO = 0.05  # tamanho do passo em m ate inicio da leitura dos sensores
		self.DIS_CURVA = 0.262  # delta para virar PI, ja que ha o delay de comunicacao e eh float, nunca igual, (~VEL_MOT/(7.5PI)) - aleatorio
		self.D_ANG = 0.1  # delta para captacao de salto da atan, (~DIS_CURVA-0.1)
		self.MAX_INTENSITY = 0.2  # delta para media ta intensidade. tecnicamente, deve ser zero
		self.CONT = 0  # contador para comecar virar

		self.motor_speed = {}

	def getOrientation(self):
		angle = self.simulator.getObjectAbsoluteOrientation(object=self.robot)
		return angle


	def getPosition(self):
		position = self.simulator.getObjectAbsolutePostion(object=self.robot)
		return position


	def readProximitySensor(self, sensor):
		reading, detected_object, detected_object_handle, detected_surface  \
			= self.simulator.readProximitySensor(object=sensor)

		return reading, detected_object, detected_object_handle, detected_surface


	def readVisionSensor(self, sensors):
		return self.__readAllVisionSensors(sensors)

	def objectInFrontOfProximitySensor(self, sensor):
		reading = self.readProximitySensor(sensor)
		return reading[0]

	def visionAvarageIntensity(self, vision_data):
		readings = {}
		vision_avarage_intensity_index = 10
		for sensor, values in vision_data.items():
			if not values:
				readings[sensor] = 0
			elif len(values[0]) > vision_avarage_intensity_index:
				readings[sensor] = values[0][vision_avarage_intensity_index] < self.MAX_INTENSITY
			else:
				readings[sensor] = 0

		return readings

	def setMotorSpeed(self, motor, speed):
		if not self.motor_speed:
			self.motor_speed = {}

		self.motor_speed[motor] = speed
		self.simulator.setMotorSpeed(motor, speed)

	def __readAllVisionSensors(self, sensors):
		sensor_reading = {}
		sensor_data = {}
		for sensor_name, sensor_handler in sensors.items():
			reading, data = self.__readVisionSensor(sensor_handler)
			sensor_reading[sensor_name] = reading
			sensor_data[sensor_name] = data

		return sensor_reading, sensor_data


	def __readVisionSensor(self, sensor):
		vision_reading, vision_data = self.simulator.readVisionSensor(sensor)
		return vision_reading, vision_data