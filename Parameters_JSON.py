from dataclasses import dataclass
from dataclass_wizard import JSONWizard
import json

@dataclass
class ParametersList(JSONWizard):
    """
    A class containing ParametersGC class.
    """
    globular_cluster: list['ParametersGC']


@dataclass
class ParametersGC:
    """
    Class containing values/parameters saved into a JSON file. These values
    will be used to, generally, to plot or analyze data that belongs to a cluster
    with name 'name'.
    """
    name: str = ''
    PM_plot_x_axis_min: float = 0.
    PM_plot_x_axis_max: float = 0.
    PM_plot_y_axis_min: float = 0.
    PM_plot_y_axis_max: float = 0.
    width_minim: float = 0.
    width_maxim : float = 0.
    width_nstep: int = 0
    height_minim: float = 0.
    height_maxim: float = 0.
    height_nstep: int = 0
    incl_minim: float = 0.
    incl_maxim: float = 0.
    incl_nstep: int = 0


def isInJSONParametersFile(filename_json: str) -> (ParametersGC, bool):
    """
    Checks if the current object name has already been studied/analyzed checking
    if it is in 'filename_json' JSON file. If the object is present it will return
    the parameters that belongs to the object contained in JSON file into the form 
    of a ParametersGC object; and also will return a True (indicating it is present 
    in Parameters JSON file). 
    If the object is not present it will return a simple ParameterGC object (with
    only 0 values and an empty 'name') and a False (indicating it is not present in 
    Parameters JSON file).
    """
    # Read JSON file
    with open(filename_json, 'r') as j:
        data_json = json.loads(j.read())
    
    # Load JSON data (dictionary) into our custom class
    object_json = ParametersList.from_dict(data_json)
    
    # Check if the object is in the list of previously studied objects
    for item in object_json.globular_cluster:
        if item.name.upper() == object_name.upper():
            cluster_found = ParametersGC(name=item.name, 
                                         PM_plot_x_axis_min=float(item.PM_plot_x_axis_min),
                                         PM_plot_x_axis_max=float(item.PM_plot_x_axis_max),
                                         PM_plot_y_axis_min=float(item.PM_plot_y_axis_min),
                                         PM_plot_y_axis_max=float(item.PM_plot_y_axis_max),
                                         width_minim=float(item.width_minim),
                                         width_maxim=float(item.width_maxim),
                                         width_nstep=int(item.width_nstep),
                                         height_minim=float(item.height_minim),
                                         height_maxim=float(item.height_maxim),
                                         height_nstep=int(item.height_nstep),
                                         incl_minim=float(item.incl_minim),
                                         incl_maxim=float(item.incl_maxim),
                                         incl_nstep=int(item.incl_nstep))
            return cluster_found, True
    
    return ParametersGC(), False
