
# .. .................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos         .. #
# .. Archivo: datos.py - procesos de obtencion y almacenamiento de datos                  .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                   .. #
# .. Licencia: Todos los derechos reservados                                              .. #
# .. Repositorio: https://github.com/                                                     .. #
# .. .................................................................................... .. #

# Mercado accesible por segmento
segmento_A = 10800         # Segmento A: Familias
segmento_B = 9000          # Segmento B: Jovenes

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
cpm_A = 10                # Costo para anunciarse con el segmento A
cpm_B = 10                # Costo para anunciarse con el segmento B

# Tipos de productos que se venderian
v_plantas_n = ["planta1", "planta2", "planta3", "planta4"]

# Precios de tales productos
v_plantas_p = [30, 50, 150, 200]
v_plantas_c = [20, 30, 100, 120]

# Numero de productos totales
k_plantas = len(v_plantas_n)

# Maxima cantidad que se estaria dispuesto a comprar
k_max_prod = 3

# Parametros

# Parametros para distribucion beta, para las distribuciones de [clicks] visita, regresa, compra
param_beta = [[[1.5, 4, 0, 0.1], [4, 2, 0, 0.2], [1, 2, 0, 0.05], [4.5, 1.5, 0.2, 0.55]], # Canal 1
                [[4, 2, 0, 0.1], [1, 2, 0, 0.05], [4.5, 1.5, 0.2, 0.35]]]      # Canal 2

# Parametros para los 16 posibles combinaciones (distribucion beta)
param_comb = [1.5, 2, 0, 1]

# Parametros para la maxima cantidad de productos (distribucion exponencial)
param_cant = [0.31, 0.03]


