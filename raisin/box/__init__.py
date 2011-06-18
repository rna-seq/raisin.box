import os
from configobj import ConfigObj

RESOURCES = ConfigObj(os.path.join(os.path.dirname(__file__), "resources.ini"), 
                      interpolation=False)
BOXES = ConfigObj(os.path.join(os.path.dirname(__file__), "boxes.ini"))

# All boxes are registered here
resources_registry = []

import boxes
