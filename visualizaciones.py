
# .. .................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos         .. #
# .. Archivo: visualizaciones.py - procesos de visualizacion de datos                     .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                   .. #
# .. Licencia: Todos los derechos reservados                                              .. #
# .. Repositorio: https://github.com/                                                     .. #
# .. .................................................................................... .. #
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
from datos import param_beta

pb = param_beta[0]
# Visualizar las distribuciones propuestas

# Distribucion de los clicks
# [1.5, 4, 0, 0.1]
param = pb[0]
x = np.arange(-0.01,0.15,0.01)
pdf= st.beta.pdf(x, *param[:-2], loc=param[-2], scale=param[-1])
plt.plot(x, pdf)
plt.show()

# Distribucion de las visitas
# [4, 2, 0, 0.2]
param = pb[1]
x = np.arange(-0.01,0.25,0.01)
pdf= st.beta.pdf(x, *param[:-2], loc=param[-2], scale=param[-1])
plt.plot(x, pdf)
plt.show()

# Distribucion de los que regresan
# [1, 2, 0, 0.05]
param = pb[2]
x = np.arange(-0.01,0.06,0.01)
pdf= st.beta.pdf(x, *param[:-2], loc=param[-2], scale=param[-1])
plt.plot(x, pdf)
plt.show()

# Distribucion de los que compran
# [4.5, 1.5, 0.2, 0.55]
param = pb[3]
x = np.arange(-0.01,0.85,0.01)
pdf= st.beta.pdf(x, *param[:-2], loc=param[-2], scale=param[-1])
plt.plot(x, pdf)
plt.show()

# Serie de tiempo de compras, una simulacion
from principal import datos_visita_A, t
x = np.arange(t)
y = datos_visita_A[1]

plt.plot(x, y)
plt.show()