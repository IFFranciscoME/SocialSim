
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


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  FUNCION: Simular aleatorio - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion para simular aleatorios con diferente distribucion de probabilidad

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
                                                size=param_num) * (
                            param_rango[1] - param_rango[0])).round(param_redondeo)
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
        # llega a haber situaciones donde param_pars['param1'] < 0
        parchesote = abs(param_pars['param1'])
        return np.random.binomial(n=parchesote, p=param_pars['param2'],
                                  size=param_num).round(param_redondeo)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Discretizar funcion  - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion que calcula la probabilidad siguiendo una distribucion dada discretizandola

def f_prob_discr(param_dist, param_pars_dist, param_num):
    """
    Parameters
    ----------
    param_dist : str :  nombre de la distribucion
    param_pars_dist : list : parametros de la distribucion
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
    v_prob_acum = dist.cdf(x, *param_pars_dist[:-2], loc=param_pars_dist[-2],
                           scale=param_pars_dist[-1])
    v_prob = np.diff(v_prob_acum)
    if sum(v_prob) == 1:
        return v_prob_acum
    else:
        # print('-')
        return v_prob_acum


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Matriz combinaciones - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion para generar una matriz de combinaciones

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


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Vector de probabilidad - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion de vector de probabilidad

def f_prob_cantidad(param_n_max_product, param_dist, param_par_dist_cant):
    """
    Parameters
    ----------
    param_n_max_product : int :  numero maximo de productos que se venderian
    param_dist: list : parametros de distribucion beta [a, b, loc, scale]
    param_par_dist_cant :

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


# - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Acompanantes por periodo - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion para generar una matriz de combinaciones

def f_acompanantes_periodo(param_v_sector_acom_prob, param_seg, param_ajuste):
    """
    Parameters
    ----------
    param_v_sector_acom_prob : list : vector con las probabilidades
    param_seg: int : numero de asistentes por sector
    param_ajuste : int : numero de ajuste

    Returns
    -------
    v_cant_acom : list : cantidad de acompanantes por sector

    Debugging
    -------
    param_vectorprob = [.2, .8, 1]
    param_seg = [342]
    param_ajuste = 2

    """
    v_cant_acom = []
    for i in range(param_seg):
        r = np.random.random()
        v_cant_acom.append(len(np.where(param_v_sector_acom_prob < r)[0]) + param_ajuste)

    return sum(v_cant_acom)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -  FUNCION: Probabilidad Binomial - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion para generar aleatorios con dist probabilidad binominal

def f_prob_binomial(param_porcent, param_seg, param_acompanante):
    """
    Parameters
    ----------
    param_porcent : float : porcentaje
    param_seg : int : numero de asistentes por sector A
    param_acompanante : int: numero de acompanantes por sector A

    Returns
    -------
    personas : lis : cantidad de personas de acuerdo con la probabilidad binomial

    Debugging
    -------
    param_porcentaje = 0.5
    param_seg = 365
    param_acompanante= 546

    """
    # print('utilizado f_prob_binomial')
    personas = f_simular("binomial",
                         {'param1': param_seg + param_acompanante,
                          'param2': param_porcent}, 1, 2, 0)

    return personas


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Familias ven mural - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion para generar numero de familias que ven el mural

def f_familias_mural(personas_asamblea, n_familias_total, porcentaje_van,
                     porcentaje_ven_mural):
    """
    Parameters
    ----------
    personas_asamblea : DataFrame : personas que van a la asamblea
    n_familias_total : int : numero de familias total de la comunidad
    porcentaje_van : float : porcentaje de personas que van a la casa comunal
    porcentaje_ven_mural : float : porcentaje de los que ven el mural

    Returns
    -------
    familias_ven_mural : lis : cantidad de personas que usan el bano

    Debugging
    -------
    personas_asambleas = pd.DataFrame([[5, 7, 9],[6, 6, 8])
    n_familias_total = 30
    porcentaje_van = 0.1
    porcentaje_ven_mural = 0.9

    """
    familias_no_asamblea = n_familias_total - personas_asamblea

    familias_van_casa_com = [list(
        itertools.chain(*[f_prob_binomial(porcentaje_van, int(familias_no_asamblea.iloc[i, j]),
                                          0) for i in range(len(personas_asamblea))])) for j in
                             range(len(personas_asamblea.columns))]

    familias_ven_mural = [list(
        itertools.chain(*[f_prob_binomial(porcentaje_ven_mural, familias_van_casa_com[j][i],
                                          0) for i in range(len(personas_asamblea))])) for j in
                          range(len(personas_asamblea.columns))]

    return familias_ven_mural
