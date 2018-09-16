# Autores: Davi Boberg e Renato Böhler
from subprocess import call

class RobotControl():

	map_command_direction = {
		'straight': '8',
		'left': '4',
		'right': '6',
	}

	@staticmethod
	def execute_commands(directions):
		project_api = './ProjetoRemoteApi/cppremoteapi'
		commands = RobotControl.convert_to_commands(directions)
		commands.insert(0, project_api)
		call(commands)

	@staticmethod
	def convert_to_commands(directions):
		commands = []
		for direction in directions:
			commands.append(RobotControl.map_command_direction[direction])

		return commands