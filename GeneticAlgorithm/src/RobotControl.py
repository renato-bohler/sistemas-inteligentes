from subprocess import call

class RobotControl():

	map_command_direction = {
		'straight': '8',
		'left': '4',
		'right': '6',
	}

	def execute_commands(self, directions):
		project_api = './ProjetoRemoteApi/cppremoteapi'
		commands = self.convert_to_commands(directions)
		commands.insert(0, project_api)
		call(commands)

	def convert_to_commands(self, directions):
		commands = []
		for direction in directions:
			commands.append(self.map_command_direction[direction])

		return commands