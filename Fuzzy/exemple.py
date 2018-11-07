# from fcl_parser import FCLParser

# p = FCLParser()    # Create the parser
# p.read_fcl_file('tests/tipper.fcl')  # Parse a file

# print(p)
# ... and so on, as usual for skfuzzy:
# cs = ctrl.ControlSystem(p.rules)


import vrep
import sys
import numpy as np
import math
import time
import skfuzzy as fuzz
import skfuzzy.control as ctrl



from fcl_parser import FCLParser

parser = FCLParser()    # Create the parser
parser.read_fcl_file('wheelRules.fcl')  # Parse a file

wheelControl = ctrl.ControlSystem(parser.rules)
wheelFuzzy   = ctrl.ControlSystemSimulation(wheelControl)

print(wheelControl.view())
print(wheelFuzzy.view())