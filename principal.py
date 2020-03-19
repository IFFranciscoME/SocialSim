
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
        Numero de canales: Facebook y Iteso
        Numero de periodos simulados (18 meses)
        Parametros para las distribuciones de las simulaciones de visitas, regresos, compras
        Numero de personas alcanzadas por segmentos
        Personas que visitaron en el tiempo t-1
        - - - 
        Numero de personas en el periodo de tiempo actual,  que se repetira la funcion anterior
        Matriz de posibles combinaciones (funcion en simulaciones: f_prob_combinaciones)
        Vector de probabilidades por combinacion (f_prob_combinaciones)
        Vector de probabilidades por cantidad (f_prob_cantidad)
        Vector de lista de precios por producto
        Vector de lista de costos por producto'''
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        
param_a_v_p = [t, dat.n_canales, dat.param_beta, dat.p_total_A, dat.k_plantas_porcentaje, # Parametros de f_serie_tiempo_visitan
                           m_bin_comb, v_prob_comb, v_prob_cant, dat.v_plantas_p, dat.v_plantas_c, dat.v_plantas_h]
param_b_v_p = [t, dat.n_canales, dat.param_beta, dat.p_total_B, dat.k_plantas_porcentaje, # Parametros de f_serie_tiempo_visitan
                           m_bin_comb, v_prob_comb, v_prob_cant, dat.v_plantas_p, dat.v_plantas_c, dat.v_plantas_h]
param_c_v_p = [t, dat.n_canales_c, dat.param_beta_c, dat.p_total_C, dat.k_plantas_porcentaje, # Parametros de f_serie_tiempo_visitan
                           m_bin_comb, v_prob_comb, v_prob_cant, dat.v_plantas_p, dat.v_plantas_c, dat.v_plantas_h]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
param_a_v_c = [t, dat.n_canales, dat.param_beta, dat.p_total_A, dat.k_comidas_porcentaje, # Parametros de f_serie_tiempo_visitan
                           m_bin_comb_c, v_prob_comb_c, v_prob_cant, dat.v_comidas_p, dat.v_comidas_c, dat.v_comidas_h]
param_b_v_c = [t, dat.n_canales, dat.param_beta, dat.p_total_B, dat.k_comidas_porcentaje, # Parametros de f_serie_tiempo_visitan
                           m_bin_comb_c, v_prob_comb_c, v_prob_cant, dat.v_comidas_p, dat.v_comidas_c, dat.v_comidas_h]
param_c_v_c = [t, dat.n_canales_c, dat.param_beta_c, dat.p_total_C, dat.k_comidas_porcentaje, # Parametros de f_serie_tiempo_visitan
                           m_bin_comb_c, v_prob_comb_c, v_prob_cant, dat.v_comidas_p, dat.v_comidas_c, dat.v_comidas_h]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

''' Parametros de costos
        Parametros para las distribuciones de acompañantes
        Numero minimo de acompañantes por sector
        Porcentaje de personas que van al baño
        Costo por uso de baño
        Porcentaje de personas que van a los talleres
        Costo de insumos de talleres
'''
param_a_c = [param_v_sector_A_prob_acom, dat.min_acomp_A, dat.porcentaje_baño, 
                                         dat.baño_insumo_c, dat.porcentaje_taller_A, dat.taller_insumo_c, dat.costo_total_fijo]
param_b_c = [param_v_sector_B_prob_acom, dat.min_acomp_B, dat.porcentaje_baño, 
                                         dat.baño_insumo_c, dat.porcentaje_taller_B, dat.taller_insumo_c, dat.costo_total_fijo]
param_c_c = [param_v_sector_C_prob_acom, dat.min_acomp_C, dat.porcentaje_baño, 
                                         dat.baño_insumo_c, dat.porcentaje_taller_C, dat.taller_insumo_c, dat.costo_total_fijo]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Df_A_plantas_flujo = pr.f_DataFrames(10, param_a_v_p, param_a_c, 'flujo')
Df_B_plantas_flujo = pr.f_DataFrames(10, param_b_v_p, param_b_c, 'flujo')

Df_A_comidas_flujo = pr.f_DataFrames(10, param_a_v_c, param_a_c, 'flujo')
Df_B_comidas_flujo = pr.f_DataFrames(10, param_b_v_c, param_b_c, 'flujo')

Df_C = pr.f_DataFrames(10, param_c_v_p, param_c_c, 'personas c')


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#%%


#vpn = [np.npv(rate, utilidad[i]) for i in range(n_sim)]
#tir = [np.irr(rate, utilidad[i]) for i in range(n_sim)]







