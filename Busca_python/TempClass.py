from src import vrep
#from src import vrepConst
# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!


# Variaveis robo
VEL_MOT = 4.25 #tecnicamente em rad/s
DIS_RETO = 0.05 #tamanho do passo em m ate inicio da leitura dos sensores
DIS_CURVA = 0.262 #delta para virar PI, ja que ha o delay de comunicacao e eh float, nunca igual, (~VEL_MOT/(7.5PI)) - aleatorio
D_ANG = 0.1 #delta para captacao de salto da atan, (~DIS_CURVA-0.1)
MAX_INTE = 0.2 #delta para media ta intensidade. tecnicamente, deve ser zero
CONT = 0 #contador para comecar virar


import time

print ('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
	print ('Connected to remote API server')

	leftMotorHandle = 0
	rightMotorHandle = 0
	bubbleRob = 0
	turnleft = 0
	turnright = 0

	# inteiros para sensores de visao
	Left_Vision_sensor = 0
	LM_Vision_sensor = 0
	Middle_Vision_sensor = 0
	RM_Vision_sensor = 0
	Right_Vision_sensor = 0

	# inteiros para sensores ultrassom e os objetos detectados
	Left_ultrasonic = 0
	LM_ultrasonic = 0
	Middle_ultrasonic = 0
	RM_ultrasonic = 0
	Right_ultrasonic = 0

	detectedObjetHandleMU = 0

	# variaveis para movimentacao do robo
	vLeft = 0
	vRight = 0
	dx = 0
	dy = 0
	X_inicial = 0
	Y_inicial = 0
	d_ang = 0
	ang_inicial = 0
	ang = 0

	# inicialização dos motores e do robo
	bubbleRob_status, bubbleRob = vrep.simxGetObjectHandle(clientID, "bubbleRob", vrep.simx_opmode_oneshot_wait)
	if (bubbleRob_status == vrep.simx_return_ok):
		print("conectado ao bubbleRob")

	Left_ultrasonic_status, Left_ultrasonic = vrep.simxGetObjectHandle(clientID, "Left_ultrasonic", vrep.simx_opmode_oneshot_wait)
	LM_ultrasonic_status, LM_ultrasonic = vrep.simxGetObjectHandle(clientID, "LM_ultrasonic",  vrep.simx_opmode_oneshot_wait)
	Middle_ultrasonic_status, Middle_ultrasonic = vrep.simxGetObjectHandle(clientID, "Middle_ultrasonic", vrep.simx_opmode_oneshot_wait)
	RM_ultrasonic_status, RM_ultrasonic = vrep.simxGetObjectHandle(clientID, "RM_ultrasonic", vrep.simx_opmode_oneshot_wait)
	Right_ultrasonic_status, Right_ultrasonic = vrep.simxGetObjectHandle(clientID, "Right_ultrasonic", vrep.simx_opmode_oneshot_wait)

	if (Left_ultrasonic_status == vrep.simx_return_ok
			and LM_ultrasonic_status == vrep.simx_return_ok
			and Middle_ultrasonic_status == vrep.simx_return_ok
			and RM_ultrasonic_status == vrep.simx_return_ok
			and Right_ultrasonic_status == vrep.simx_return_ok):
		print("conectado aos sensores ultrassom")

	Left_Vision_sensor_status, Left_Vision_sensor = vrep.simxGetObjectHandle(clientID, "Left_Vision_sensor", vrep.simx_opmode_oneshot_wait)
	LM_Vision_sensor_status, LM_Vision_sensor = vrep.simxGetObjectHandle(clientID, "LM_Vision_sensor", vrep.simx_opmode_oneshot_wait)
	Middle_Vision_sensor_status, Middle_Vision_sensor = vrep.simxGetObjectHandle(clientID, "Middle_Vision_sensor", vrep.simx_opmode_oneshot_wait)
	RM_Vision_sensor_status, RM_Vision_sensor = vrep.simxGetObjectHandle(clientID, "RM_Vision_sensor", vrep.simx_opmode_oneshot_wait)
	Right_Vision_sensor_status, Right_Vision_sensor = vrep.simxGetObjectHandle(clientID, "Right_Vision_sensor", vrep.simx_opmode_oneshot_wait)

	if (Left_Vision_sensor_status == vrep.simx_return_ok
			and LM_Vision_sensor_status == vrep.simx_return_ok
			and Middle_Vision_sensor_status == vrep.simx_return_ok
			and RM_Vision_sensor_status == vrep.simx_return_ok
			and Right_Vision_sensor_status == vrep.simx_return_ok):
		print("conectado aos sensores de visao")

	leftMotorHandle_status, leftMotorHandle = vrep.simxGetObjectHandle(clientID, "bubbleRob_leftMotor", vrep.simx_opmode_oneshot_wait)

	if (leftMotorHandle_status != vrep.simx_return_ok):
		print("Handle do motor esquerdo nao encontrado!")
	else:
		print("Conectado ao motor esquerdo!")

	rightMotorHandle_status, rightMotorHandle = vrep.simxGetObjectHandle(clientID, "bubbleRob_rightMotor", vrep.simx_opmode_oneshot_wait)

	if (rightMotorHandle_status != vrep.simx_return_ok):
		print("Handle do motor direito nao encontrado!")
	else:
		print("Conectado ao motor direito!")

	_, angle = vrep.simxGetObjectOrientation(clientID, bubbleRob, -1, vrep.simx_opmode_streaming) # alpha, beta e gamma.Usa - se o gamma
	_, position = vrep.simxGetObjectPosition(clientID, bubbleRob, -1, vrep.simx_opmode_streaming) # x, y, z.Nao usa - se o z
	_, readingMU, detectedObjetMU, detectedObjetHandleMU, detectedSurfaceMU = vrep.simxReadProximitySensor(clientID, Middle_ultrasonic, vrep.simx_opmode_streaming) # apenas ultrassom central esta sendo usado
	_, readingLVS, DataLVS = vrep.simxReadVisionSensor(clientID, Left_Vision_sensor, vrep.simx_opmode_streaming)
	_, readingLMVS, DataLMVS = vrep.simxReadVisionSensor(clientID, LM_Vision_sensor, vrep.simx_opmode_streaming)
	_, readingMVS, DataMVS = vrep.simxReadVisionSensor(clientID, Middle_Vision_sensor, vrep.simx_opmode_streaming)
	_, readingRMVS, DataRMVS = vrep.simxReadVisionSensor(clientID, RM_Vision_sensor, vrep.simx_opmode_streaming)
	_, readingRVS, DataRVS = vrep.simxReadVisionSensor(clientID, Right_Vision_sensor, vrep.simx_opmode_streaming)

	auxLVS = len(DataLVS)
	auxLMVS = len(DataLMVS)
	auxMVS = len(DataMVS)
	auxRMVS = len(DataRMVS)
	auxRVS = len(DataRVS)

	while (vrep.simxGetConnectionId(clientID) != -1):

		_, position = vrep.simxGetObjectPosition(clientID, bubbleRob, -1, vrep.simx_opmode_buffer)
		_, angle = vrep.simxGetObjectOrientation(clientID, bubbleRob, -1, vrep.simx_opmode_buffer)
		X_inicial = position[0]
		Y_inicial = position[1]
		ang_inicial = angle[2]
		# virar para esquerda, ang aumenta.direita, diminui
		_, readingMU, detectedObjetMU, detectedObjetHandleMU, detectedSurfaceMU = vrep.simxReadProximitySensor(clientID, Middle_ultrasonic, vrep.simx_opmode_buffer)
		read, readingLVS, DataLVS = vrep.simxReadVisionSensor(clientID, Left_Vision_sensor, vrep.simx_opmode_buffer)
		_, readingLMVS, DataLMVS = vrep.simxReadVisionSensor(clientID, LM_Vision_sensor, vrep.simx_opmode_buffer)
		_, readingMVS, DataMVS = vrep.simxReadVisionSensor(clientID, Middle_Vision_sensor, vrep.simx_opmode_buffer)
		_, readingRMVS, DataRMVS = vrep.simxReadVisionSensor(clientID, RM_Vision_sensor, vrep.simx_opmode_buffer)
		_, readingRVS, DataRVS = vrep.simxReadVisionSensor(clientID, Right_Vision_sensor, vrep.simx_opmode_buffer)

		auxLVS = len(DataLVS)
		auxLMVS = len(DataLMVS)
		auxMVS = len(DataMVS)
		auxRMVS = len(DataRMVS)
		auxRVS = len(DataRVS)

		readingLVS = DataLVS[10] < MAX_INTE if auxLVS > 10 else 0
		readingLMVS = DataLMVS[10] < MAX_INTE if auxLMVS > 10 else 0
		readingMVS = DataMVS[10] < MAX_INTE if auxMVS > 10 else 0
		readingRMVS = DataRMVS[10] < MAX_INTE if auxRMVS > 10 else 0
		readingRVS = DataRVS[10] < MAX_INTE if auxRVS > 10 else 0


		#if (*(comando1.first) == 8 & & )

		if readingMU is False:

			while (((readingLVS and readingMVS) or (readingMVS and readingRVS)) and readingMU == 0):
				# verificar se ta no mesmo estado, tecnicamente inutil devido a funcao acima
				vLeft = VEL_MOT
				vRight = VEL_MOT
				vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft, vrep.simx_opmode_streaming)
				vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight, vrep.simx_opmode_streaming)
				_, readingMU, detectedObjetMU, detectedObjetHandleMU, detectedSurfaceMU, = vrep.simxReadProximitySensor(clientID, Middle_ultrasonic, vrep.simx_opmode_buffer)
				_, readingLVS, DataLVS = vrep.simxReadVisionSensor(clientID, Left_Vision_sensor, vrep.simx_opmode_buffer)
				_, readingMVS, DataMVS = vrep.simxReadVisionSensor(clientID, Middle_Vision_sensor, vrep.simx_opmode_buffer)
				_, readingRVS, DataRVS = vrep.simxReadVisionSensor(clientID, Right_Vision_sensor, vrep.simx_opmode_buffer)

				auxLVS = len(DataLVS)
				auxMVS = len(DataMVS)
				auxRVS = len(DataRVS)

				readingLVS = DataLVS[10] < MAX_INTE if auxLVS > 10 else 0
				readingMVS = DataMVS[10] < MAX_INTE if auxMVS > 10 else 0
				readingRVS = DataRVS[10] < MAX_INTE if auxRVS > 10 else 0

				#vrep.extApi_sleepMs(5)
				time.sleep(5 / 1000.0)
				if (readingMU):

					print("objeto ", detectedObjetHandleMU, " na posicao ", detectedObjetMU[0], ", ", detectedObjetMU[1], ", ", detectedObjetMU[2])
					print("superficie em ", detectedSurfaceMU[0], ", ",  detectedSurfaceMU[1], ", ", detectedSurfaceMU[2])

			while (not ((readingLVS and readingMVS) or (readingMVS and readingRVS)) and readingMU == 0):
				#anda ate os sensores captarem a linha ou obstaculo
				vLeft = VEL_MOT
				vRight = VEL_MOT
				result = vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft , vrep.simx_opmode_streaming)
				vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight , vrep.simx_opmode_streaming)
				_, readingMU, detectedObjetMU, detectedObjetHandleMU, detectedSurfaceMU = vrep.simxReadProximitySensor(clientID,Middle_ultrasonic, vrep.simx_opmode_buffer)
				_,  readingLVS, DataLVS = vrep.simxReadVisionSensor(clientID, Left_Vision_sensor,vrep.simx_opmode_buffer)
				_,  readingLMVS, DataLMVS = vrep.simxReadVisionSensor(clientID, LM_Vision_sensor,vrep.simx_opmode_buffer)
				_,  readingMVS, DataMVS = vrep.simxReadVisionSensor(clientID, Middle_Vision_sensor,vrep.simx_opmode_buffer)
				_,  readingRMVS, DataRMVS = vrep.simxReadVisionSensor(clientID, RM_Vision_sensor,vrep.simx_opmode_buffer)
				_,  readingRVS, DataRVS = vrep.simxReadVisionSensor(clientID, Right_Vision_sensor,vrep.simx_opmode_buffer)

				auxLVS = len(DataLVS)
				auxLMVS = len(DataLMVS)
				auxMVS = len(DataMVS)
				auxRMVS = len(DataRMVS)
				auxRVS = len(DataRVS)

				readingLVS = DataLVS[10] < MAX_INTE if auxLVS > 10 else 0
				readingLMVS = DataLMVS[10] < MAX_INTE if auxLMVS > 10 else 0
				readingMVS = DataMVS[10] < MAX_INTE if auxMVS > 10 else 0
				readingRMVS = DataRMVS[10] < MAX_INTE if auxRMVS > 10 else 0
				readingRVS = DataRVS[10] < MAX_INTE if auxRVS > 10 else 0


				if (readingRVS):

					vLeft = VEL_MOT
					vRight = VEL_MOT / 4
					vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft, vrep.simx_opmode_streaming)
					vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight, vrep.simx_opmode_streaming)
					_, readingMU, detectedObjetMU, detectedObjetHandleMU, detectedSurfaceMU = vrep.simxReadProximitySensor(clientID, Middle_ultrasonic, vrep.simx_opmode_buffer)
					_, readingLVS, DataLVS = vrep.simxReadVisionSensor(clientID, Left_Vision_sensor, vrep.simx_opmode_buffer)
					_, readingMVS, DataMVS = vrep.simxReadVisionSensor(clientID, Middle_Vision_sensor, vrep.simx_opmode_buffer)
					_, readingRVS, DataRVS = vrep.simxReadVisionSensor(clientID, Right_Vision_sensor, vrep.simx_opmode_buffer)


					auxLVS = len(DataLVS)
					auxMVS = len(DataMVS)
					auxRVS = len(DataRVS)

					readingLVS = DataLVS[10] < MAX_INTE if auxLVS > 10 else 0
					readingMVS = DataMVS[10] < MAX_INTE if auxMVS > 10 else 0
					readingRVS = DataRVS[10] < MAX_INTE if auxRVS > 10 else 0

					turnright = 1
					turnleft = 0
				elif (readingRMVS):
					vLeft = VEL_MOT
					vRight = VEL_MOT / 2
					vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft, vrep.simx_opmode_streaming)
					vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight, vrep.simx_opmode_streaming)
					_, readingMU, detectedObjetMU, detectedObjetHandleMU, detectedSurfaceMU = vrep.simxReadProximitySensor(clientID, Middle_ultrasonic, vrep.simx_opmode_buffer)
					_, readingLVS, DataLVS = vrep.simxReadVisionSensor(clientID, Left_Vision_sensor, vrep.simx_opmode_buffer)
					_, readingMVS, DataMVS = vrep.simxReadVisionSensor(clientID, Middle_Vision_sensor, vrep.simx_opmode_buffer)
					_, readingRVS, DataRVS = vrep.simxReadVisionSensor(clientID, Right_Vision_sensor, vrep.simx_opmode_buffer)

					auxLVS = len(DataLVS)
					auxMVS = len(DataMVS)
					auxRVS = len(DataRVS)

					readingLVS = DataLVS[10] < MAX_INTE if auxLVS > 10 else 0
					readingMVS = DataMVS[10] < MAX_INTE if auxMVS > 10 else 0
					readingRVS = DataRVS[10] < MAX_INTE if auxRVS > 10 else 0

					turnright = 1
					turnleft = 0
				elif (readingLMVS): # robo ta desviando para a direita, gira esquerda

					vLeft = VEL_MOT / 2
					vRight = VEL_MOT
					vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft, vrep.simx_opmode_streaming)
					vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight, vrep.simx_opmode_streaming)
					_, readingMU, detectedObjetMU, detectedObjetHandleMU, detectedSurfaceMU = vrep.simxReadProximitySensor(clientID, Middle_ultrasonic, vrep.simx_opmode_buffer)
					_, readingLVS, DataLVS = vrep.simxReadVisionSensor(clientID, Left_Vision_sensor, vrep.simx_opmode_buffer)
					_, readingMVS, DataMVS = vrep.simxReadVisionSensor(clientID, Middle_Vision_sensor, vrep.simx_opmode_buffer)
					_, readingRVS, DataRVS = vrep.simxReadVisionSensor(clientID, Right_Vision_sensor, vrep.simx_opmode_buffer)

					auxLVS = len(DataLVS)
					auxMVS = len(DataMVS)
					auxRVS = len(DataRVS)

					readingLVS = DataLVS[10] < MAX_INTE if auxLVS > 10 else 0
					readingMVS = DataMVS[10] < MAX_INTE if auxMVS > 10 else 0
					readingRVS = DataRVS[10] < MAX_INTE if auxRVS > 10 else 0

					turnright = 0
					turnleft = 1
				elif (readingLVS): #robo ta desviando para a direita, gira esquerda
					vLeft = VEL_MOT / 4
					vRight = VEL_MOT
					vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft, vrep.simx_opmode_streaming)
					vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight, vrep.simx_opmode_streaming)
					_, readingMU, detectedObjetMU, detectedObjetHandleMU, detectedSurfaceMU = vrep.simxReadProximitySensor(clientID, Middle_ultrasonic, vrep.simx_opmode_buffer)
					_, readingLVS, DataLVS = vrep.simxReadVisionSensor(clientID, Left_Vision_sensor, vrep.simx_opmode_buffer)
					_, readingMVS, DataMVS = vrep.simxReadVisionSensor(clientID, Middle_Vision_sensor, vrep.simx_opmode_buffer)
					_, readingRVS, DataRVS = vrep.simxReadVisionSensor(clientID, Right_Vision_sensor, vrep.simx_opmode_buffer)

					auxLVS = len(DataLVS)
					auxMVS = len(DataMVS)
					auxRVS = len(DataRVS)

					readingLVS = DataLVS[10] < MAX_INTE if auxLVS > 10 else 0
					readingMVS = DataMVS[10] < MAX_INTE if auxMVS > 10 else 0
					readingRVS = DataRVS[10] < MAX_INTE if auxRVS > 10 else 0

					turnright = 0
					turnleft = 1

				elif (not (readingLVS or readingLMVS or readingMVS or readingRMVS or readingRMVS)):
					if (turnright):
						vLeft = VEL_MOT
						vRight = VEL_MOT / 4
						vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft, vrep.simx_opmode_streaming)
						vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight, vrep.simx_opmode_streaming)
						_, readingMU, detectedObjetMU, detectedObjetHandleMU, detectedSurfaceMU,  = vrep.simxReadProximitySensor(clientID, Middle_ultrasonic, vrep.simx_opmode_buffer)
						_, readingLVS, DataLVS = vrep.simxReadVisionSensor(clientID, Left_Vision_sensor, vrep.simx_opmode_buffer)
						_, readingMVS, DataMVS = vrep.simxReadVisionSensor(clientID, Middle_Vision_sensor, vrep.simx_opmode_buffer)
						_, readingRVS, DataRVS = vrep.simxReadVisionSensor(clientID, Right_Vision_sensor, vrep.simx_opmode_buffer)

						auxLVS = len(DataLVS)
						auxMVS = len(DataMVS)
						auxRVS = len(DataRVS)

						readingLVS = DataLVS[10] < MAX_INTE if auxLVS > 10 else 0
						readingMVS = DataMVS[10] < MAX_INTE if auxMVS > 10 else 0
						readingRVS = DataRVS[10] < MAX_INTE if auxRVS > 10 else 0

					elif (turnleft):
						vLeft = VEL_MOT / 4
						vRight = VEL_MOT
						vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft, vrep.simx_opmode_streaming)
						vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight, vrep.simx_opmode_streaming)
						_, readingMU, detectedObjetMU, detectedObjetHandleMU, detectedSurfaceMU = vrep.simxReadProximitySensor(clientID, Middle_ultrasonic, vrep.simx_opmode_buffer)
						_, readingLVS, DataLVS = vrep.simxReadVisionSensor(clientID, Left_Vision_sensor, vrep.simx_opmode_buffer)
						_, readingMVS, DataMVS = vrep.simxReadVisionSensor(clientID, Middle_Vision_sensor, vrep.simx_opmode_buffer)
						_, readingRVS, DataRVS = vrep.simxReadVisionSensor(clientID, Right_Vision_sensor, vrep.simx_opmode_buffer)

						auxLVS = len(DataLVS)
						auxMVS = len(DataMVS)
						auxRVS = len(DataRVS)

						readingLVS = DataLVS[10] < MAX_INTE if auxLVS > 10 else 0
						readingMVS = DataMVS[10] < MAX_INTE if auxMVS > 10 else 0
						readingRVS = DataRVS[10] < MAX_INTE if auxRVS > 10 else 0

				if (readingMU):
					print("objeto ", detectedObjetHandleMU, " na posicao ", detectedObjetMU[0], ", ", detectedObjetMU[1], ", ", detectedObjetMU[2])
					print("superficie em ", detectedSurfaceMU[0], ", ", detectedSurfaceMU[1], ", ", detectedSurfaceMU[2])
				#extApi_sleepMs(5)
				time.sleep(5 / 1000.0)

			_, position = vrep.simxGetObjectPosition(clientID, bubbleRob, -1, vrep.simx_opmode_buffer)
			X_inicial = position[0]
			Y_inicial = position[1]
			dx = 0
			dy = 0

			while ((dx < DIS_RETO and dy < DIS_RETO) and readingMU == 0):  # chegar na linha
				vLeft = VEL_MOT
				vRight = VEL_MOT
				vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft, vrep.simx_opmode_streaming)
				vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight, vrep.simx_opmode_streaming)
				_, position = vrep.simxGetObjectPosition(clientID, bubbleRob, -1, vrep.simx_opmode_buffer)
				_, readingMU, detectedObjetMU, detectedObjetHandleMU, detectedSurfaceMU = vrep.simxReadProximitySensor(clientID,Middle_ultrasonic, vrep.simx_opmode_buffer)
				dx = abs(position[0] - X_inicial)
				dy = abs(position[1] - Y_inicial)
				#extApi_sleepMs(5)
				time.sleep(5 / 1000.0)
				if (readingMU):
					print("objeto ", detectedObjetHandleMU, " na posicao ", detectedObjetMU[0], ", ", detectedObjetMU[1], ", ", detectedObjetMU[2])
					print("superficie em ", detectedSurfaceMU[0], ", ", detectedSurfaceMU[1], ", ", detectedSurfaceMU[2])

		# zera variaveis e manda o robo parar
		X_inicial = 0
		Y_inicial = 0
		dx = 0
		dy = 0
		d_ang = 0
		ang = 0
		vLeft = 0
		vRight = 0
		vrep.simxSetJointTargetVelocity(clientID, leftMotorHandle, vLeft, vrep.simx_opmode_streaming)
		vrep.simxSetJointTargetVelocity(clientID, rightMotorHandle, vRight, vrep.simx_opmode_streaming)
		#extApi_sleepMs(5);
		time.sleep(5/1000.0)

	# Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
	vrep.simxGetPingTime(clientID)

	# Now close the connection to V-REP:
	vrep.simxFinish(clientID)

else:
	print ('Failed connecting to remote API server')
print ('Program ended')
