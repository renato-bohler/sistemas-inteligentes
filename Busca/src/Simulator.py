import vrep
from collections import namedtuple

class Simulator:

	def __init__(self, ip = '127.0.0.1', port=19997):
		self.ip = ip
		self.port = port
		self.command_on_server = {}

	def connect(self):
		vrep.simxFinish(-1)
		self.clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
		if self.clientID == -1:
			raise RuntimeError('Error connecting to server')
		return self.clientID


	def loadRobot(self, robot_components):
		robot_handler = robot_components.pop('robot_name')
		robot = {}
		robot['robot'] = self.__load_component(robot_handler)

		for component_type in robot_components:
			components = {}

			for component_name in robot_components[component_type]:
				components[component_name] = self.__load_component(component_name)

			robot[component_type] = components

		robot_object = namedtuple("Robot", robot.keys())(*robot.values())

		return robot_object


	def getObjectAbsoluteOrientation(self, object):
		operation = self.__controlCommandsOnServer('orientation', object)
		if operation is vrep.simx_opmode_streaming:
			_, angle = vrep.simxGetObjectOrientation(self.clientID, object, -1, operation)

		_, angle = vrep.simxGetObjectOrientation(self.clientID, object, -1, vrep.simx_opmode_streaming)

		return angle

	def getObjectAbsolutePostion(self, object):
		operation = self.__controlCommandsOnServer('position', object)
		if operation is vrep.simx_opmode_streaming:
			vrep.simxGetObjectPosition(self.clientID, object, -1, operation)

		_, position = vrep.simxGetObjectPosition(self.clientID, object, -1, vrep.simx_opmode_streaming)

		return position

	def readProximitySensor(self, object):
		operation = self.__controlCommandsOnServer('proximity_sensor', object)
		if operation is vrep.simx_opmode_streaming:
			vrep.simxReadProximitySensor(self.clientID, object, operation)

		_, sensor_reading, detected_object, detected_object_handle, detected_surface = vrep.simxReadProximitySensor(
			self.clientID, object, vrep.simx_opmode_streaming)

		return sensor_reading, detected_object, detected_object_handle, detected_surface


	def readVisionSensor(self, object):
		operation = self.__controlCommandsOnServer('vision_sensor', object)
		if operation is vrep.simx_opmode_streaming:
			vrep.simxReadVisionSensor(self.clientID, object, operation)

		_, sensor_reading, sensor_data = vrep.simxReadVisionSensor(self.clientID, object, vrep.simx_opmode_streaming)

		return sensor_reading, sensor_data


	def setMotorSpeed(self, object, speed):
		vrep.simxSetJointTargetVelocity(self.clientID, object, speed,vrep.simx_opmode_streaming)


	def __load_component(self, component_name):
		robot_status, component = vrep.simxGetObjectHandle(self.clientID, component_name, vrep.simx_opmode_oneshot_wait)
		if robot_status != vrep.simx_return_ok:
			raise RuntimeError('Error loading object {component}'.format(component=component_name))

		return component


	def __controlCommandsOnServer(self, command, object):
		if not self.command_on_server:
			self.command_on_server[command] = {object: False}

		if command not in self.command_on_server:
			self.command_on_server[command] = {object: False}

		if object not in self.command_on_server[command]:
			self.command_on_server[command][object] = True
			return vrep.simx_opmode_streaming
		else:
			return vrep.simx_opmode_buffer


	def isConnected(self):
		if vrep.simxGetConnectionId(self.clientID) != -1:
			return True


	def close(self):
		vrep.simxGetPingTime(self.clientID)
		vrep.simxFinish(self.clientID)