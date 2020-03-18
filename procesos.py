
# .. .................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos         .. #
# .. Archivo: procesos.py - funciones de procesamiento general de datos                   .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                   .. #
# .. Licencia: Todos los derechos reservados                                              .. #
# .. Repositorio: https://github.com/                                                     .. #
# .. .................................................................................... .. #

import numpy as np
import pandas as pd
import random
import simulaciones as sim
import itertools

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INGRESOS
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion que da el numero de visitas y el numero de personas que compraron al mes
def f_visitas_segmento(n_canales, param_beta, param_segmento, param_t_visitan):
    """
    Parameters
    ----------
    n_canales : int : numero de canales por los cuales se quiere llegar al segmento
    param_beta : list : matriz de 4x4 de los parametros de distribuciones beta [a, b, lim_inf, lim_sup]
    param_segmento : list :  cantidad de personas del segmento alcanzables por cada canal
    param_t_visitan : list : personas que visitaron en t-1

    Returns
    -------
    personas_visitan_total: list : personas que visitan por canal
    personas_compran_total : int : personas totales que compran
    personas_regresan : list : personas que regresan por canal del periodo anterior

    Debugging
    -------
    n_canales = 2
    param_beta = [[[1.5, 4, 0, 0.1], [4, 2, 0, 0.2], [1, 2, 0, 0.05], [4.5, 1.5, 0.2, 0.55]], # Canal 1
                    [[4, 2, 0, 0.2], [1, 2, 0, 0.05], [4.5, 1.5, 0.2, 0.55]]]      # Canal 2
    param_segmento = [5000, 10800]
    param_t_visitan = [0, 0]
    """
    # Simulaciones de porcentajes segun cada canal
    simulaciones = [[(sim.f_simular("beta", {'param1': param_beta[j][i][0],
                                         'param2': param_beta[j][i][1]}, 1, 4,
                                [param_beta[j][i][2], param_beta[j][i][3]]))
                     for i in range(len(param_beta[j]))] for j in range(len(param_beta))]

    # Vector de simulaciones para cada canal
    v_porcentajes = [list(itertools.chain(*simulaciones[i])) for i in range(len(simulaciones))]

    '''Multiplicacion de todos los porcentajes simulados, debido a que:
        Antes del penultimo ES porcentante de visitas.
        El penultimo es el porcentaje de una visita anterior que regresa
        El ultimo es el porcentaje que compra
    '''
    # Porcentaje de numero de personas que visitan por canal
    porcentaje_visita = [np.prod(v_porcentajes[i][:-2]) for i in range(n_canales)]
    # Porcentaje de numero de personas que regresan por canal
    porcentaje_regresa = [v_porcentajes[i][-2] for i in range(n_canales)]
    # Porcentaje de numero de personas que compran
    porcentaje_compra = [v_porcentajes[i][-1] for i in range(n_canales)]

    # Personas que visitan por canal
    personas_visitan = [int(porcentaje_visita[i] * param_segmento[i]) for i in range(n_canales)]
    # Personas que regresan (porcentaje que regresan por personas que visitaron un periodo antes)
    personas_regresan = [int(porcentaje_regresa[i] * param_t_visitan[i]) for i in range(n_canales)]
    # Personas que visitan este periodo mas personas que regresan
    personas_visitan_total = [int(personas_visitan[i] + personas_regresan[i]) for i in range(n_canales)]
    # Personas que compran por canal
    personas_compran = [int(personas_visitan_total[i] * porcentaje_compra[i]) for i in range(n_canales)]
    # Personas totales que compran
    personas_compran_total = np.sum(personas_compran)
    
    return personas_visitan_total, personas_compran_total, personas_regresan


