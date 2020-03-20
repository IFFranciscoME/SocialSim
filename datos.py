
# .. .................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos         .. #
# .. Archivo: datos.py - procesos de obtencion y almacenamiento de datos                  .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                   .. #
# .. Licencia: Todos los derechos reservados                                              .. #
# .. Repositorio: https://github.com/                                                     .. #
# .. .................................................................................... .. #

import numpy as np

# Segmento A: Familias
segmento_A = 'a'
# Segmento B: Jovenes
segmento_B = 'b'
# Segmento C: Comuneros
segmento_C = 'c'

# Presupuesto por mes
publicidad_mensual = 500        # Dinero estimado destiando para publicidad

# Presupuesto para cada segmento '%'
ponderacio_A = 0.5              # Porcentaje que se le designará al segmento A
ponderacio_B = 0.5              # Porcentaje que se le designará al segmento B
# Deben de sumar 1 las ponderaciones por segmento (100%)

# Presupuesto para cada segmento '$'
publicidad_A = publicidad_mensual * ponderacio_A
publicidad_B = publicidad_mensual * ponderacio_B

# Costo por mil impresiones para anuncios en Facebook
cpm_A = 50                # Costo para anunciarse con el segmento A
cpm_B = 40                # Costo para anunciarse con el segmento B

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Mercado accesible por segmento

# Personas de alcance por canal de facebook
p_canal_facebook_A = int((publicidad_A / cpm_A)* 1000)
p_canal_facebook_B = int((publicidad_B / cpm_B)* 1000)

# Personas de alcance por canal de iteso
p_canal_iteso_A = 750
p_canal_iteso_B = 940

# Personas de alcance por canal kiosko
p_canal_plaza_A = 200
p_canal_plaza_B = 100

segmento_C = 30

p_total_A = [p_canal_facebook_A, p_canal_iteso_A, p_canal_plaza_A]
p_total_B = [p_canal_facebook_B, p_canal_iteso_B, p_canal_plaza_B]
p_total_C = [segmento_C, segmento_C]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Tipos de productos que se venderian
k_n_productos = 2

v_plantas_n = ["planta1", "planta2", "planta3", "planta4"]
v_comidas_n = ["comida1", "comida2", "comida3"]

# Precios de tales productos

# Plantas
v_plantas_p = [30, 50, 150, 200]
v_plantas_c = [20, 30, 100, 120]
v_plantas_h = [0.5, 1, 2, 3.5]

k_plantas_porcentaje = 0.35
c_insumo_plantas = 1

# Comida
v_comidas_p = [25, 35, 55]
v_comidas_c = [10, 15, 20]
v_comidas_h = [0.15, 0.2, 0.5]

k_comidas_porcentaje = 0.65
c_insumo_comida = 5

# Numero de productos totales
k_plantas = len(v_plantas_n)
k_comidas = len(v_comidas_n)

# Maxima cantidad que se estaria dispuesto a comprar
k_max_prod = 3

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Parametros

# Parametros para distribucion beta, para las distribuciones de [clicks] visita, regresa, compra
'''
Ejemplo: [1.5, 4, 0.05, 0.07]. Donde:
    1.5 es 'a' para distribucion beta, 
    4 es 'b' para la distribucion beta (ambos son los parametros que cambian la forma de la campana)
    0.05 es el porcentaje minimo que esta simulacion (clicks) arrojaria
    0.07 es el porcentaje maximo de clicks que daria la simulacion
'''
param_beta_a = [[[1.5, 4, 0.05, 0.07], [4, 2, 0.1, 0.18], [1, 2, 0.1, 0.25], [4.5, 1.5, 0.2, 0.55]], # Canal 1: Facebook
                [[1.5, 4, 0.05, 0.5], [4, 2, 0.05, 0.15], [1, 2, 0.03, 0.3], [4.5, 1.5, 0.35, 0.75]],    # Canal 2: Iteso
              [[4, 2, 0.1, 0.2], [1, 2, 0.1, 0.5], [4.5, 1.5, 0.2, 0.45]]]      # Canal 3: Plaza tlajomulco

