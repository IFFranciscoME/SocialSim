
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

# Funcion de visitas por segmento, ejemplo del segmento A (un periodo)
''' Parametros: 
        Numero de canales: Facebook y Iteso
        Parametros para las distribuciones de las simulaciones de visitas, regresos, compras
        Numero de personas alcanzadas por segmentos
        Personas que visitaron en el tiempo t-1'''
# Numero de canales
n_canales = 2
# Personas de alcance por canal de facebook
p_canal_facebook = int((dat.publicidad_A / dat.cpm_A)* 1000)
# Personas de alcance por canal de iteso
p_canal_iteso = dat.segmento_A

# 3 resultados: numero de personas que visitan, compran y regresan
v, c, r = pr.f_visitas_segmento(n_canales, dat.param_beta, [p_canal_facebook, p_canal_iteso], [0,0])
#print(v, c, r)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Funcion de serie de tiempo de visitas

''' Parametros: 
        Numero de periodos de la serie de tiempo
        Numero de canales: Facebook y Iteso
        Parametros para las distribuciones de las simulaciones de visitas, regresos, compras
        Numero de personas alcanzadas por segmentos
        Personas que visitaron en el tiempo t-1'''

# Periodos a simular
t = 18
# Resultado de datos visita: [Visitas, Compras, Regresan]
datos_visita = pr.f_serie_tiempo_visitan(t, n_canales, dat.param_beta, [p_canal_facebook, p_canal_iteso])

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

# Funcion de ventas por cada persona
''' Parametros: 
        Matriz de posibles combinaciones (funcion en simulaciones: f_prob_combinaciones)
        Vector de probabilidades por combinacion (f_prob_combinaciones)
        Vector de probabilidades por cantidad (f_prob_cantidad)
        Vector de lista de precios por producto
        Vector de lista de costos por producto'''

ingreso, utilidad, ventas, costos = pr.f_ventas_persona(m_bin_comb, v_prob_comb, v_prob_cant, dat.v_plantas_p, dat.v_plantas_c)
#print(ingreso, utilidad, ventas, costos)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion que da las compras del periodo de todas las personas

''' Parametros:
        Numero de personas en el periodo de tiempo actual,  que se repetira la funcion anterior
        Matriz de posibles combinaciones (funcion en simulaciones: f_prob_combinaciones)
        Vector de probabilidades por combinacion (f_prob_combinaciones)
        Vector de probabilidades por cantidad (f_prob_cantidad)
        Vector de lista de precios por producto
        Vector de lista de costos por producto'''

ing_ut_ven_cos = pr.f_periodo_ventas(c, m_bin_comb, v_prob_comb, v_prob_cant, dat.v_plantas_p, dat.v_plantas_c)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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

ing_ut_ven_cos_18 = pr.f_ventas_total(t, n_canales, dat.param_beta, [p_canal_facebook, p_canal_iteso], # Parametros de f_serie_tiempo_visitan
                           m_bin_comb, v_prob_comb, v_prob_cant, dat.v_plantas_p, dat.v_plantas_c) # Parametros de f_periodo_ventas

print(len(ing_ut_ven_cos_18))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion para vector de probabilidades de acompañantes del sector A

''' Parametros: 
        Numero de acompañantes del sector
        Distribucion que seguiria las diferentes numero de acompañantes
        Parametros para la distribucion de los acompañantes'''

param_v_sector_A_prob_acom = sim.f_prob_cantidad(dat.n_acomp_A, 'beta', dat.param_acomp_A)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion para los acompañantes del sector en un periodo

''' Parametros: 
        Numero de acompañantes del sector
        Distribucion que seguiria las diferentes numero de acompañantes
        Parametros para la distribucion de los acompañantes'''

acompañ_A = sim.f_acompañantes_periodo(param_v_sector_A_prob_acom, int(datos_visita[0][0]), dat.min_acomp_A)
#print(acompañ_A)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion para la cantidad de personas que utilizarian el baño

''' Parametros: 
        Porcentaje que usaría
        Personas del segmento
        Personas que acompañan a las personas del segmento'''

personas_baños = pr.f_prob_binomial(dat.porcentaje_baño, int(datos_visita[0][0]), acompañ_A)
#print(personas_baños)
costo_baños = personas_baños*dat.baño_insumo_c

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Funcion para la cantidad de personas que irian a los talleres

''' Parametros: 
        Porcentaje que usaría
        Personas del segmento
        Personas que acompañan a las personas del segmento'''

personas_taller = pr.f_prob_binomial(dat.porcentaje_taller_A, int(datos_visita[0][0]), acompañ_A)
#print(personas_baños)
costo_baños = personas_taller*dat.taller_insumo_c + dat.taller_fijo_c

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -




