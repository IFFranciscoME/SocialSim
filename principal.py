
# .. ................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos        .. #
# .. Archivo: principal.py - flujo principal de uso                                      .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                  .. #
# .. Licencia: Todos los derechos reservados                                             .. #
# .. Repositorio: https://github.com/                                                    .. #
# .. ................................................................................... .. #

import procesos as pr
import datos as dat
import simulaciones as sim
import visualizaciones as vs
import numpy as np
import pandas as pd
from time import time

t0 = time()

if __name__ == "__main__":

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Colores para graficas

    colores = dict(azul_f='#047CFB', azul_b='#418FFB', azul_m='#004A94', hopbush='#d863b3',
                   gris_f='#6B6B6B', gris_b='#ABABAB', naranja_b='#FB8304',
                   verde_f='#42c29b', verde_b='#04CBCC')

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Funcion para matriz de combinaciones

    ''' Parametros: 
            Numero de productos que se venderian
            Parametros para la distribucion de las combinaciones'''

    # Matriz de combinaciones y vector de probabilidad por combinacion para Plantas
    m_bin_comb_p, v_prob_comb_p = sim.f_prob_combinaciones(dat.k_plantas, dat.param_comb)

    # Matriz de combinaciones y vector de probabilidad por combinacion para Comidas
    m_bin_comb_c, v_prob_comb_c = sim.f_prob_combinaciones(dat.k_comidas, dat.param_comb)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Funcion para vector de probabilidades de cantidad

    ''' Parametros: 
            Numero maximo de productos que se venderian
            Distribucion que seguiria las diferentes cantidades
            Parametros para la distribucion de las cantidades'''

    # Vector de probabilidades de la cantidad de productos que se vendera
    v_prob_cant = sim.f_prob_cantidad(dat.k_max_prod, 'expon', dat.param_cant)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Funcion para vector de probabilidades de acompanantes

    ''' Parametros: 
            Numero de acompanantes del sector
            Distribucion que seguiria las diferentes numero de acompanantes
            Parametros para la distribucion de los acompanantes'''

    # Acompanantes para segmento de clientes A
    param_v_sector_A_prob_acom = sim.f_prob_cantidad(dat.n_acomp_A, 'beta', dat.param_acomp_A)
    # Acompanantes para segmento de clientes B
    param_v_sector_B_prob_acom = sim.f_prob_cantidad(dat.n_acomp_B, 'beta', dat.param_acomp_B)
    # Acompanantes para segmento de clientes C
    param_v_sector_C_prob_acom = sim.f_prob_cantidad(dat.n_acomp_C, 'beta', dat.param_acomp_C)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Numero de periodos que se simulan
    t = dat.t
    # Numero de simulaciones
    n_sim = dat.n_sim

    ''' Parametros de ventas
            Numero de periodos (meses) que se simularian
            Numero de canales: Facebook, Iteso y Plaza
            Parametros para distribuciones de las simulaciones de visitas, regresos, compras
            Numero de personas alcanzadas por canal
            Porcentaje de personas que comprarian pantas
            - - - 
            Matriz de posibles combinaciones (f_prob_combinaciones)
            Vector de probabilidades por combinacion (f_prob_combinaciones)
            Vector de probabilidades por cantidad (f_prob_cantidad)
            Vector de lista de precios por producto
            Vector de lista de costos por producto'''

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    # Lista completa de parametros necesarios para calculos de ventas de plantas al segmento A
    param_a_v_p = [t, dat.n_canales_a, dat.param_beta_a, dat.p_total_A, dat.tendencia_a,
                   dat.k_plantas_porcentaje,
                   m_bin_comb_p, v_prob_comb_p, v_prob_cant, dat.v_plantas_p, dat.v_plantas_c,
                   dat.v_plantas_h]

    # Lista completa de parametros necesarios para calculos de ventas de plantas al segmento B
    param_b_v_p = [t, dat.n_canales_b, dat.param_beta_b, dat.p_total_B, dat.tendencia_b,
                   dat.k_plantas_porcentaje,
                   m_bin_comb_p, v_prob_comb_p, v_prob_cant, dat.v_plantas_p, dat.v_plantas_c,
                   dat.v_plantas_h]

    # Lista completa de parametros necesarios para calculos de ventas de plantas al segmento C
    param_c_v_p = [t, dat.n_canales_c, dat.param_beta_c, dat.p_total_C, dat.tendencia_c,
                   dat.k_plantas_porcentaje,
                   m_bin_comb_p, v_prob_comb_p, v_prob_cant, dat.v_plantas_p, dat.v_plantas_c,
                   dat.v_plantas_h]

    # Lista completa de parametros necesarios para calculos de ventas de comidas al segmento A
    param_a_v_c = [t, dat.n_canales_a, dat.param_beta_a, dat.p_total_A, dat.tendencia_a,
                   dat.k_comidas_porcentaje,
                   m_bin_comb_c, v_prob_comb_c, v_prob_cant, dat.v_comidas_p, dat.v_comidas_c,
                   dat.v_comidas_h]

    # Lista completa de parametros necesarios para calculos de ventas de comidas al segmento B
    param_b_v_c = [t, dat.n_canales_b, dat.param_beta_b, dat.p_total_B, dat.tendencia_b,
                   dat.k_comidas_porcentaje,
                   m_bin_comb_c, v_prob_comb_c, v_prob_cant, dat.v_comidas_p, dat.v_comidas_c,
                   dat.v_comidas_h]

    # Lista completa de parametros necesarios para calculos de ventas de comidas al segmento C
    param_c_v_c = [t, dat.n_canales_c, dat.param_beta_c, dat.p_total_C, dat.tendencia_c,
                   dat.k_comidas_porcentaje,
                   m_bin_comb_c, v_prob_comb_c, v_prob_cant, dat.v_comidas_p, dat.v_comidas_c,
                   dat.v_comidas_h]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    ''' Parametros de costos
            Parametros para las distribuciones de acompanantes
            Numero minimo de acompanantes por sector
            Porcentaje de personas que van al bano
            Costo por uso de bano
            Porcentaje de personas que van a los talleres
            Costo de insumos de talleres
    '''

    param_a_c = [param_v_sector_A_prob_acom, dat.min_acomp_A, dat.porcentaje_bano,
                 dat.bano_insumo_c, dat.porcentaje_taller_A, dat.taller_insumo_c,
                 dat.costo_total_fijo / 2]

    param_b_c = [param_v_sector_B_prob_acom, dat.min_acomp_B, dat.porcentaje_bano,
                 dat.bano_insumo_c, dat.porcentaje_taller_B, dat.taller_insumo_c,
                 dat.costo_total_fijo / 2]

    param_c_c = [param_v_sector_C_prob_acom, dat.min_acomp_C, dat.porcentaje_bano,
                 dat.bano_insumo_c, dat.porcentaje_taller_C, dat.taller_insumo_c,
                 dat.costo_total_fijo]

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # DataFrame por segementos

    df_a_plantas_flujo = pr.f_dataframes(n_sim, param_a_v_p, param_a_c, 'flujo')
    df_a_comidas_flujo = pr.f_dataframes(n_sim, param_a_v_c, param_a_c, 'flujo')

    df_b_plantas_flujo = pr.f_dataframes(n_sim, param_b_v_p, param_b_c, 'flujo')
    df_b_comidas_flujo = pr.f_dataframes(n_sim, param_b_v_c, param_b_c, 'flujo')

    df_c = pr.f_dataframes(n_sim, param_c_v_p, param_c_c, 'personas c')

    df_a_plantas_completo = pr.f_dataframes(n_sim, param_a_v_p, param_a_c, 'completo')
    df_a_comidas_completo = pr.f_dataframes(n_sim, param_a_v_c, param_a_c, 'completo')

    df_b_plantas_completo = pr.f_dataframes(n_sim, param_b_v_p, param_b_c, 'completo')
    df_b_comidas_completo = pr.f_dataframes(n_sim, param_b_v_c, param_b_c, 'completo')

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Info necesaria para metricas

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # SEGMENTO A y B

    # Utilidad

    keys_u = ['Utilidad_A-Plantas', 'Utilidad_A-Comidas', 'Utilidad_B-Plantas',
              'Utilidad_B-Comidas']

    utilidad_segmento = [
        pd.concat([df_a_plantas_flujo[i].iloc[:, 3], df_a_comidas_flujo[i].iloc[:, 3],
                   df_b_plantas_flujo[i].iloc[:, 3], df_b_comidas_flujo[i].iloc[:, 3]], axis=1,
                  keys=keys_u) for i in range(n_sim)]

    utilidad_total = pd.concat(
        [pd.concat([df_a_plantas_flujo[i].iloc[:, 3], df_a_comidas_flujo[i].iloc[:, 3],
                    df_b_plantas_flujo[i].iloc[:, 3], df_b_comidas_flujo[i].iloc[:, 3]],
                   axis=1).T.sum() for i in range(n_sim)], axis=1)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # SEGMENTO C

    # Horas de trabajo

    keys_h = ['Horas_A-Plantas', 'Horas_A-Comidas', 'Horas_B-Plantas', 'Horas_B-Comidas']

    horas_segmento = [
        pd.concat([df_a_plantas_completo[i].iloc[:, 10], df_a_comidas_completo[i].iloc[:, 10],
                   df_b_plantas_completo[i].iloc[:, 10], df_b_comidas_completo[i].iloc[:, 10]],
                  axis=1, keys=keys_h) for i in range(n_sim)]

    keys_sim = list(np.arange(n_sim).astype('U'))

    horas_total = pd.concat(
        [pd.concat([df_a_plantas_completo[i].iloc[:, 10],
                    df_a_comidas_completo[i].iloc[:, 10],
                    df_b_plantas_completo[i].iloc[:, 10],
                    df_b_comidas_completo[i].iloc[:, 10]],
                   axis=1).T.sum() for i in range(n_sim)], axis=1, keys=keys_sim)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Participantes de asambleas

    asamblea_total = pd.concat([df_c[i].iloc[:, 0]
                                for i in range(n_sim)], axis=1, keys=keys_sim)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Participantes en talleres

    taller_total = pd.concat([df_c[i].iloc[:, 1] for i in range(n_sim)], axis=1, keys=keys_sim)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Familias que no van a la asamblea pero ven el mural en la casa comunal

    ven_mural = pd.DataFrame(sim.f_familias_mural(asamblea_total, dat.total_familias,
                                                  dat.porcentaje_familias_van_casa,
                                                  dat.porcentaje_familias_ven_mural),
                             index=keys_sim).T

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Metricas Sociales

    # 1. Actividad Economica: Utilidad total / Familias que venden
    fam_venden = [int(df_c[i]['Plantas'].iloc[len(df_c[i]['Plantas'])-1] +
                      df_c[i]['Comidas'].iloc[len(df_c[i]['Comidas'])-1])
                  for i in range(0, len(df_c))]

    # Promedio Ponderado del Ingreso Familiar (Mensual, en pesos)
    ppif = 8520
    ms_actividad_economica = (ppif +
                              utilidad_total.iloc[len(utilidad_total)-1, :]/fam_venden)

    # Obtener la metrica 1: Actividad economica
    ms_actividad_economica_metrica = np.array(ms_actividad_economica).mean()

    # 2. Participacion: Horas de plantas + Horas de comidas + Horas de asambleas
    ms_participacion = asamblea_total * dat.horas_asamblea_fam + horas_total
    ms_participacion = ms_participacion.iloc[len(ms_participacion)-1, :]
    # Obtener la metrica 2: Participacion
    ms_participacion_metrica = np.array(ms_participacion).mean()

    # 3. Educacion Social: Familias asistentes a talleres / total de Familias
    ms_educ_social = (taller_total / dat.total_familias)*100
    ms_educ_social = ms_educ_social.iloc[len(ms_educ_social)-1, :]
    # Obtener la metrica 3: Educacion Social
    ms_educ_social_metrica = np.array(ms_educ_social).mean()

    # 4. Comunicacion: Familias asistentes asambleas +
    # Familias ven el periodico mural que no fueron a la asamblea
    ms_comunicacion = asamblea_total + ven_mural
    ms_comunicacion = ms_comunicacion.iloc[len(ms_comunicacion)-1, :]
    # Obtener la metrica 4: Comunicacion
    ms_comunicacion_metrica = np.array(ms_comunicacion).mean()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Metricas Financieras

    mf_vpn, mf_tir = pr.f_metricas_financieras(utilidad_total, dat.inversion, dat.tasa, n_sim)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    t1 = time()
    # print(t1 - t0)
    print('el tiempo transcurrido fue: ' + str(t1-t0))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Graficas: Sociales - #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Generacion de graficas (Histograma y Simulacion de series de tiempo)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ACTIVIDAD ECONOMICA - #
    colores_a = {'marker': colores['verde_f']}
    etiquetas_a = {'titulo': '<b> Valores simulados de ACTIVIDAD ECONOMICA </b> <br> '
                             'Promedio Ponderado del Ingreso Mensual Familiar',
                   'ejex': 'Promedio Ponderado del Ingreso Mensual Familiar (Pesos)',
                   'ejey': 'probabilidad'}

    # - - Histograma
    fig_actividad_econ = vs.g_histograma(param_val=ms_actividad_economica,
                                         param_colores=colores_a,
                                         param_etiquetas=etiquetas_a)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - PARTICIPACION - #
    colores_p = {'marker': colores['azul_m']}
    etiquetas_p = {'titulo': '<b> Valores simulados de PARTICIPACION </b> <br> '
                             'Horas totales de participación dentro de la comunidad',
                   'ejex': 'Horas totales de participación dentro de la comunidad',
                   'ejey': 'probabilidad'}

    # - - Histograma
    fig_participacion = vs.g_histograma(param_val=ms_participacion, param_colores=colores_p,
                                        param_etiquetas=etiquetas_p)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  EDUCACION SOCIAL - #
    colores_e = {'marker': colores['hopbush']}
    etiquetas_e = {'titulo': '<b> Valores simulados de EDUCACION SOCIAL </b> <br> '
                             '% de familias que asisten a talleres sociales',
                   'ejex': '% de familias que asisten a talleres sociales',
                   'ejey': 'probabilidad'}

    # - - Histograma
    fig_educacion = vs.g_histograma(param_val=ms_educ_social, param_colores=colores_e,
                                    param_etiquetas=etiquetas_e)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  COMUNICACION - #
    colores_c = {'marker': colores['naranja_b']}
    etiquetas_c = {'titulo': '<b> Valores simulados de COMUNICACION </b> <br> '
                             'familias comunicadas (asambleas + mural)',
                   'ejex': 'familias comunicadas (asambleas + mural)',
                   'ejey': 'probabilidad'}

    # - - Histograma
    fig_comunicacion = vs.g_histograma(param_val=ms_comunicacion, param_colores=colores_c,
                                       param_etiquetas=etiquetas_c)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Graficas: Economicas - #
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Generacion de graficas

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - TIR - #
    colores_t = {'marker': colores['azul_b']}
    etiquetas_t = {'titulo': '<b> Valores simulados de TIR </b> <br> '
                   'Tasa Interna de Retorno a la Inversión',
                   'ejex': 'rango de valores TIR (%)', 'ejey': 'probabilidad'}

    # - - Histograma
    fig_TIR = vs.g_histograma(param_val=mf_tir, param_colores=colores_t,
                              param_etiquetas=etiquetas_t)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - VPN - #
    colores_v = {'marker': colores['gris_f']}
    etiquetas_v = {'titulo': '<b> Valores simulados de VPN </b> <br> '
                   'Valor Presente Neto de Flujos de la Inversión',
                   'ejex': 'rango de valores VPN (Pesos)', 'ejey': 'probabilidad'}

    # - - Histograma
    fig_VPN = vs.g_histograma(param_val=mf_vpn, param_colores=colores_v,
                              param_etiquetas=etiquetas_v)

    fig_actividad_econ.show()
    fig_participacion.show()
    fig_educacion.show()
    fig_comunicacion.show()

    fig_TIR.show()
    fig_VPN.show()

    print('Final de codigo')
