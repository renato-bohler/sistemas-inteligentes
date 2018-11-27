import math
import pdb
import pickle
import sys
import time

import numpy as np
import skfuzzy.control as ctrl
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

import vrep

PI = math.pi

vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

if clientID != -1:
	print('Connected to remote API server')
else:
	sys.exit('Could not connect')

returnCode, KJuniorHandle = vrep.simxGetObjectHandle(clientID, 'KJunior', vrep.simx_opmode_oneshot_wait)
returnCode, KJuniorLeftHandle = vrep.simxGetObjectHandle(clientID, 'KJunior_motorLeft', vrep.simx_opmode_oneshot_wait)
returnCode, KJuniorRightHandle = vrep.simxGetObjectHandle(clientID, 'KJunior_motorRight', vrep.simx_opmode_oneshot_wait)

# returnCode, BubbleRobHandle      = vrep.simxGetObjectHandle(clientID, 'bubbleRob',            vrep.simx_opmode_oneshot_wait)
# returnCode, BubbleRobLeftHandle  = vrep.simxGetObjectHandle(clientID, 'bubbleRob_leftMotor',  vrep.simx_opmode_oneshot_wait)
# returnCode, BubbleRobRightHandle = vrep.simxGetObjectHandle(clientID, 'bubbleRob_rightMotor', vrep.simx_opmode_oneshot_wait)

returnCode, LaptopHandle = vrep.simxGetObjectHandle(clientID, 'laptop', vrep.simx_opmode_oneshot_wait)

from fcl_parser import FCLParser

# Fuzzy FCL file reader
parser = FCLParser()  # Create the parser
parser.read_fcl_file('wheelRules.fcl')  # Parse a file

wheelControl = ctrl.ControlSystem(parser.rules)
wheelFuzzy = ctrl.ControlSystemSimulation(wheelControl)

KJuniorProxSensors = []
KJuniorProxSensorsVal = []

for i in [1, 2, 4, 5]:
	errorCode, proxSensor = vrep.simxGetObjectHandle(clientID, 'KJunior_proxSensor' + str(i), vrep.simx_opmode_oneshot_wait)
	KJuniorProxSensors.append(proxSensor)
	errorCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, proxSensor, vrep.simx_opmode_streaming)
	distance = round(2000 - np.linalg.norm(detectedPoint) * 20000, 2)
	if distance <= 0 or distance == 2000:
		distance = 0
	KJuniorProxSensorsVal.append(distance)

# Current KJunior and Objective position
errorCode, KJuniorCurrentPosition = vrep.simxGetObjectPosition(clientID, KJuniorHandle, -1, vrep.simx_opmode_streaming)
errorCode, LaptopPosition = vrep.simxGetObjectPosition(clientID, LaptopHandle, -1, vrep.simx_opmode_streaming)

# Orientation related to Origin
errorCode, _KJuniorOrientation = vrep.simxGetObjectOrientation(clientID, KJuniorHandle, -1, vrep.simx_opmode_streaming)
KJuniorOrientationOrigin = [math.degrees(_KJuniorOrientation[0]), math.degrees(_KJuniorOrientation[1]), math.degrees(_KJuniorOrientation[2])]

# Orientation related to Objective
KJuniorOrientationObjective = math.degrees(
	math.atan2(KJuniorCurrentPosition[1] - LaptopPosition[1], KJuniorCurrentPosition[0] - LaptopPosition[0])
	)

reachedDestination = False


dataframe = pd.DataFrame()

columns = ['leftSensor',
           'centerLeftSensor',
           'centerRightSensor',
           'rightSensor',
           'orientation',
           'leftVel',
           'rightVel'
           ]


loaded_model = pickle.load(open('model.sav', 'rb'))
labels_scaler:MinMaxScaler = pickle.load(open('labels_scaler', 'rb'))
orientation_scaler: MinMaxScaler = pickle.load(open('orientation_scaler', 'rb'))
sensors_scaler: MinMaxScaler = pickle.load(open('sensors_scaler', 'rb'))


