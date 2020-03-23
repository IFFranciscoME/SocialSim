
# .. ................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos        .. #
# .. Archivo: datos.py - procesos de obtencion y almacenamiento de datos                 .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                  .. #
# .. Licencia: Todos los derechos reservados                                             .. #
# .. Repositorio: https://github.com/                                                    .. #
# .. ................................................................................... .. #

import numpy as np

# Segmento A: Familias
# segmento_A = 'a'
# Segmento B: Jovenes
# segmento_B = 'b'
# Segmento C: Comuneros
# segmento_C = 'c'

# Presupuesto por mes
publicidad_mensual = 500  # Dinero estimado destiando para publicidad

# Presupuesto para cada segmento '%'
ponderacio_A = 0.75  # Porcentaje que se le designará al segmento A
ponderacio_B = 0.25  # Porcentaje que se le designará al segmento B
# Deben de sumar 1 las ponderaciones por segmento (100%)

# Presupuesto para cada segmento '$'
publicidad_A = publicidad_mensual * ponderacio_A
publicidad_B = publicidad_mensual * ponderacio_B

# Costo por mil impresiones para anuncios en Facebook
cpm_A = 150  # Costo Por Mil impresiones de anuncio: Para anunciarse al segmento A
cpm_B = 100  # Costo Por Mil impresiones de anuncio: Para anunciarse al segmento B

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Mercado accesible por segmento - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# Personas de alcance por canal de facebook
p_canal_facebook_A = int(publicidad_A/cpm_A*1000)
p_canal_facebook_B = int(publicidad_B/cpm_B*1000)

# Personas de alcance por canal de ITESO
alumnos = 10000
egresados = 35000
tiempofijo = 300
tiempovariable = 1100
comunidad_iteso = alumnos + egresados + tiempofijo + tiempovariable
alcance_institucional = 0.02
difusion_iteso = comunidad_iteso*alcance_institucional

# Criterio empirico para proporcion del mercado en la comunidad ITESO
p_canal_iteso_A = round(difusion_iteso*0.75, 0)
p_canal_iteso_B = round(difusion_iteso*0.25, 0)

# Personas de alcance por canal kiosko
p_canal_plaza_A = 200
p_canal_plaza_B = 100

# Cantidad de familias de la CIT, obtenida con el CENSO
segmento_C = 54

# Distribucion de prospectos por segmento por canal
p_total_A = [p_canal_facebook_A, p_canal_iteso_A, p_canal_plaza_A]
p_total_B = [p_canal_facebook_B, p_canal_iteso_B, p_canal_plaza_B]
p_total_C = [segmento_C, segmento_C]

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Productos a la venta - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# cantidad de tipos diferentes de productos que se venderian. Ej: 1) Plantas, 2) Comida
k_n_productos = 2

v_plantas_n = ["planta1", "planta2", "planta3", "planta4"]
v_comidas_n = ["comida1", "comida2", "comida3"]

# Precios de tales productos (en pesos mexicanos)

# Precio unitario de plantas
v_plantas_p = [15, 30, 75, 100]
# Costo unitario de plantas
v_plantas_c = [7.5, 15, 37.5, 50]
# Horas unitarias invertidas por planta vendido
v_plantas_h = [0.5, 1, 1.5, 3]

# Porcentaje de personas que comprarian alguna planta
k_plantas_porcentaje = 0.35
# Costo unitario de insumos comunes contabilizado por planta (en pesos mexicanos)
c_insumo_plantas = 1

# Precio unitario de alimentos y bebidas
v_comidas_p = [10, 30, 60]
# Costo unitario de alimentos y bebidas
v_comidas_c = [5, 7.5, 20]
# Horas unitarias invertidas por alimento o bebida vendido
v_comidas_h = [0.10, 0.15, 0.2]

# Porcentaje de personas que comprarian alguna comida o bebida
k_comidas_porcentaje = 0.65
# Costo unitario de insumos comunes contabilizado por alimento o bebida (en pesos mexicanos)
c_insumo_comida = 5

# Numero de productos totales
k_plantas = len(v_plantas_n)
k_comidas = len(v_comidas_n)

# Maxima cantidad que se estaria dispuesto a comprar
k_max_prod = 3

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Parametros para simulaciones - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - Parametros para las distribuciones de [clicks] visita, regresa, compra

'''
Ejemplo: [1.5, 4, 0.05, 0.07]. Donde:
    1.5 es 'a' para distribucion beta, 
    4 es 'b' para la distribucion beta (ambos parametros cambian la forma de la campana)
    0.05 es el porcentaje minimo que esta simulacion (clicks) arrojaria
    0.07 es el porcentaje maximo de clicks que daria la simulacion
'''

param_beta_a = [
    # Canal 1: Facebook
    [[1.5, 4, 0.05, 0.10], [4, 2, 0.1, 0.15], [1, 2, 0.1, 0.25], [4.5, 1.5, 0.2, 0.55]],
    # Canal 2: Iteso
    [[1.5, 4, 0.05, 0.5], [4, 2, 0.05, 0.15], [1, 2, 0.03, 0.3], [4.5, 1.5, 0.35, 0.75]],
    # Canal 3: Plaza tlajomulco
    [[4, 2, 0.1, 0.2], [1, 2, 0.1, 0.5], [4.5, 1.5, 0.2, 0.45]]
    ]