# Funcion que, a partir de la funcion de personas que visitan por mes, te da una serie de tiempo de n periodos
def f_serie_tiempo_visitan(param_n_periodos, n_canales, param_beta, param_segmento):
    """
    Parameters
    ----------
    param_n_periodos : int : numero de meses a simular
    param_beta : list : lista de listas de los parametros para la funcion de ventas por mes
    param_segmento : int : numero de personas por segmentos

    Returns
    -------
    datos_visita : np.array : matriz de numero de personas que [visitan, compran, regresan]

    Debugging
    -------
    param_n_periodos = 18
    param_beta = [[1.5, 4, 0, 0.1], [4, 2, 0, 0.2], [1, 2, 0, 0.05], [4.5, 1.5, 0.2, 0.55]]
    param_segmento = 10800
    param_publicidad = 500
    param_cpm = 10

    """
    datos_visita = np.zeros((3, param_n_periodos))
    v, c, r = [list(np.zeros(n_canales))], [], []
    for i in range(param_n_periodos):
        vi, ci, ri = f_visitas_segmento(n_canales, param_beta, param_segmento, v[i])
        v.append(vi)
        c.append(ci)
        r.append(ri)

    # Visitan
    datos_visita[0] = [np.sum(v[i]) for i in range(1, len(v))]
    datos_visita[1] = c
    datos_visita[2] = [np.sum(r[i]) for i in range(len(r))]

    return datos_visita


# Funcion que regresa la compra individual
def f_ventas_persona(param_m_bin_comb, param_v_prob_comb, param_v_prob_cant, param_v_precios, param_v_costos, param_v_horas):
    """
    Parameters
    ----------
    param_m_bin_comb : list : matriz de posibles combinaciones binarias
    param_v_prob_comb: list : probabilidades de cada combinacion
    param_v_prob_cant: list : probabilidades de cada cantidad posible comprada
    param_v_precios:  list : lista de precios por producto

    Returns
    -------
    k_ingreso_total : int : venta de una persona

    Debugging
    -------
    param_m_bin_comb = [[0, 0],[0, 1],[1, 0],[1, 1]]
    param_v_prob_comb = [0.1, 0.45, 0.85, 1]
    param_v_prob_cant = [0.1, 0.8, 1]
    param_v_precios = [10, 20]

    """

    # Numero aleatorio para ver cual combinacion de productos se compraria
    r_comb = random.random()

    # Indice de la combinacion segun el aleatorio anterior
    i_comb = len(np.where(param_v_prob_comb < r_comb)[0] - 1)

    # Combinacion de productos
    combinacion = param_m_bin_comb[i_comb]

    def v_cantidad(combinacion, param_v_prob_cant):
        """
        Parameters
        ----------
        v_cant_prod : list :
        param_v_prob_cant: list : probabilidades de cada cantidad posible comprada

        Returns
        -------
        v_cant_prod : list : productos vendido de una persona

        Debugging
        -------
        v_cant_prod = []
        param_v_prob_cant = [0.1, 0.8, 1]

        """

        v_cant_prod = np.zeros(len(combinacion))
        for i in range(len(combinacion)):
            if combinacion[i] != 0:
                r = random.random()
                v_cant_prod[i] = len(np.where(param_v_prob_cant < r)[0]) + 1

        return v_cant_prod

    cantidad = v_cantidad(combinacion, param_v_prob_cant)

    # Venta totales
    v_venta_persona = np.array(cantidad) * np.array(combinacion) * np.array(param_v_precios)
    v_costo_persona = np.array(cantidad) * np.array(combinacion) * np.array(param_v_costos)
    v_horas_persona = np.array(cantidad) * np.array(combinacion) * np.array(param_v_horas)

    k_horas_total = sum(v_horas_persona)
    k_ingreso_total = sum(v_venta_persona)
    k_costo_total = sum(v_costo_persona)
    k_utilidad_total = sum(v_venta_persona) - sum(v_costo_persona)

    return k_ingreso_total, k_costo_total, k_utilidad_total, v_venta_persona, v_costo_persona, k_horas_total


