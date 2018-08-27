from RobotControl import RobotControl

robot_control = RobotControl()

commands = {
	'8': 'straight',
	'4': 'left',
	'6': 'right',
}

while robot_control.simulator.isConnected():

	print('''
		Comandos:
		Frente: 8
		Esquerda: 4
		Direita: 6
		
	''')
	command = input()
	if command not in commands:
		print('Comando Invalido')
		continue

	robot_control.run(commands[command])
	command = 0

	while robot_control.isWalking():
		continue
	print('Stopped')
	print(command)


robot_control.simulator.close()