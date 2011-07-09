"""Provide information about boxes and the associated resources

RESOURCES: Read from the resources.ini file

    * Used by raisin.restyler to fetch the resource

BOXES: Read from the boxes.ini file

    * Used by raisin.restyler to verify that a box id passed in a url really exists

    * Used by raisin.restyler to get meta information about the boxes

resources_registry: A list of registered resources. For each resource it contains

    * the name of the resource
    
    * the method to call for augmenting the box information obtained from BOXES
    
    * the list of formats that the augmentation method needs
    
"""

import os
from configobj import ConfigObj

RESOURCES = ConfigObj(os.path.join(os.path.dirname(__file__), "resources.ini"), 
                      interpolation=False)
BOXES = ConfigObj(os.path.join(os.path.dirname(__file__), "boxes.ini"))

# All boxes are registered here
resources_registry = []

import boxes