param_beta_b = [[[1.5, 4, 0.05, 0.07], [4, 2, 0.1, 0.18], [1, 2, 0.1, 0.25], [4.5, 1.5, 0.2, 0.55]], # Canal 1: Facebook
                [[1.5, 4, 0.05, 0.5], [4, 2, 0.05, 0.15], [1, 2, 0.03, 0.3], [4.5, 1.5, 0.35, 0.75]],    # Canal 2: Iteso
              [[4, 2, 0.1, 0.2], [1, 2, 0.1, 0.5], [4.5, 1.5, 0.2, 0.45]]]      # Canal 3: Plaza tlajomulco

param_beta_c = [[[4, 2, 0.2, 0.3], [1, 2, 0.5, 0.85], [4.5, 1.5, 0.2, 0.5]], # Venden Plantas
                [[4, 2, 0.2, 0.3], [1, 2, 0.5, 0.85], [4.5, 1.5, 0.4, 0.7]]] # Venden Comida
# van a asambleas, muestran interes, hacen trabajo comunal

# Parametros para los 16 posibles combinaciones (distribucion beta)
param_comb = [1.5, 2, 0, 1]

# Parametros para la maxima cantidad de productos (distribucion exponencial)
param_cant = [0.31, 0.03]

# Numero de canales
n_canales_a = len(param_beta_a)
n_canales_b = len(param_beta_b)
n_canales_c = len(param_beta_c)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Acompañantes

# Segmento A
min_acomp_A = 2
max_acomp_A = 5
n_acomp_A = (max_acomp_A - min_acomp_A) + 1
param_acomp_A = [1.5, 2.5, 0, 1]

# Segmento B
min_acomp_B = 1
max_acomp_B = 3
n_acomp_B = (max_acomp_B - min_acomp_B) + 1
param_acomp_B = [1.5, 3.5, 0, 1]

# Segmento C
min_acomp_C = 2
max_acomp_C = 5
n_acomp_C = (max_acomp_C - min_acomp_C) + 1
param_acomp_C = [1.5, 2.5, 0, 1]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Baño

# Porcentaje del total de personas que visitarian que entrarian al baño
porcentaje_baño = 0.15
# Costo por insumo de bañor
baño_insumo_c = 1

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Talleres
n_talleres = 4

# Porcentaje que asistirian por segmento
porcentaje_taller_A = 0.15
porcentaje_taller_B = 0.05
porcentaje_taller_C = 0.20

# Costos de taller
taller_insumo_c = 10
taller_fijo_c = 100

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Costos Fijos

c_f_limpieza_estacionamiento = 100
c_f_limpieza_baños = 100
c_f_limpieza_general = 100
c_f_limpieza_comida = 100
c_f_wifi = 100
c_f_energiaelectrica = 100
c_f_agua = 100

costo_total_fijo = np.array([c_f_limpieza_estacionamiento, c_f_limpieza_baños, c_f_limpieza_general,
                    c_f_limpieza_comida, c_f_wifi, c_f_energiaelectrica, c_f_agua, taller_fijo_c]).sum()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Metricas Sociales

# 1. Actividad Economica: Horas trabajadas * salario por hora
salario_hora = 16

# 2. Participacion: Horas de plantas + Horas de comidas + Horas de asambleas
horas_asamblea_fam = 0.5

# 3. Educacion Social: Familias asistentes a talleres / total de Familias
total_familias = 30

# 4. Comunicacion: Familias asistentes asambleas + Familias ven el periodico mural que no fueron a la asamblea
# **De las que estan en casa comunal (los que no fueron a asamblea) simular cuales sí verían el periodico mural** 
porcentaje_familias_van_casa = 0.10
porcentaje_familias_ven_mural = 0.90

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Metricas Financieras

# Tasa de descuento
tasa = 0.10
 
# Inversion inicial
inversion = 5000









