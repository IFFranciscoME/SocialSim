
# .. .................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos         .. #
# .. Archivo: visualizaciones.py - procesos de visualizacion de datos                     .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                   .. #
# .. Licencia: Todos los derechos reservados                                              .. #
# .. Repositorio: https://github.com/                                                     .. #
# .. .................................................................................... .. #

import matplotlib.pyplot as plt
# import numpy as np
# import scipy.stats as st
import datos as dat
import simulaciones as sim


# Visualizar las distribuciones propuestas en los parametros para las simulaciones

''' Los parametros para el segmento A se encuentran en dat.param_beta_a
    Es una lista la cual tiene adentro los parametros para cada canal
    por lo tanto len(dat.param_beta_a) es el numero de canales
    Dentro de cada lista (por canal) debe haber minimo 3 vectores (listas) 
    los cuales representan como se simula el prcentaje de los que visitan, 
    regresan (penultimo) y compran (siendo este el ultimo) de determinado canal.
    Cada simulacion con 4 numeros (tambien dado en lista), que representa 'a', 'b'
    es decir, que los dos primeros numeros marcan la forma de la distribucion beta
    'min' y 'max' y estos dos ultimos el rango entre los que se regresará un numero
    de porcentaje para esta simulacion (clicks, visitan, regresan, compran)
    
'''

pb = dat.param_beta_a

''' Primer CANAL de A :  Facebook = dat.param_beta_a[0]
    Este canal cuenta con un embudo de 4 simulaciones, por lo tanto len(dat.param_beta_a[0])
    es igual a 4. Cada uno es parte del embudo de ventas.
    El primero son los clicks de la pagina de Facebook
    esta simulacion tiene la siguiente forma y tiene el supuesto que 
    entre 5% y 7%
'''

# Distribucion de los clicks

param = pb[0][0] # [1.5, 4, 0.05, 0.10]

# Simulaciones con esos parametros
simul = sim.f_simular("beta", {'param1': param[0], 'param2': param[1]},
                      10000, 4, [param[2], param[3]])

# Graficar
plt.hist(simul, bins=100)
plt.title('Porcentaje de personas que dan CLICK (Segmento A - Canal Facebook)')
plt.xlabel('Porcentaje que dan click')
plt.ylabel('Frecuencia')
plt.show()

'''
    La segunda simulacion es la que nos regresa el porcentaje de personas que
    despues de darle click se interesaron y fueron a la casa comunal
'''

# Distribucion de las visitas

param = pb[0][1]  # [4, 2, 0.1, 0.15]

# Simulaciones con esos parametros
simul = sim.f_simular("beta", {'param1': param[0], 'param2': param[1]},
                      10000, 4, [param[2], param[3]])

# Graficar
plt.hist(simul, bins=100)
plt.title('Porcentaje de personas que VISITAN (Segmento A - Canal Facebook)')
plt.xlabel('Porcentaje que visitan')
plt.ylabel('Frecuencia')
plt.show()

'''
    La tercera simulacion regresa el porcentaje de personas que
    regresaria despues de haber ido una para el periodo t+1
'''

# Distribucion de los que regresan

param = pb[0][2]  # [1, 2, 0.1, 0.25]

# Simulaciones con esos parametros
simul = sim.f_simular("beta", {'param1': param[0], 'param2': param[1]},
                      10000, 4, [param[2], param[3]])

# Graficar
plt.hist(simul, bins=100)
plt.title('Porcentaje de personas que REGRESAN (Segmento A - Canal Facebook)')
plt.xlabel('Porcentaje que regresan')
plt.ylabel('Frecuencia')
plt.show()

'''
    La cuarta y ultima simulacion de este canal (facebook) para el segemento A
    es el porcentaje de lo que visitan que comprarian estando en casa comunal
'''

# Distribucion de los que compran
param = pb[0][3]  # [4.5, 1.5, 0.2, 0.55]

# Simulaciones con esos parametros
simul = sim.f_simular("beta", {'param1': param[0], 'param2': param[1]},
                      10000, 4, [param[2], param[3]])

# Graficar
plt.hist(simul, bins=100)
plt.title('Porcentaje de personas que COMPRAN (Segmento A - Canal Facebook)')
plt.xlabel('Porcentaje que compran')
plt.ylabel('Frecuencia')
plt.show()