# Funcion que da las compras del periodo de todas las personas
def f_periodo_ventas(param_visita, m_bin_comb, v_prob_comb, v_prob_cant, param_v_precios, param_v_costos, param_v_horas):
    """
    Parameters
    ----------
    param_visita : int : personas que asisten y compran en el periodo
    m_bin_comb : list : matriz de posibles combinaciones binarias
    v_prob_comb : list : vector probabilidades de cada combinacion posible de combinaciones de productos
    v_prob_cant : list : vector probabilidades de cada cantidad posible comprada
    v_precios : list : vector de precios por producto
    Returns
    -------
    v_mes : list : venta del periodo (mes) de todas las personas

    Debugging
    -------
    param_visita = 217
    param_m_bin_comb = [[0, 0],[0, 1],[1, 0],[1, 1]]
    param_v_prob_comb = [0.1, 0.45, 0.85, 1]
    param_v_prob_cant = [0.1, 0.8, 1]
    param_v_precios = [10, 20]

    """
    # Se simulan las ventas por personas, dependiendo de el numero de personas que visitaron y compraron (mes)
    v_periodo = [f_ventas_persona(m_bin_comb, v_prob_comb, v_prob_cant, param_v_precios,
                                  param_v_costos, param_v_horas) for i in range(param_visita)]
    return v_periodo


# Funcion de ventas totales por personas y periodo de tiempo
def f_ventas_total(param_n_periodos, n_canales, param_beta, param_segmento,
                           m_bin_comb, v_prob_comb, v_prob_cant, param_v_precios, param_v_costos, param_v_horas):
    """
    Parameters
    ----------
    param_n_periodo : int : numero de meses a simular
    param_beta : list : lista de listas de los parametros para la funcion de ventas por mes
    param_segmento : int : numero de personas por segmentos
    param_publicidad : int : cantidad presupuestado para la publicidad
    param_cpm : int : datos del precio por publicidad

    param_visita : int : personas que asisten y compran en el periodo
    m_bin_comb : list : matriz de posibles combinaciones binarias
    v_prob_comb : list : vector probabilidades de cada combinacion posible de combinaciones de productos
    v_prob_cant : list : vector probabilidades de cada cantidad posible comprada
    v_precios : list : vector de precios por producto
    k_mn : int : numero maximo de productos

    """
    # Matriz que regresa las personas que van [vistan, compran, regresan] durante n_periodos
    m_visitan = f_serie_tiempo_visitan(param_n_periodos, n_canales, param_beta, param_segmento)

    # Matriz de ventas por persona y periodo
    m_ventas_totales_persona = [f_periodo_ventas(int(m_visitan[1][i]), m_bin_comb, v_prob_comb, v_prob_cant,
                                       param_v_precios, param_v_costos, param_v_horas) for i in range(param_n_periodos)]

    return m_visitan, m_ventas_totales_persona


# Funcion para extraer de f_ventas_total un dato especifico
def f_extract(param_obj, param_k_num, param_b_suma):
    """
    Parameters
    ----------
    param_obj : list : return de funcion f_ventas_total
    param_k_num : int : numero [0, 4] donde 0 es ingreso, 1 es utilidad, 2 ventas por producto, 3 costo por producto, 4 horas
    param_b_suma : bool : La suma de todo el periodo

    Returns
    -------
    dato : lis : serie de tiempo del dato requerido

    Debugging
    -------
    param_obj = f_ventas_total(parameters)
    param_k_num = 1
    param_b_suma = True

    """
    if param_b_suma:
        dato = [np.sum([param_obj[1][j][i][param_k_num] for i in range(len(param_obj[1][j]))]) for j in range(len(param_obj[1]))]
    else:
        dato = [[param_obj[1][j][i][param_k_num] for i in range(len(param_obj[1][j]))] for j in range(len(param_obj[1]))]
    return dato


