
# .. ................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos        .. #
# .. Archivo: procesos.py - funciones de procesamiento general de datos                  .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                  .. #
# .. Licencia: Todos los derechos reservados                                             .. #
# .. Repositorio: https://github.com/                                                    .. #
# .. ................................................................................... .. #

import numpy as np
import pandas as pd
import random
import simulaciones as sim
import itertools


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# INGRESOS
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Visitas en el tiempo - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - de personas que visitan por mes, te da una serie de tiempo de n periodos
    
def f_serie_tiempo_visitan(param_n_periodos, n_canales, param_beta, param_segmento, param_tendencia):
    """
    Parameters
    ----------
    param_n_periodos : int : numero de meses a simular
    n_canales : int : numero de canales
    param_beta : list : lista de listas de los parametros para la funcion de ventas por mes
    param_segmento : int : numero de personas por segmentos
    Returns
    -------
    datos_visita : np.array : matriz de numero de personas que [visitan, compran, regresan]
    datos_visita_canal : list : visitas, compran y regresan por cada canal
    Debugging
    -------
    param_n_periodos = 18
    n_canales = 1
    param_beta = [[[1.5, 4, 0, 0.1], [4, 2, 0, 0.2], [1, 2, 0, 0.05], [4.5, 1.5, 0.2, 0.55]]]
    param_segmento = [10800]
    """
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Visitas Segmento - #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # - - Funcion que da el numero de visitas y el numero de personas que compraron al mes

    def f_visitas_segmento(n_canales, param_beta, param_segmento, param_t_visitan, x_tendencia):
        """
        Parameters
        ----------
        n_canales : int : numero de canales por los cuales se quiere llegar al segmento
        param_beta : list : matriz de 4x4 de los parametros de distribuciones beta [a, b, lim_inf,
        lim_sup]
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
        param_beta = [[[1.5, 4, 0, 0.1], [4, 2, 0, 0.2],
                       [1, 2, 0, 0.05], [4.5, 1.5, 0.2, 0.55]], # Canal 1
                       [[4, 2, 0, 0.2], [1, 2, 0, 0.05],
                        [4.5, 1.5, 0.2, 0.55]]]                 # Canal 2
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
    
        ''' Multiplicacion de todos los porcentajes simulados, debido a que:
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
        personas_visitan = [int(porcentaje_visita[i] * param_segmento[i]) for i in
                            range(n_canales)]
        # Personas que regresan (porcentaje que regresan por personas que visitaron antes)
        personas_regresan = [int(porcentaje_regresa[i] * param_t_visitan[i]) for i in
                             range(n_canales)]
        # Personas que visitan este periodo mas personas que regresan
        personas_visitan_total = [int(x_tendencia) + int(personas_visitan[i] + personas_regresan[i]) for i in
                                  range(n_canales)]
        # Personas que compran por canal
        personas_compran = [int(personas_visitan_total[i] * porcentaje_compra[i]) for i in
                            range(n_canales)]
        # Personas totales que compran
        personas_compran_total = np.sum(personas_compran)
    
        return personas_visitan_total, personas_compran_total, personas_regresan, personas_compran
    
    # - - - - - - - - - - - - - - -
    # Ahora hacerlo para n periodos
    
    datos_visita = np.zeros((3, param_n_periodos))
    # Tendencia
    x = np.arange(param_n_periodos)*param_tendencia
    
    # Donde se guarda los datos
    v, c, r, pc = [list(np.zeros(n_canales))], [], [], []
    for i in range(param_n_periodos):
        vi, ci, ri, pci = f_visitas_segmento(n_canales, param_beta, param_segmento, v[i], x[i])
        v.append(vi)
        c.append(ci)
        r.append(ri)
        pc.append(pci)

    # Visitan
    datos_visita[0] = [np.sum(v[i]) for i in range(1, len(v))]
    datos_visita[1] = c
    datos_visita[2] = [np.sum(r[i]) for i in range(len(r))]
    datos_visita_canal = [v, pc, r]
    return datos_visita, datos_visita_canal


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Ventas por persona - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion que regresa la compra individual

def f_ventas_persona(param_m_bin_comb, param_v_prob_comb, param_v_prob_cant, param_v_precios,
                     param_v_costos, param_v_horas):
    """
    Parameters
    ----------
    param_m_bin_comb : list : matriz de posibles combinaciones binarias
    param_v_prob_comb: list : probabilidades de cada combinacion
    param_v_prob_cant: list : probabilidades de cada cantidad posible comprada
    param_v_precios :  list : vector de precios por producto
    param_v_costos : list : vector de costos por producto
    param_v_horas : list : vector de horas por producto

    Returns
    -------
    k_ingreso_total : int : dinero del ingreso de las personas
    k_costo_total : int : dinero del costo de las ventas de persona
    k_utilidad_total : int : resta entre el ingreso y costo por producto
    v_venta_persona : list : vector de ingreso por producto
    v_costo_persona : list : vector de costo por producto
    k_horas_total : int : horas totales de los productos vendidos para esta persona
    k_cantidad_productos : list : cantidad de cada producto vendido

    Debugging
    -------
    param_m_bin_comb = [[0, 0],[0, 1],[1, 0],[1, 1]]
    param_v_prob_comb = [0.1, 0.45, 0.85, 1]
    param_v_prob_cant = [0.1, 0.8, 1]
    param_v_precios = [10, 20, 30]
    param_v_costos = [5, 10, 12]
    param_v_horas = [0.25, 0.5, 1]

    """

    # Numero aleatorio para ver cual combinacion de productos se compraria
    r_comb = random.random()

    # Indice de la combinacion segun el aleatorio anterior
    i_comb = len(np.where(param_v_prob_comb < r_comb)[0] - 1)

    # Combinacion de productos
    combinacion = param_m_bin_comb[i_comb]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Auxiliar para cantidad - #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # - - Funcion auxiliar para cantidad

    def v_cantidad(combinacion, param_v_prob_cant):
        """
        Parameters
        ----------
        combinacion :
        param_v_prob_cant: list : probabilidades de cada cantidad posible comprada
        Returns
        -------
        v_can_prod : list : vector de productos comprados
        Debugging
        -------
        v_cant_prod = [0, 1, 0]
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
    v_cantidad_persona = np.array(cantidad) * np.array(combinacion)
    v_venta_persona = np.array(cantidad) * np.array(combinacion) * np.array(param_v_precios)
    v_costo_persona = np.array(cantidad) * np.array(combinacion) * np.array(param_v_costos)
    v_horas_persona = np.array(cantidad) * np.array(combinacion) * np.array(param_v_horas)

    k_horas_total = sum(v_horas_persona)
    k_ingreso_total = sum(v_venta_persona)
    k_costo_total = sum(v_costo_persona)
    k_utilidad_total = sum(v_venta_persona) - sum(v_costo_persona)
    k_cantidad_productos = sum(v_cantidad_persona)

    return k_ingreso_total, k_costo_total, k_utilidad_total, v_venta_persona, v_costo_persona,\
           k_horas_total, k_cantidad_productos


# - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Compras todas las personas - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion que da las compras del periodo de todas las personas

def f_periodo_ventas(param_visita, m_bin_comb, v_prob_comb, v_prob_cant, param_v_precios,
                     param_v_costos, param_v_horas):
    """
    Parameters
    ----------
    param_visita : int : personas que asisten y compran en el periodo
    m_bin_comb : list : matriz de posibles combinaciones binarias
    v_prob_comb : list : vector probabilidades de cada combinacion posible de productos
    v_prob_cant : list : vector probabilidades de cada cantidad posible comprada
    param_v_precios : list : vector de precios por producto
    param_v_costos : list : vector de costos por producto
    param_v_horas : list : vector de horas por productp

    Returns
    -------
    v_periodo : list : venta del periodo (mes) de todas las personas
    Debugging
    -------
    param_visita = 217
    param_m_bin_comb = [[[0, 0],[0, 1],[1, 0],[1, 1]]]
    param_v_prob_comb = [0.1, 0.45, 0.85, 1]
    param_v_prob_cant = [0.1, 0.8, 1]
    param_v_precios = [10, 20]
    param_v_costos = [5, 10, 12]
    param_v_horas = [0.25, 0.5, 1]
    """

    # Se simulan las ventas por personas, con el numero que visitaron y compraron (mes)
    v_periodo = [f_ventas_persona(m_bin_comb, v_prob_comb, v_prob_cant, param_v_precios,
                                  param_v_costos, param_v_horas) for i in range(param_visita)]

    return v_periodo


# - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Ventas totales por persona - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion de ventas totales por personas y periodo de tiempo

