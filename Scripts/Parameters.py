from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard
import json
import numpy as np


class Error(Exception):
    """Base class for other exceptions"""
    pass


class ClusterNotFound(Error):
    """
    Custom error class to indicate the object provided by the user is not in the
    file provided by Vasiliev (2019) and Harris (2010)
    """
    pass


@dataclass(frozen=True, order=True, kw_only=True)
class VasilievData:
    """
    An object/struct used to store data loaded from Vasiliev (2019) file.
    """
    name: str #object name
    RA: float #object RA coordinates (J2000)
    DEC: float #object DEC coordinates (J2000)
    distance: float # Harris (2010) distance in kpc
    losv: float # line of sight velocity in km/s
    err_losv: float # error of line of sight velocity in km/s
    pm_RA : float # mean proper motion RA in mas / yr
    pm_DEC: float # mean proper motion DEC in mas / yr
    err_pm_RA : float # error mean proper motion RA in mas / yr
    err_pm_DEC : float # error mean proper motion DEC in mas / yr
    correlation: float # correlation coefficient (normalized non-diagonal element in the error covariance matrix)
    rh: float # angular scale radius (arcmin)
    N_stars: int # numbers of stars

        
@dataclass
class VasilievList:
    """
    Struct containing a list of VasilievData objects
    """
    data: list[VasilievData] = field(default_factory=list)
        

def get_GC_params(fname: str) -> VasilievList:
    """
    Reads data from file containing Vasiliev (2019) data. And returns a list with their characteristics
    in a dataclass.
    """
    data_type = np.dtype([("name", np.unicode_, 16), ("ra", float), ("dec", float), ("dist",float), ("hrv",float),
                         ("err_hrv", float), ("pmRA", float), ("pmDEC", float), ("err_pmRA", float), ("err_pmDEC", float),
                         ("corr", float), ("r_h",float), ("N_stars", int)])
    gc_names, gc_ra, gc_dec, dist, hrv, e_hrv, pmRA, pmDEC, e_pmRA, e_pmDEC, corr, gc_rh, n_stars = np.loadtxt(fname, 
                                                                                                               dtype=data_type, 
                                                                                                               comments='#',
                                                                                                               unpack=True)    
    data_vasiliev = VasilievList()
    
    for name_it, ra, dec, d, hr, ehr, pmra, pmdec, epmra, epmdec, c, rh_it, n in zip(gc_names, gc_ra, gc_dec, dist, hrv, e_hrv, pmRA, pmDEC, e_pmRA, e_pmDEC, corr, gc_rh, n_stars):
        data = VasilievData(name=name_it, RA=ra, DEC=dec, distance=d, losv=hr, err_losv=ehr, pm_RA=pmra, pm_DEC=pmdec,
                           err_pm_RA=epmra, err_pm_DEC=epmdec, correlation=c, rh=rh_it, N_stars=n)
        data_vasiliev.data += [data]
    
    return data_vasiliev

def get_selected_GC(obj_name: str, data_listed: VasilievList) -> (VasilievData, bool):
    """
    Returns a VasilievData type variable which name matches with that variable.name inside
    Vasiliev Data list.
    If the object (obj_name) is not found in data list (data_listed) then it will return an
    empty variable and it will raise an exception.
    """
    try:
        for item in data_listed.data:
            if item.name.upper() == obj_name.upper():
                return item, True
        raise ClusterNotFound
        
    except ClusterNotFound:
        print(f"{obj_name!r} object not found in Globular Cluster list!")
        print("You will have to add coordinates manually in the next cell.")
        print()
        return VasilievData(name="", RA=0., DEC=0., distance=0., losv=0., err_losv=0.,
                            pm_RA=0., pm_DEC=0., err_pm_RA=0, err_pm_DEC=0., correlation=0,
                            rh=0., N_stars=0), False
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


def isInJSONParametersFile(filename_json: str, object_name: str) -> (ParametersGC, bool):
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