def f_n_simulaciones_proceso(n_sim, list_parameters_ventas, list_parameters_costos):
    """
    Parameters
    ----------
    n_sim : int : numero de simulaciones
    list_parameters_ventas : list : lista de paarmetros

    Returns
    -------
    dato : lis : serie de tiempo del dato requerido

    Debugging
    -------
    list_parameters_ventas

    """
    
    obj = [f_ventas_total(list_parameters_ventas[0], list_parameters_ventas[1], list_parameters_ventas[2],
                             list_parameters_ventas[3], list_parameters_ventas[4], list_parameters_ventas[5], 
                             list_parameters_ventas[6], list_parameters_ventas[7], list_parameters_ventas[8], 
                             list_parameters_ventas[9]) for i in range(n_sim)]
    
    # visitantes, compradores, regresan, ingresos, costos, utilidad, horas
    datos1 = [[obj[i][0][0], obj[i][0][1], obj[i][0][2], f_extract(obj[i], 0, True), f_extract(obj[i], 1, True),
               f_extract(obj[i], 2, True), f_extract(obj[i], 4, True)] for i in range(n_sim)]
    
    # acompañantes, costos de los baños, personas taller, costo taller
    datos2 = [f_ts_costos(list_parameters_costos[0], datos1[i][0], list_parameters_costos[1],
                                         list_parameters_costos[2], list_parameters_costos[3],
                                         list_parameters_costos[4], list_parameters_costos[5]) for i in range(n_sim)]
    return datos1, datos2

def f_DataFrame_1(n_sim, list_parameters_v, list_parameters_c):
    """
    Parameters
    ----------
    n_sim : int : numero de simulaciones
    list_parameters : list : lista de paarmetros

    Returns
    -------
    dato : lis : serie de tiempo del dato requerido

    Debugging
    -------
    list_parameters

    """
    datos1, datos2 = f_n_simulaciones_proceso(n_sim, list_parameters_v, list_parameters_c)
    
    nombres = ['Visitantes', 'Acompañantes', 'Compradores', 'Regresan', 'Personas taller', 'Costo de taller', 'Costo de baños',
               'Ingreso', 'Costo', 'Utilidad', 'Horas']
    #lista = [[visitas[i], compradores[i], regresan[i], ingresos[i], costos[i], utilidad[i], horas[i]] for i in range(n_sim)]
    lista = [[datos1[i][0], datos2[i][0], datos1[i][1], datos1[i][2], datos2[i][2], datos2[i][3], datos2[i][1],
                datos1[i][3], datos1[i][4], datos1[i][5], datos1[i][6]] for i in range(n_sim)]
    
    DF_results = [pd.DataFrame(lista[i], index = nombres).T for i in range(n_sim)]
    
    return DF_results

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# COSTOS
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def f_ts_costos(param_v_sector_prob_acomp, param_v_visitantes, param_k_min_acomp,
                param_porcentaje_baño, param_costo_baño,
                param_porcentaje_taller, param_costo_taller):
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
    v_acompañantes = [sim.f_acompañantes_periodo(param_v_sector_prob_acomp,
                                                 int(param_v_visitantes[i]),
                                                 param_k_min_acomp) for i in range(len(param_v_visitantes))]

    # Baños
    personas_baños = [f_prob_binomial(param_porcentaje_baño, int(param_v_visitantes[i]),
                                      v_acompañantes[i]) for i in range(len(param_v_visitantes))]
    costo_baños = param_costo_baño * np.array(personas_baños)

    # Talleres
    personas_taller = [f_prob_binomial(param_porcentaje_taller, int(param_v_visitantes[i]),
                                       v_acompañantes[i]) for i in range(len(param_v_visitantes))]
    insumos_taller = param_costo_taller * np.array(personas_taller)

    return v_acompañantes, list(itertools.chain(*costo_baños)), list(itertools.chain(*personas_taller)), list(itertools.chain(*insumos_taller))


def f_prob_binomial(param_porcent, param_seg, param_acompañante):
    """
    Parameters
    ----------
    param_porcent : float : porcentaje
    param_seg : int : numero de asistentes por sector A
    param_acompañante : int: numero de acompañantes por sector A

    Returns
    -------
    vis_baños : lis : cantidad de personas que usan el baño

    Debugging
    -------
    param_porcentaje = 0.5
    param_seg = 365
    param_acompañante= 546

    """

    personas = sim.f_simular("binomial", {'param1': param_seg + param_acompañante, 'param2': param_porcent}, 1, 2, 0)

    return personas


