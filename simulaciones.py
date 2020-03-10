# .. .................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos         .. #
# .. Archivo: simulaciones.py - procesos de estadistica y simulacion                      .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                   .. #
# .. Licencia: Todos los derechos reservados                                              .. #
# .. Repositorio: https://github.com/                                                     .. #
# .. .................................................................................... .. #

import numpy as np
import scipy.stats as st
import itertools


def f_simular(param_dist, param_pars, param_num, param_redondeo, param_rango):
    """
    Parameters
    ----------
    param_dist : str :  nombre de la distribucion
    param_pars : list : parametros de la distribucion
    param_num : int : cantidad de muestras a simular
    param_redondeo : int : decimal para redondeo del resultado final
    param_rango : list : lista con dos elementos del rango, el inicial y el final.
    Returns
    -------
    np.random
    Debugging
    -------
    param_dist = 'beta'
    param_pars = {'param1': 1.5, 'param2': 4}
    param_num = 1
    param_redondeo = 2
    param_rango = [0, 0.10]
    """

    if param_dist == "beta":  # -- Beta
        return (param_rango[0] + np.random.beta(a=param_pars['param1'], b=param_pars['param2'],
                                               size=param_num) * (param_rango[1] - param_rango[0])).round(param_redondeo)
    elif param_dist == "normal":  # -- Normal
        return np.random.normal(loc=param_pars['param1'], scale=param_pars['param2'],
                                size=param_num).round(param_redondeo)
    elif param_dist == "triangular":  # -- Triangular
        return np.random.triangular(left=param_pars['param1'], mode=param_pars['param2'],
                                    right=param_pars['param3'],
                                    size=param_num).round(param_redondeo)
    elif param_dist == "uniforme":  # -- Uniforme
        return np.random.uniform(low=param_pars['param1'], high=param_pars['param2'],
                                 size=param_num)
    elif param_dist == "binomial":  # -- Binomial
        return np.random.binomial(n=param_pars['param1'], p=param_pars['param2'],
                                  size=param_num).round(param_redondeo)


# Funcion que calcula la probabilidad siguiendo una distribucion dada discretisandola
def f_prob_discr(param_dist, param_pars_dist, param_num):
    """
    Parameters
    ----------
    param_dist : str :  nombre de la distribucion
    param_pars : list : parametros de la distribucion
    param_num : int : cantidad de probabilidades requeridas

    Returns
    -------
    v_prob_acum : np.ndarray : probabilidades que siguen tal distribución

    Debugging
    -------
    param_dist = 'beta'
    param_pars = [1.5, 4]
    param_num = 16
    """
    dist = getattr(st, param_dist)
    x = np.linspace(0, 1, param_num + 1)
    v_prob_acum = dist.cdf(x, *param_pars_dist[:-2], loc=param_pars_dist[-2], scale=param_pars_dist[-1])
    v_prob = np.diff(v_prob_acum)
    if sum(v_prob) == 1:
        return v_prob_acum
    else:
        #print('-')
        return v_prob_acum


# Matriz de combinaciones
def f_prob_combinaciones(param_n_product, param_par_dist_comb):
    """
    Parameters
    ----------
    param_n_product : int :  numero de productos que se venderian
    param_par_dist_comb: list : parametros de distribucion beta [a, b, loc, scale]

    Returns
    -------
    m_bin_comb : list : matriz de posibles combinaciones binarias
    v_prob_comb : np.ndarray : probabilidades de cada combinacion

    Debugging
    -------
    param_n_product = 4
    param_par_dist_comb = [1.5, 2, 0, 1]
    """

    # Se propone distribucion beta para las combinaciones
    dist_comb = 'beta'

    # Numero de productos
    k_n = param_n_product

    # Crear matriz binaria de posibles compras
    m_bin_comb = list(map(list, itertools.product([0, 1], repeat=k_n)))

    # Numero de combinaciones posibles 2^n
    k_l = len(m_bin_comb)

    # Vector de probabilidades acumuladas | no tomar el primero, es cero
    v_prob_comb = f_prob_discr(dist_comb, param_par_dist_comb, k_l)[1:]

    return m_bin_comb, v_prob_comb


# Funcion de vector de probabilidad
def f_prob_cantidad(param_n_max_product, param_dist, param_par_dist_cant):
    """
    Parameters
    ----------
    param_n_max_product : int :  numero maximo de productos que se venderian
    param_par_dist_ventas: list : parametros de distribucion beta [a, b, loc, scale]

    Returns
    -------
    v_prob_comb : np.ndarray : probabilidades que siguen tal distribución

    Debugging
    -------
    param_n_max_product = 3
    param_par_dist_cant = [.8, 0.3, 0.5]
    """

    # Se propone distribucion beta para las combinaciones
    dist_cant = param_dist

    # Numero maximo de productos que se comprarian
    k_nm_p = param_n_max_product

    # Vector de probabilidades acumuladas | no tomar el primero, es cero
    v_prob_cant = f_prob_discr(dist_cant, param_par_dist_cant, k_nm_p)[1:]

    return v_prob_cant


def f_acompañantes_periodo(param_v_sector_acom_prob, param_seg, param_ajuste):
    """
    Parameters
    ----------
    param_vectorprob : list : vector con las probabilidades
    param_seg: int : numero de asistentes por sector
    Returns
    -------
    v_cant_acom : list : cantidad de acompañantes por sector

    Debugging
    -------
    param_vectorprob = [.2, .8, 1]
    param_seg= [342]

    """
    v_cant_acom = []
    for i in range(param_seg):
        r = np.random.random()
        v_cant_acom.append(len(np.where(param_v_sector_acom_prob < r)[0]) + param_ajuste)

    return sum(v_cant_acom)