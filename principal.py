
# .. .................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos         .. #
# .. Archivo: principal.py - flujo principal de uso                                       .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                   .. #
# .. Licencia: Todos los derechos reservados                                              .. #
# .. Repositorio: https://github.com/                                                     .. #
# .. .................................................................................... .. #
import procesos as pr
import datos as dat
import simulaciones as sim
import numpy as np
import pandas as pd
from time import time

t0 = time()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion para matriz de combinaciones

''' Parametros: 
        Numero de productos que se venderian
        Parametros para la distribucion de las combinaciones'''

m_bin_comb, v_prob_comb = sim.f_prob_combinaciones(dat.k_plantas, dat.param_comb)

m_bin_comb_c, v_prob_comb_c = sim.f_prob_combinaciones(dat.k_comidas, dat.param_comb)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion para vector de probabilidades de cantidad

''' Parametros: 
        Numero maximo de productos que se venderian
        Distribucion que seguiria las diferentes cantidades
        Parametros para la distribucion de las cantidades'''

v_prob_cant = sim.f_prob_cantidad(dat.k_max_prod, 'expon', dat.param_cant)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion para vector de probabilidades de acompañantes

''' Parametros: 
        Numero de acompañantes del sector
        Distribucion que seguiria las diferentes numero de acompañantes
        Parametros para la distribucion de los acompañantes'''

param_v_sector_A_prob_acom = sim.f_prob_cantidad(dat.n_acomp_A, 'beta', dat.param_acomp_A)
param_v_sector_B_prob_acom = sim.f_prob_cantidad(dat.n_acomp_B, 'beta', dat.param_acomp_B)
param_v_sector_C_prob_acom = sim.f_prob_cantidad(dat.n_acomp_C, 'beta', dat.param_acomp_C)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Numero de periodos que se simulan
t = 18

# Numero de simulaciones
n = 10

''' Parametros de ventas
        Numero de periodos (meses) que se simularian
        Numero de canales: Facebook, Iteso y Plaza
        Parametros para las distribuciones de las simulaciones de visitas, regresos, compras
        Numero de personas alcanzadas por canal
        Porcentaje de personas que comprarian pantas
        - - - 
        Matriz de posibles combinaciones (f_prob_combinaciones)
        Vector de probabilidades por combinacion (f_prob_combinaciones)
        Vector de probabilidades por cantidad (f_prob_cantidad)
        Vector de lista de precios por producto
        Vector de lista de costos por producto'''
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        
param_a_v_p = [t, dat.n_canales_a, dat.param_beta_a, dat.p_total_A,
               dat.k_plantas_porcentaje,  # Parametros de f_serie_tiempo_visitan
               m_bin_comb, v_prob_comb, v_prob_cant, dat.v_plantas_p,
               dat.v_plantas_c, dat.v_plantas_h]
param_b_v_p = [t, dat.n_canales_b, dat.param_beta_b, dat.p_total_B,
               dat.k_plantas_porcentaje,  # Parametros de f_serie_tiempo_visitan
               m_bin_comb, v_prob_comb, v_prob_cant, dat.v_plantas_p,
               dat.v_plantas_c, dat.v_plantas_h]
param_c_v_p = [t, dat.n_canales_c, dat.param_beta_c, dat.p_total_C,
               dat.k_plantas_porcentaje,  # Parametros de f_serie_tiempo_visitan
               m_bin_comb, v_prob_comb, v_prob_cant, dat.v_plantas_p,
               dat.v_plantas_c, dat.v_plantas_h]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
param_a_v_c = [t, dat.n_canales_a, dat.param_beta_a, dat.p_total_A,
               dat.k_comidas_porcentaje,  # Parametros de f_serie_tiempo_visitan
               m_bin_comb_c, v_prob_comb_c, v_prob_cant, dat.v_comidas_p,
               dat.v_comidas_c, dat.v_comidas_h]
param_b_v_c = [t, dat.n_canales_b, dat.param_beta_b, dat.p_total_B,
               dat.k_comidas_porcentaje,  # Parametros de f_serie_tiempo_visitan
               m_bin_comb_c, v_prob_comb_c, v_prob_cant, dat.v_comidas_p,
               dat.v_comidas_c, dat.v_comidas_h]
param_c_v_c = [t, dat.n_canales_c, dat.param_beta_c, dat.p_total_C,
               dat.k_comidas_porcentaje,  # Parametros de f_serie_tiempo_visitan
               m_bin_comb_c, v_prob_comb_c, v_prob_cant, dat.v_comidas_p,
               dat.v_comidas_c, dat.v_comidas_h]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

''' Parametros de costos
        Parametros para las distribuciones de acompañantes
        Numero minimo de acompañantes por sector
        Porcentaje de personas que van al baño
        Costo por uso de baño
        Porcentaje de personas que van a los talleres
        Costo de insumos de talleres
'''
param_a_c = [param_v_sector_A_prob_acom, dat.min_acomp_A, dat.porcentaje_bano,
                                         dat.bano_insumo_c, dat.porcentaje_taller_A,
             dat.taller_insumo_c, dat.costo_total_fijo/2]
