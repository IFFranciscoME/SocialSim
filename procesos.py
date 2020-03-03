
# .. .................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos         .. #
# .. Archivo: procesos.py - funciones de procesamiento general de datos                   .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                   .. #
# .. Licencia: Todos los derechos reservados                                              .. #
# .. Repositorio: https://github.com/                                                     .. #
# .. .................................................................................... .. #

import numpy as np

# Este es un caso particular, se tiene que tener un codigo que lo generalice
m_matriz_c = np.array([[0, 0, 0],
                       [0, 0, 1],
                       [0, 1, 0],
                       [0, 1, 1],
                       [1, 0, 0],
                       [1, 0, 1],
                       [1, 1, 0],
                       [1, 1, 1]], np.int64)

# Este es un caso particular, se tiene que tener un codigo que lo generalice
v_matrix_prob = [0.06, 0.08, 0.12, 0.18, 0.24, 0.17, 0.09, 0.06]
# -- La suma debe de ser 1
sum(v_matrix_prob)

# referencias
# https://docs.scipy.org/doc/scipy/reference/tutorial/stats/discrete.html
# https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.beta.html
