
# .. .................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos         .. #
# .. Archivo: procesos.py - funciones de procesamiento general de datos                   .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                   .. #
# .. Licencia: Todos los derechos reservados                                              .. #
# .. Repositorio: https://github.com/                                                     .. #
# .. .................................................................................... .. #

import numpy as np
import matplotlib.pyplot as plt
import random
import simulaciones as sim
import datos as dat
import itertools


# Funcion que da el numero de visitas y el numero de personas que compraron al mes
def f_visitas_mes(param_beta, param_segmento, param_publicidad, param_cpm, param_ni_t_visitan):
    """
    Parameters
    ----------
    param_beta : list : matriz de 4x4 de los parametros de distribuciones beta [a, b, lim_inf, lim_sup]
    param_segmento : int :  cantidad de personas del segmento
    param_publicidad : int : cantidad de dinero destinado a la publicidad
    param_cpm : int : cantidad del costo por publicidad
    ni_R_visitant: int: cantidad de personas que visitaron en t-1

    Returns
    -------
    ni_R_visitan: int : Numero de personas que visitan
    ni_R_compran: int : Numero de personas que compran

    Debugging
    -------
    param_beta = [[1.5, 4, 0, 0.1], [4, 2, 0, 0.2], [1, 2, 0, 0.05], [4.5, 1.5, 0.2, 0.55]]
    param_segmento = 10800
    param_publicidad = 500
    param_cpm = 10
    param_ni_t_visitan = 0
    """

    # Mercado accesible (población)
    K_seg = param_segmento
    # Presupuesto para publicidad
    k_pre_pub = param_publicidad
    # Precio por publicidad en Facebook
    k_cpm = param_cpm
    # Cantidad de personas alcanzadas
    ni_mapc = k_pre_pub / (k_cpm * 1 / 10000)

    # Simulaciones
    k = [(sim.f_simular("beta", {'param1': param_beta[i][0], 'param2': param_beta[i][1]},
                    1, 2, [param_beta[i][2], param_beta[i][3]])) for i in range(len(param_beta))]

    # Simulacion de cuantos clicks
    k_f1_clicks = float(k[0])
    # Personas que dieron click
    ni_A_clicks = ni_mapc * k_f1_clicks

    # Simulacion de cuantos visitan el lugar
    k_f2_visitan = float(k[1])
    # Personas que visitan
    ni_A_visitan = ni_A_clicks * k_f2_visitan

    # Simulacion de cuantos regresan
    k_f3_regresan = float(k[2])
    # Personas que regresan
    ni_R_regresan = param_ni_t_visitan * k_f3_regresan
    ni_R_visitan = ni_R_regresan + ni_A_visitan

    # Simulacion personas que compran
    k_f4_compran = float(k[3])
    # Personas que terminan comprando
    ni_R_compran = ni_R_visitan * k_f4_compran

    return int(ni_A_visitan), int(ni_R_compran), int(ni_R_regresan)


# Funcion que, a partir de la funcion de personas que visitan por mes, te da una serie de tiempo de n periodos
def f_serie_tiempo_visitan(param_n_periodos, param_beta, param_segmento, param_publicidad, param_cpm):
    """
    Parameters
    ----------
    param_n_periodos : int : numero de meses a simular
    param_beta : list : lista de listas de los parametros para la funcion de ventas por mes
    param_segmento : int : numero de personas por segmentos
    param_publicidad : int : cantidad presupuestado para la publicidad
    param_cpm : int : datos del precio por publicidad
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
    datos_visita = np.zeros((3, param_n_periodos + 1))

    for i in range(param_n_periodos):
        ni_A_visitan, ni_R_compra, regresan = f_visitas_mes(param_beta, param_segmento,
                                                            param_publicidad, param_cpm, datos_visita[0][i])
        datos_visita[0][i+1] = ni_A_visitan
        datos_visita[1][i+1] = ni_R_compra
        datos_visita[2][i+1] = regresan

    return datos_visita


# Funcion que regresa la compra individual
def f_ventas_persona(param_m_bin_comb, param_v_prob_comb, param_v_prob_cant, param_v_precios, param_i_max_prod):
    """
    Parameters
    ----------
    param_m_bin_comb : list : matriz de posibles combinaciones binarias
    param_v_prob_comb: list : probabilidades de cada combinacion
    param_v_prob_cant: list : probabilidades de cada cantidad posible comprada
    param_v_precios:  list : lista de precios por producto
    param_i_max_prod:

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

    # Vector de cantidad de productos [1, 2, 3]
    v_cant_prod = []

    def v_cantidad(v_cant_prod, param_v_prob_cant):
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
        for i in range(len(param_v_precios)):
            r = random.random()
            v_cant_prod.append(len(np.where(param_v_prob_cant < r)[0])+1)

        return v_cant_prod

    cantidad = v_cantidad(v_cant_prod, param_v_prob_cant)

    # Venta totales
    v_venta_persona = cantidad*np.array(combinacion)*np.array(param_v_precios)
    k_ingreso_total = sum(v_venta_persona)

    #print(cantidad, combinacion, param_v_precios)
    return k_ingreso_total