param_b_c = [param_v_sector_B_prob_acom, dat.min_acomp_B, dat.porcentaje_bano,
                                         dat.bano_insumo_c, dat.porcentaje_taller_B,
             dat.taller_insumo_c, dat.costo_total_fijo/2]
param_c_c = [param_v_sector_C_prob_acom, dat.min_acomp_C, dat.porcentaje_bano,
                                         dat.bano_insumo_c, dat.porcentaje_taller_C,
             dat.taller_insumo_c, dat.costo_total_fijo]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# DataFrame por segementos

Df_A_plantas_flujo = pr.f_dataframes(n, param_a_v_p, param_a_c, 'flujo')
Df_B_plantas_flujo = pr.f_dataframes(n, param_b_v_p, param_b_c, 'flujo')

Df_A_comidas_flujo = pr.f_dataframes(n, param_a_v_c, param_a_c, 'flujo')
Df_B_comidas_flujo = pr.f_dataframes(n, param_b_v_c, param_b_c, 'flujo')

Df_C = pr.f_dataframes(n, param_c_v_p, param_c_c, 'personas c')

Df_A_plantas_completo = pr.f_dataframes(n, param_a_v_p, param_a_c, 'completo')
Df_A_comidas_completo = pr.f_dataframes(n, param_a_v_c, param_a_c, 'completo')

Df_B_plantas_completo = pr.f_dataframes(n, param_b_v_p, param_b_c, 'completo')
Df_B_comidas_completo = pr.f_dataframes(n, param_b_v_c, param_b_c, 'completo')


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Info necesaria para metricas

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# SEGMENTO A y B
#
# Utilidad 

keys_u = ['Utilidad_A-Plantas', 'Utilidad_A-Comidas',
          'Utilidad_B-Plantas', 'Utilidad_B-Comidas']

utilidad_segmento = [pd.concat([Df_A_plantas_flujo[i].iloc[:, 3],
                                Df_A_comidas_flujo[i].iloc[:, 3],
                                Df_B_plantas_flujo[i].iloc[:, 3],
                                Df_B_comidas_flujo[i].iloc[:, 3]],
                               axis=1, keys=keys_u) for i in range(n)]

utilidad_total = pd.concat([pd.concat([Df_A_plantas_flujo[i].iloc[:, 3],
                                       Df_A_comidas_flujo[i].iloc[:, 3],
                                       Df_B_plantas_flujo[i].iloc[:, 3],
                                       Df_B_comidas_flujo[i].iloc[:, 3]],
                                      axis=1).T.sum() for i in range(n)], axis=1)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# SEGMENTO C
#

# Horas de trabajo

keys_h = ['Horas_A-Plantas', 'Horas_A-Comidas', 'Horas_B-Plantas', 'Horas_B-Comidas']

horas_segmento = [pd.concat([Df_A_plantas_completo[i].iloc[:, 10],
                             Df_A_comidas_completo[i].iloc[:, 10],
                             Df_B_plantas_completo[i].iloc[:, 10],
                             Df_B_comidas_completo[i].iloc[:, 10]],
                            axis=1, keys=keys_h) for i in range(n)]

keys_sim = list(np.arange(n).astype('U'))

horas_total = pd.concat([pd.concat([Df_A_plantas_completo[i].iloc[:, 10],
                                    Df_A_comidas_completo[i].iloc[:, 10],
                                    Df_B_plantas_completo[i].iloc[:, 10],
                                    Df_B_comidas_completo[i].iloc[:, 10]],
                                   axis=1).T.sum() for i in range(n)], axis=1, keys=keys_sim)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Participantes de asambleas

asamblea_total = pd.concat([Df_C[i].iloc[:, 0] for i in range(n)], axis=1, keys=keys_sim)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Participantes en talleres

taller_total = pd.concat([Df_C[i].iloc[:, 1] for i in range(n)], axis=1, keys=keys_sim)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Familias que no van a la asamblea pero ven el mural debido a que asisten a la casa comunal

ven_mural = pd.DataFrame(sim.f_familias_mural(asamblea_total, dat.total_familias,
                                              dat.porcentaje_familias_van_casa,
                                              dat.porcentaje_familias_ven_mural),
                         index=keys_sim).T

# Metricas Sociales

# 1. Actividad Economica: Horas trabajadas * salario por hora
ms_actividad_economica = horas_total * dat.salario_hora

# 2. Participacion: Horas de plantas + Horas de comidas + Horas de asambleas
ms_participacion = asamblea_total * dat.horas_asamblea_fam + horas_total

# 3. Educacion Social: Familias asistentes a talleres / total de Familias
ms_educ_social = taller_total / dat.total_familias

# 4. Comunicacion: Familias asistentes asambleas +
# Familias ven el periodico mural que no fueron a la asamblea
ms_comunicacion = asamblea_total + ven_mural

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Metricas Financieras

mf_vpn, mf_tir = pr.f_metricas_financieras(utilidad_total, dat.inversion, dat.tasa, n)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Tiempo
t1 = time()
tiempo = (t1-t0)
print(tiempo)