while not reachedDestination:
	# Current KJunior and Objective position
	errorCode, KJuniorCurrentPosition = vrep.simxGetObjectPosition(clientID, KJuniorHandle, -1, vrep.simx_opmode_buffer)
	errorCode, LaptopPosition = vrep.simxGetObjectPosition(clientID, LaptopHandle, -1, vrep.simx_opmode_buffer)

	# Orientation related to X axis
	errorCode, _KJuniorOrientation = vrep.simxGetObjectOrientation(clientID, KJuniorHandle, -1, vrep.simx_opmode_buffer)
	KJuniorOrientationOrigin = [math.degrees(_KJuniorOrientation[0]), math.degrees(_KJuniorOrientation[1]), math.degrees(_KJuniorOrientation[2])]
	KJuniorOrientationRelativeToX = 0
	if KJuniorOrientationOrigin[2] >= 0:
		KJuniorOrientationRelativeToX = KJuniorOrientationOrigin[1] * -1
	else:
		if KJuniorOrientationOrigin[1] < 0:
			KJuniorOrientationRelativeToX = 180 - abs(KJuniorOrientationOrigin[1])
		else:
			KJuniorOrientationRelativeToX = (180 - KJuniorOrientationOrigin[1]) * -1

	# Orientation related to Objective
	KJuniorOrientationObjective = math.degrees(
		math.atan2(LaptopPosition[1] - KJuniorCurrentPosition[1], LaptopPosition[0] - KJuniorCurrentPosition[0])
		) * -1

	# Orientation relative to my view and objective
	KJuniorOrientation = KJuniorOrientationRelativeToX - KJuniorOrientationObjective

	# Read sensors
	KJuniorProxSensorsVal = []
	for i in [1, 2, 4, 5]:
		distance = 0
		errorCode, proxSensor = vrep.simxGetObjectHandle(clientID, 'KJunior_proxSensor' + str(i), vrep.simx_opmode_oneshot_wait)
		errorCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, proxSensor, vrep.simx_opmode_buffer)
		# Normalize distance
		distance = round(2000 - np.linalg.norm(detectedPoint) * 20000, 2)
		# print(proxSensor, 'read', detectedPoint, 'with distance of', distance, 'detectionState', detectionState, 'errorCode', errorCode)
		if detectedObjectHandle == LaptopHandle:
			print('Reached destination!!!!!!!')
			reachedDestination = True
		if distance <= 0 or distance == 2000 or not detectionState:
			distance = 0
		KJuniorProxSensorsVal.append(distance)

	# FUZZY

	# save this sensors data below

	data = []
	leftVel = 0
	rightVel = 0
	try:

		leftSensor = KJuniorProxSensorsVal[0]
		centerLeftSensor = KJuniorProxSensorsVal[1]
		centerRightSensor = KJuniorProxSensorsVal[2]
		rightSensor= KJuniorProxSensorsVal[3]
		orientation = KJuniorOrientation

		sensors_data = [[leftSensor, centerLeftSensor, centerRightSensor, rightSensor]]
		scaled_sensor = sensors_scaler.transform(sensors_data)

		scaled_orientation = orientation_scaler.transform([[orientation]])


		values = np.c_[scaled_sensor, scaled_orientation]

		prediction = loaded_model.predict(values)

		scaled_labels = labels_scaler.inverse_transform(prediction)

		leftVel = scaled_labels[0][0]
		rightVel = scaled_labels[0][1]

		## For savin fuzzy
		# wheelFuzzy.input['leftSensor'] = leftSensor
		# wheelFuzzy.input['centerLeftSensor'] = centerLeftSensor
		# wheelFuzzy.input['centerRightSensor'] = centerRightSensor
		# wheelFuzzy.input['rightSensor'] = rightSensor
		# wheelFuzzy.input['orientation'] = orientation

		# data = [leftSensor,
		#         centerLeftSensor,
		#         centerRightSensor,
		#         rightSensor,
		#         orientation
		#         ]

	except:
		print('ERROR IN INPUTS!!!!!!!!!!!!!!')
		print('ERROR IN INPUTS!!!!!!!!!!!!!!')
		print('ERROR IN INPUTS!!!!!!!!!!!!!!')
		print('ERROR IN INPUTS!!!!!!!!!!!!!!')
		print('ERROR IN INPUTS!!!!!!!!!!!!!!')
		pdb.set_trace()


	# leftVel = wheelFuzzy.output['leftWheelVel']
	# rightVel = wheelFuzzy.output['rightWheelVel']



	## add fuzzy result to dataset
	# newDataframe = pd.DataFrame(data=[data + [leftVel, rightVel]], columns=columns)
	# dataframe = dataframe.append(newDataframe)

	errorCode = vrep.simxSetJointTargetVelocity(clientID, KJuniorLeftHandle, leftVel, vrep.simx_opmode_streaming)
	errorCode = vrep.simxSetJointTargetVelocity(clientID, KJuniorRightHandle, rightVel, vrep.simx_opmode_streaming)

	time.sleep(0.5)

## Save fuzzy control values
# dataframe.to_csv('robot_walk.csv', header=False, index=False, mode='a')
errorCode = vrep.simxSetJointTargetVelocity(clientID, KJuniorLeftHandle, 0, vrep.simx_opmode_streaming)
errorCode = vrep.simxSetJointTargetVelocity(clientID, KJuniorRightHandle, 0, vrep.simx_opmode_streaming)
errorCode = vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