def f_periodo_ventas(param_visita, m_bin_comb, v_prob_comb, v_prob_cant, v_precios, k_mn):
    """
    Parameters
    ----------
    param_visita : int : personas que asisten y compran en el periodo
    m_bin_comb : list : matriz de posibles combinaciones binarias
    v_prob_comb : list : vector probabilidades de cada combinacion posible de combinaciones de productos
    v_prob_cant : list : vector probabilidades de cada cantidad posible comprada
    v_precios : list : vector de precios por producto
    k_mn : int : numero maximo de productos
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
    v_periodo = [f_ventas_persona(m_bin_comb, v_prob_comb, v_prob_cant, v_precios, k_mn) for i in range(param_visita)]
    return v_periodo


# Funcion de ventas totales por personas y periodo de tiempo
def f_ventas_total(n_periodo, param_beta, param_segmento, param_publicidad, param_cpm,
                           m_bin_comb, v_prob_comb, v_prob_cant, v_precios, k_mn):
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
    m_visitan = f_serie_tiempo_visitan(n_periodo, param_beta, param_segmento, param_publicidad, param_cpm)

    # Matriz de ventas por persona y periodo
    m_ventas_totales_persona = [f_periodo_ventas(int(m_visitan[1][i]), m_bin_comb, v_prob_comb, v_prob_cant,
                                       v_precios, k_mn) for i in range(1, n_periodo)]
    # Sumar todas las ventas del periodo
    ventas_totales = [sum(m_ventas_totales_persona[i]) for i in range(len(m_ventas_totales_persona))]
    return ventas_totales


# param_visita, m_bin_comb, v_prob_comb, v_prob_cant, v_precios, k_mn):

# ---------
# DATOS
# ---------
# Numero de productos que se venderian
k_n = dat.k_plantas
# Numero maximo de productos que se venderian
k_mn = dat.k_max_prod_cte
# Precios de los productos
v_precios = dat.v_plantas_p
# Parametros para los 16 posibles combinaciones (distribucion beta)
param_comb = [1.5, 2, 0, 1]
# Parametros para la maxima cantidad de productos (distribucion exponencial)
param_cant = [ 0.31, 0.01]
# Numero de simulaciones por periodos
n_mes = 18

# Matriz de parametros para simulaciones con distribucion beta [a, b, limite inferior, limite superior]
param_beta = [[1.5, 4, 0, 0.1],      # Parametros beta: simulacion de clicks
              [4, 2, 0, 0.2],        # Parametros beta: simulacion de visitas
              [1, 2, 0, 0.05],       # Parametros beta: simulacion de regresos
              [4.5, 1.5, 0.2, 0.55]] # Parametros beta: simulacion de compras

# Combinaciones
m_bin_comb, v_prob_comb = sim.f_prob_combinaciones(k_n, param_comb)

# Cantidad
v_prob_cant = sim.f_prob_cantidad(k_mn, param_cant)

# Numero de simulaciones
n_sim = 50
# Funcion de ventas totales para segmento A
ventas_totales_p = [f_ventas_total(n_mes, param_beta, dat.segmento_ctes_A, dat.publicidad_A, dat.cpm_ctes_A,
                                  m_bin_comb, v_prob_comb, v_prob_cant, v_precios, k_mn) for i in range(n_sim)]

t = np.arange(len(ventas_totales_p[0]))

# Graficas
fig = plt.figure()
ax = plt.axes()
[ax.plot(t, ventas_totales_p[i]) for i in range(n_sim)]
plt.show()