def f_ventas_total(param_n_periodos, n_canales, param_beta, param_segmento, param_tendencia,
                   param_porcentaje_compran,
                   m_bin_comb, v_prob_comb, v_prob_cant, param_v_precios, param_v_costos,
                   param_v_horas):
    """
    Parameters
    ----------
    param_n_periodos : int : numero de meses a simular
    n_canales : int : numero de canales por segmento
    param_beta : list : lista de listas de los parametros para la funcion de ventas por mes
    param_segmento : int : numero de personas por segmentos
    param_porcentaje_compran : float : porcentaje que comprarian este producto
    m_bin_comb : list : matriz de posibles combinaciones binarias
    v_prob_comb : list : vector probabilidades de cada combinacion posible de productos
    v_prob_cant : list : vector probabilidades de cada cantidad posible comprada
    param_v_precios : list : vector de precios por producto
    param_v_costos :
    param_v_horas :
    Returns
    -------
    m_visitan : np.array : visitan, regresan, compran de funcion f_serie_tiempo_visitan
    m_ventas_totales_persona
    m_visitan_canal : list :  por canal visitan, regresan, compran de funcion
                              f_serie_tiempo_visitan
    Debugging
    -------
    param_n_periodos = 18
    n_canales = 1
    param_porcentaje_compran = 0.75
    param_beta = [[[1.5, 4, 0, 0.1], [4, 2, 0, 0.2], [1, 2, 0, 0.05], [4.5, 1.5, 0.2, 0.55]]]
    param_segmento = [10800]
    ...
    param_visita = 217
    param_m_bin_comb = [[[0, 0],[0, 1],[1, 0],[1, 1]]]
    param_v_prob_comb = [0.1, 0.45, 0.85, 1]
    param_v_prob_cant = [0.1, 0.8, 1]
    param_v_precios = [10, 20]
    param_v_costos = [5, 10, 12]
    param_v_horas = [0.25, 0.5, 1]
    """

    # Matriz que regresa las personas que van [vistan, compran, regresan] durante n_periodos
    m_visitan, m_visitan_canal = f_serie_tiempo_visitan(param_n_periodos, n_canales,
                                                        param_beta, param_segmento, param_tendencia)

    # Matriz de ventas por persona y periodo
    m_ventas_totales_persona = [
        f_periodo_ventas(int(m_visitan[1][i] * param_porcentaje_compran), m_bin_comb,
                         v_prob_comb, v_prob_cant,
                         param_v_precios, param_v_costos, param_v_horas) for i in
        range(param_n_periodos)]

    return m_visitan, m_ventas_totales_persona, m_visitan_canal


# - - - - - - - - - - - - - - - - - - - - - - - - - -  FUNCION: Extraer datos especificos - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion para extraer de f_ventas_total un dato especifico

