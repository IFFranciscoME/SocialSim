
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

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion para matriz de combinaciones

''' Parametros: 
        Numero de productos que se venderian
        Parametros para la distribucion de las combinaciones'''

m_bin_comb, v_prob_comb = sim.f_prob_combinaciones(dat.k_plantas, dat.param_comb)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion para vector de probabilidades de cantidad

''' Parametros: 
        Numero maximo de productos que se venderian
        Distribucion que seguiria las diferentes cantidades
        Parametros para la distribucion de las cantidades'''

v_prob_cant = sim.f_prob_cantidad(dat.k_max_prod, 'expon', dat.param_cant)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
t = 18

# Funcion que combina f_serie_tiempo_visitan y f_periodo_ventas

''' Parametros:
        Numero de periodos (meses) que se simularian
        Numero de canales: Facebook y Iteso:
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

vcr_iuvch_A = pr.f_ventas_total(t, dat.n_canales, dat.param_beta, dat.p_total_A, # Parametros de f_serie_tiempo_visitan
                           m_bin_comb, v_prob_comb, v_prob_cant, dat.v_plantas_p, dat.v_plantas_c, dat.v_plantas_h) # Parametros de f_periodo_ventas

vcr_iuvch_B = pr.f_ventas_total(t, dat.n_canales, dat.param_beta, dat.p_total_B, # Parametros de f_serie_tiempo_visitan
                           m_bin_comb, v_prob_comb, v_prob_cant, dat.v_plantas_p, dat.v_plantas_c, dat.v_plantas_h) # Parametros de f_periodo_ventas

vcr_iuvch_C = pr.f_ventas_total(t, dat.n_canales_c, dat.param_beta_c, dat.p_total_C, # Parametros de f_serie_tiempo_visitan
                           m_bin_comb, v_prob_comb, v_prob_cant, dat.v_plantas_p, dat.v_plantas_c, dat.v_plantas_h) # Parametros de f_periodo_ventas

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#%%
'''
    vcr_iuvc_A[1] los 18 periodos
    vcr_iuvc_A[1][0] las personas del primer periodo
    vcr_iuvc_A[1][0][0] los ingresos, las utilidades, ventas por producto, costo por productos, horas de una persona
    vcr_iuvc_A[1][0][0][0] ingresos
'''
def f_extract(obj, num, suma):
    if suma:
        dato = [np.sum([obj[1][j][i][num] for i in range(len(obj[1][j]))]) for j in range(len(obj[1]))]
    else:
        dato = [[obj[1][j][i][num] for i in range(len(obj[1][j]))] for j in range(len(obj[1]))]
    return dato
    
# Utilidad
utilidad_A = f_extract(vcr_iuvch_A, 1, True)
utilidad_B = f_extract(vcr_iuvch_B, 1, True)

# Horas
horas_A = f_extract(vcr_iuvch_A, 4, True)
horas_B = f_extract(vcr_iuvch_B, 4, True)

# Visitantes
visitantes_A = vcr_iuvch_A[0][0]
visitantes_B = vcr_iuvch_B[0][0]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#%%

# Funcion para vector de probabilidades de acompañantes

''' Parametros: 
        Numero de acompañantes del sector
        Distribucion que seguiria las diferentes numero de acompañantes
        Parametros para la distribucion de los acompañantes'''

param_v_sector_A_prob_acom = sim.f_prob_cantidad(dat.n_acomp_A, 'beta', dat.param_acomp_A)
param_v_sector_B_prob_acom = sim.f_prob_cantidad(dat.n_acomp_B, 'beta', dat.param_acomp_B)
param_v_sector_C_prob_acom = sim.f_prob_cantidad(dat.n_acomp_C, 'beta', dat.param_acomp_C)



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Acompoñantes, baños, talleres

acomp_A, baños_A, c_b_A, taller_A, c_t_A = pr.f_ts_costos(param_v_sector_A_prob_acom, visitantes_A, dat.min_acomp_A,
                                         dat.porcentaje_baño, dat.baño_insumo_c,
                                         dat.porcentaje_taller_A, dat.taller_insumo_c)
acomp_B, baños_B, c_b_B, taller_B, c_t_B = pr.f_ts_costos(param_v_sector_B_prob_acom, visitantes_B, dat.min_acomp_B,
                                         dat.porcentaje_baño, dat.baño_insumo_c,
                                         dat.porcentaje_taller_B, dat.taller_insumo_c)
acomp_B, baños_B, c_b_B, taller_B, c_t_B = pr.f_ts_costos(param_v_sector_B_prob_acom, visitantes_B, dat.min_acomp_B,
                                         dat.porcentaje_baño, dat.baño_insumo_c,
                                         dat.porcentaje_taller_B, dat.taller_insumo_c)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -







