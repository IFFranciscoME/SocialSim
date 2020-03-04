
# .. .................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos         .. #
# .. Archivo: simulaciones.py - procesos de estadistica y simulacion                      .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                   .. #
# .. Licencia: Todos los derechos reservados                                              .. #
# .. Repositorio: https://github.com/                                                     .. #
# .. .................................................................................... .. #

import numpy as np


def f_simular(param_dist, param_pars, param_num, param_redondeo):
    """
    Parameters
    ----------
    param_dist : str :  nombre de la distribucion
    param_pars : list : parametros de la distribucion
    param_num : int : cantidad de muestras a simular
    param_redondeo : decimal para redondeo del resultado final

    Returns
    -------
    np.random

    Debugging
    -------
    param_dist = 'beta'
    param_pars = {'param1': 1.5, 'param2': 4}
    param_num = 10
    param_redondeo = 2

    """
    if param_dist == "beta":          # -- Beta
        return np.random.beta(a=param_pars['param1'], b=param_pars['param2'],
                                           size=param_num).round(param_redondeo)
    elif param_dist == "normal":      # -- Normal
        return np.random.normal(loc=param_pars['param1'], scale=param_pars['param2'],
                                             size=param_num).round(param_redondeo)
    elif param_dist == "triangular":  # -- Triangular
        return np.random.triangular(left=param_pars['param1'], mode=param_pars['param2'],
                                    right=param_pars['param3'],
                                    size=param_num).round(param_redondeo)
    elif param_dist == "uniforme":    # -- Uniforme
        return np.random.uniform(low=param_pars['param1'], high=param_pars['param2'],
                                 size=param_num)