param_beta_b = [
    # Canal 1: Facebook
    [[1.5, 4, 0.05, 0.07], [4, 2, 0.1, 0.18], [1, 2, 0.1, 0.25], [4.5, 1.5, 0.2, 0.55]],
    # Canal 2: Iteso
    [[1.5, 4, 0.05, 0.5], [4, 2, 0.05, 0.15], [1, 2, 0.03, 0.3], [4.5, 1.5, 0.35, 0.75]],
    # Canal 3: Plaza tlajomulco
    [[4, 2, 0.1, 0.2], [1, 2, 0.1, 0.5], [4.5, 1.5, 0.2, 0.45]]
    ]

param_beta_c = [
    # Venden Plantas
    [[4, 2, 0.2, 0.3], [1, 2, 0.5, 0.85], [4.5, 1.5, 0.2, 0.5]],
    # Venden Comida
    [[4, 2, 0.2, 0.3], [1, 2, 0.5, 0.85], [4.5, 1.5, 0.4, 0.7]]
    ]

# van a asambleas, muestran interes, hacen trabajo comunal

# Parametros para los 16 posibles combinaciones (distribucion beta)
param_comb = [1.5, 2, 0, 1]

# Parametros para la maxima cantidad de productos (distribucion exponencial)
param_cant = [0.31, 0.03]

# Numero de canales
n_canales_a = len(param_beta_a)
n_canales_b = len(param_beta_b)
n_canales_c = len(param_beta_c)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Acompanantes - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - Simulacion de acompanantes por segmento

# Segmento A
# Acompanantes minimos
min_acomp_A = 2
# Acompanantes minimos
max_acomp_A = 5
n_acomp_A = (max_acomp_A - min_acomp_A) + 1
# Parametros para simulacion de acompanantes por segmento_a
param_acomp_A = [1.5, 2.5, 0, 1]

# Segmento B
# Acompanantes minimos
min_acomp_B = 1
# Acompanantes maximos
max_acomp_B = 3
n_acomp_B = (max_acomp_B - min_acomp_B) + 1
# Parametros para simulacion de acompanantes por segmento_b
param_acomp_B = [1.5, 3.5, 0, 1]

# Segmento C
# Acompanantes minimos
min_acomp_C = 2
# Acompanantes maximos
max_acomp_C = 5
n_acomp_C = (max_acomp_C - min_acomp_C) + 1
# Parametros para simulacion de acompanantes por segmento_c
param_acomp_C = [1.5, 2.5, 0, 1]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Sanitarios - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - Simulacion de uso de sanitarios

# Porcentaje del total de personas que visitarian que usarian los sanitarios
porcentaje_bano = 0.20
# Costo de insumos para bano por persona
bano_insumo_c = 1

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Talleres - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - Simulacion de asistena a talleres

# Cantidad de talleres minimos por periodo
n_talleres = 4

# Porcentaje que asistirian por segmento
porcentaje_taller_A = 0.20
porcentaje_taller_B = 0.05
porcentaje_taller_C = 0.30

# Costos de ofrecimiento por taller
# Costo de insumos para taller por asistente
taller_insumo_c = 5
# Costo de realizar taller (pago representativo a expositor)
taller_fijo_c = 100

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Costos Fijos - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - Parametros para los Costos Fijos

# Los siguientes egresos son mensuales
c_f_limpieza_estacionamiento = 100
c_f_limpieza_banos = 500
c_f_limpieza_general = 500
c_f_limpieza_comida = 500
c_f_wifi = 500
c_f_energiaelectrica = 1000
c_f_agua = 300

# Costo total fijo de todos los anteriores
costo_total_fijo = np.array(
    [c_f_limpieza_estacionamiento, c_f_limpieza_banos, c_f_limpieza_general,
     c_f_limpieza_comida, c_f_wifi, c_f_energiaelectrica, c_f_agua, taller_fijo_c]).sum()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Metricas Sociales - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - Consideraciones para simulacion de Metricas Sociales

# 1. Actividad Economica: Horas trabajadas * salario por hora (Salario minimo oficial al 2020)
salario_hora = 16

# 2. Participacion: Horas de plantas + Horas de comidas + Horas de asambleas
horas_asamblea_fam = 0.5

# 3. Educacion Social: Familias asistentes a talleres / total de Familias
total_familias = segmento_C

# 4. Comunicacion: Familias asistentes asambleas + Familias ven el periodico mural
# que no fueron a la asamblea **De las que estan en casa comunal
# (los que no fueron a asamblea) simular cuales sí verían el periodico mural**

porcentaje_familias_van_casa = 0.10
porcentaje_familias_ven_mural = 0.90

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  Metricas Financieras - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Consideraciones para simulacion de Metricas Financieras

# Tasa de descuento
tasa = 0.07

# Inversion inicial
inversion = 1000
