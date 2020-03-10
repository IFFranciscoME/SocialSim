
# .. .................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos         .. #
# .. Archivo: procesos.py - funciones de procesamiento general de datos                   .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                   .. #
# .. Licencia: Todos los derechos reservados                                              .. #
# .. Repositorio: https://github.com/                                                     .. #
# .. .................................................................................... .. #

import numpy as np
import random
import simulaciones as sim
import itertools


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
    personas_regresan : list : personas que regresan

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
    param_n_meses = 18
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
def f_ventas_persona(param_m_bin_comb, param_v_prob_comb, param_v_prob_cant, param_v_precios, param_v_costos):
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
    k_ingreso_total = sum(v_venta_persona)
    k_utilidad_total = sum(v_venta_persona) - sum(v_costo_persona)

    return k_ingreso_total, k_utilidad_total, v_venta_persona, v_costo_persona


# Funcion que da las compras del periodo de todas las personas
def f_periodo_ventas(param_visita, m_bin_comb, v_prob_comb, v_prob_cant, param_v_precios, param_v_costos):
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
    v_periodo = [f_ventas_persona(m_bin_comb, v_prob_comb, v_prob_cant, param_v_precios, param_v_costos) for i in range(param_visita)]
    return v_periodo


# Funcion de ventas totales por personas y periodo de tiempo
def f_ventas_total(param_n_periodos, n_canales, param_beta, param_segmento,
                           m_bin_comb, v_prob_comb, v_prob_cant, param_v_precios, param_v_costos):
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
                                       param_v_precios, param_v_costos) for i in range(param_n_periodos)]

    return m_ventas_totales_persona