def f_extract(param_obj, param_k_num, param_b_suma):
    """
    Parameters
    ----------
    param_obj : list : return de funcion f_ventas_total
    param_k_num : int : numero [0, 4] donde 0 es ingreso, 1 es utilidad,
                        2 ventas por producto, 3 costo por producto, 4 horas
    param_b_suma : bool : La suma de todos los datos del periodo
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
        dato = [np.sum([param_obj[1][j][i][param_k_num] for i in range(len(param_obj[1][j]))])
                for j in range(len(param_obj[1]))]
    else:
        dato = [[param_obj[1][j][i][param_k_num] for i in range(len(param_obj[1][j]))] for j in
                range(len(param_obj[1]))]
    return dato


# - - - - - - - - - - - - - - - - - - - - - - - - - - -  FUNCION: Simulaciones de proceso - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion para simular por completo un proceso

def f_n_simulaciones_proceso(n_sim, list_parameters_ventas, list_parameters_costos):
    """
    Parameters
    ----------
    n_sim : int : numero de simulaciones
    list_parameters_ventas : list : lista de parametros para f_ventas_total
    list_parameters_costos : list : lista de parametros para f_ts_costos
    Returns
    -------
    dato1 : list : return de algunos datos de f_ventas_total
    dato2 : list : return de f_ts_costos
    dato3 : list : segundo return de f_serie_tiempo_visitan (por canal)

    Debugging
    -------
    list_parameters_ventas
    """

    obj = [f_ventas_total(list_parameters_ventas[0], list_parameters_ventas[1],
                          list_parameters_ventas[2],
                          list_parameters_ventas[3], list_parameters_ventas[4],
                          list_parameters_ventas[5],
                          list_parameters_ventas[6], list_parameters_ventas[7],
                          list_parameters_ventas[8],
                          list_parameters_ventas[9], list_parameters_ventas[10],
                          list_parameters_ventas[11]) for i in
           range(n_sim)]
    # Por canal
    visitantes_canal = [np.array(obj[i][2][0][1:]) for i in range(n_sim)]
    compradores_canal = [np.array(obj[i][2][1]) for i in range(n_sim)]
    regresan_canal = [np.array(obj[i][2][2]) for i in range(n_sim)]

    # visitantes totales, compradores totales, regresan, ingresos, costos, utilidad, horas
    datos1 = [[obj[i][0][0], obj[i][0][1], obj[i][0][2], f_extract(obj[i], 0, True),
               f_extract(obj[i], 1, True),
               f_extract(obj[i], 2, True), f_extract(obj[i], 4, True),
               f_extract(obj[i], 5, True)] for i in range(n_sim)]

    # acompanantes, costos de los banos, personas taller, costo taller
    datos2 = [f_ts_costos(list_parameters_costos[0], datos1[i][0], list_parameters_costos[1],
                          list_parameters_costos[2], list_parameters_costos[3],
                          list_parameters_costos[4], list_parameters_costos[5],
                          list_parameters_costos[6]) for i in range(n_sim)]
    datos3 = [visitantes_canal, compradores_canal, regresan_canal]
    return datos1, datos2, datos3


# - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: DataFrames de Simulaciones - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion para generar dataframes de simulaciones completas de proceso

def f_dataframes(n_sim, list_parameters_v, list_parameters_c, dataframe_n):
    """
    Parameters
    ----------
    n_sim : int : numero de simulaciones
    list_parameters_v : list : lista de parametros de ventas
    list_parameters_c : list : lista de parametros de costos
    dataframe_n : str : tipo de DataFrame
    Returns
    -------
    dato : lis : serie de tiempo del dato requerido
    Debugging
    -------
    list_parameters
    """

    datos1, datos2, datos3 = f_n_simulaciones_proceso(n_sim, list_parameters_v,
                                                      list_parameters_c)

    # datos 1: Visitantes, Compradores, Regresa, ingresos, costos, utilidad,
    #                   0            1        2         3       4         5
    # horas, total productos
    #     6,               7

    # datos 2 : acompañantes, costos de los baños, personas taller, costo taller,
    #                      0                    1                2             3

    # costos fijos, familias taller
    #            4,               5

    # datos 3 - len 3 y adentro numero de simulaciones : simulaciones v, c, r

    # - - - DataFrame para datos basicos

    if dataframe_n == 'completo':
        nombres = ['Visitantes', 'Acompanantes', 'Compradores', 'Regresan', 'Personas taller',
                   'Costo de taller', 'Costo de banos',
                   'Ingreso', 'Costo productos', 'Utilidad', 'Horas']

        lista = [[datos1[i][0], datos2[i][0], datos1[i][1], datos1[i][2], datos2[i][2],
                  datos2[i][3], datos2[i][1],
                  datos1[i][3], datos1[i][4], datos1[i][5], datos1[i][6]] for i in
                 range(n_sim)]

        DF_results = [pd.DataFrame(lista[i], index=nombres).T for i in range(n_sim)]

        return DF_results

    # - - - DataFrame para flujo de efectivo

    if dataframe_n == 'flujo':
        nombres = ['Ingresos', 'Costos Variables', 'Costos Fijos', 'Utilidad']

        flujo = [[datos1[i][3],
                  (np.array(datos1[i][4]) + np.array(datos2[i][1]) + np.array(datos2[i][3])),
                  datos2[i][4],
                  (np.array(datos1[i][3]) - (
                              np.array(datos2[i][4]) + np.array(datos1[i][4]) + np.array(
                          datos2[i][1]) + np.array(datos2[i][3])))] for i in range(n_sim)]

        DF_results = [pd.DataFrame(flujo[i], index=nombres).T for i in range(n_sim)]

        return DF_results

    # - - - DataFrame para segmento C

    if dataframe_n == 'personas c':
        nombres = ['Asambleas', 'Talleres', 'Plantas', 'Comidas']

        personas = [[datos3[0][i][:, 0], datos2[i][5], datos3[1][i][:, 0], datos3[1][i][:, 1]]
                    for i in range(n_sim)]

        DF_results = [pd.DataFrame(personas[i], index=nombres).T for i in range(n_sim)]

        return DF_results

    # - - - DataFrame para segmento C

    if dataframe_n == 'metricas sociales':

        nombres = ['Actividad Economica', 'Participacion', 'Educacion Social', 'Comunicacion']

        lista = [[datos1[i][7], datos3[0][i][:, 0], datos2[i][5], datos3[0][i][:, 0]] for i in
                 range(n_sim)]

        DF_results = [pd.DataFrame(lista[i], index=nombres).T for i in range(n_sim)]

        return DF_results

    else:
        return datos1, datos2, datos3


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# COSTOS
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# - - - - - - - - - - - - - - - - - - - - - - - - - -  FUNCION: Serie de tiempo de costos - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion para generar datos de serie de tiempo de los costos

def f_ts_costos(param_v_sector_prob_acomp, param_v_visitantes, param_k_min_acomp,
                param_porcentaje_bano, param_costo_bano,
                param_porcentaje_taller, param_costo_taller, param_costos_fijos):
    """
    Parameters
    ----------
    param_v_sector_prob_acomp : list : vector con las probabilidades de acompañantes
    param_v_visitantes : list : vector de visitantes en el periodo
    param_k_min_acomp : int : numero acompañantes
    param_porcentaje_bano : float : porcentaje de los visitantes que van al baño
    param_costo_bano : int : costo de mantenimiento de baño
    param_porcentaje_taller : float : porcentaje que irian al taller
    param_costo_taller
    param_costos_fijos
    Returns
    -------
    v_cant_acom : list : cantidad de acompañantes por sector
    Debugging
    -------
    param_vectorprob = [.2, .8, 1]
    param_seg= [342]
    """

    v_acompanantes = [sim.f_acompanantes_periodo(param_v_sector_prob_acomp,
                                                 int(param_v_visitantes[i]),
                                                 param_k_min_acomp) for i in
                      range(len(param_v_visitantes))]

    # Banos
    personas_banos = [sim.f_prob_binomial(param_porcentaje_bano, int(param_v_visitantes[i]),
                                          v_acompanantes[i]) for i in
                      range(len(param_v_visitantes))]
    costo_banos = param_costo_bano * np.array(personas_banos)

    # Talleres
    personas_taller = [sim.f_prob_binomial(param_porcentaje_taller, int(param_v_visitantes[i]),
                                           v_acompanantes[i]) for i in
                       range(len(param_v_visitantes))]

    familias_taller = [sim.f_prob_binomial(param_porcentaje_taller, int(param_v_visitantes[i]),
                                           0) for i in range(len(param_v_visitantes))]

    insumos_taller = param_costo_taller * np.array(personas_taller)

    # Costos Fijos
    costos_fijos = np.full(shape=len(param_v_visitantes), fill_value=param_costos_fijos)

    return v_acompanantes, list(itertools.chain(*costo_banos)), list(
        itertools.chain(*personas_taller)), list(
        itertools.chain(*insumos_taller)), costos_fijos, list(
        itertools.chain(*familias_taller))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - FUNCION: Metricas financieras - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion para generar las metricas financieras

def f_metricas_financieras(utilidad, param_inversion, param_tasa, n_sim):
    """
    Parameters
    ----------
    utilidad : DataFrame : utilidades de todas las simulaciones
    param_inversion : int : inversion inicial
    param_tasa : float : tasa de descuento
    n_sim : int : numero de simulaciones

    Returns
    -------
    vpn : list : valor presente neto
    tir : list : tasa interna de retorno
    Debugging
    -------
    utilidad = pd.DataFrame([100, 200, 300], [100, 150, 350])
    param_inversion = 9000
    param_tasa = 0.10
    n_sim = 10
    """

    inversion = pd.DataFrame(np.full(shape=n_sim, fill_value=-param_inversion))
    flujo = pd.concat([inversion.T, utilidad]).reset_index(drop=True)

    vpn = [np.npv(param_tasa, flujo.iloc[:, i]) for i in range(n_sim)]
    tir = [round(np.irr(flujo.iloc[:, i])*100, 2) for i in range(n_sim)]

    return vpn, tir
