
# .. ................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos        .. #
# .. Archivo: visualizaciones.py - procesos de visualizacion de datos                    .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                  .. #
# .. Licencia: Todos los derechos reservados                                             .. #
# .. Repositorio: https://github.com/                                                    .. #
# .. ................................................................................... .. #

import datos as dat
import simulaciones as sim

import plotly.graph_objs as go
import plotly.io as pio
pio.renderers.default = "browser"


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - VISUALIZACION: HISTOGRAMA - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion para generar una grafica de histograma

def g_histograma(param_val, param_colores, param_etiquetas):
    """

    Parameters
    ----------
    param_val :
    param_colores :
    param_etiquetas :

    Returns
    -------

    Debugging
    -------

    """

    # Inicializar un objeto tipo figura
    fig = go.Figure()

    # Agregar un trazo tipo histograma 1
    fig.add_trace(go.Histogram(x=param_val, histnorm='probability',
                               marker_color=param_colores['serie_1'],
                               hovertemplate='<i>Probabilidad</i>: %{y} '
                                             '<br><b> Rango de % de personas </b>: %{x} <br>'))

    # Actualizar el layout de titulos y ejes
    fig.update_layout(title=dict(x=0.5, text=param_etiquetas['titulo']),
                      xaxis=dict(title_text=param_etiquetas['ejex']),
                      yaxis=dict(title_text=param_etiquetas['ejey']),
                      bargap=0.01)

    # Al hacer hover o "mouse over" en las barras que se trunque a 2 decimales
    # en los numeros y expersarlo en %
    fig.update_yaxes(hoverformat='%.2f')
    # Al hacer hover o "mouse over" en las barras que se trunque a 2 decimales en los numeros
    fig.update_xaxes(hoverformat=".2f")
    # Overlay both histograms
    fig.update_layout(barmode='relative')
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.5)
    # mostrar plot
    # fig.show()

    return fig


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - VISUALIZACION: SERIES DE TIEMPO - #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# - - Funcion para generar una grafica de visualizaciones de N series de tiempo

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
param = pb[0][0]  # [1.5, 4, 0.05, 0.10]

# Simulaciones con esos parametros
sim_1 = sim.f_simular("beta", {'param1': param[0], 'param2': param[1]}, 10000, 4,
                      [param[2], param[3]])


colores_1 = {'serie_1': '#047CFB', 'serie_2': '#42c29b', 'serie_3': '#6B6B6B'}
etiquetas_1 = {'titulo': '<b> Distribuciones de personas que hacen click </b>',
               'ejex': '% de personas', 'ejey': 'probabilidad'}

sim_1_fig = g_histograma(param_val=sim_1, param_colores=colores_1, param_etiquetas=etiquetas_1)


'''
    La segunda simulacion es la que nos regresa el porcentaje de personas que
    despues de darle click se interesaron y fueron a la casa comunal
'''

# Distribucion de las visitas
param = pb[0][1]  # [4, 2, 0.1, 0.15]

# Simulaciones con esos parametros
sim_2 = sim.f_simular("beta", {'param1': param[0], 'param2': param[1]}, 10000, 4,
                      [param[2], param[3]])

colores_2 = {'serie_1': '#047CFB', 'serie_2': '#42c29b', 'serie_3': '#6B6B6B'}
etiquetas_2 = {'titulo': '<b> Distribucion de personas que visitan </b>',
               'ejex': '% de personas', 'ejey': 'probabilidad'}

sim_2_fig = g_histograma(param_val=sim_2, param_colores=colores_2, param_etiquetas=etiquetas_2)

'''
    La tercera simulacion regresa el porcentaje de personas que
    regresaria despues de haber ido una para el periodo t+1
'''

# Distribucion de los que regresan
param = pb[0][2]  # [1, 2, 0.1, 0.25]

# Simulaciones con esos parametros
sim_3 = sim.f_simular("beta", {'param1': param[0], 'param2': param[1]}, 10000, 4,
                      [param[2], param[3]])

colores_3 = {'serie_1': '#047CFB', 'serie_2': '#42c29b', 'serie_3': '#6B6B6B'}
etiquetas_3 = {'titulo': '<b> Distribucion de personas que regresan </b>',
               'ejex': '% de personas', 'ejey': 'probabilidad'}

sim_3_fig = g_histograma(param_val=sim_3, param_colores=colores_3, param_etiquetas=etiquetas_3)

'''
    La cuarta y ultima simulacion de este canal (facebook) para el segemento A
    es el porcentaje de lo que visitan que comprarian estando en casa comunal
'''

# Distribucion de los que compran
param = pb[0][3]  # [4.5, 1.5, 0.2, 0.55]

# Simulaciones con esos parametros
sim_4 = sim.f_simular("beta", {'param1': param[0], 'param2': param[1]}, 10000, 4,
                      [param[2], param[3]])

colores_4 = {'serie_1': '#047CFB', 'serie_2': '#42c29b', 'serie_3': '#6B6B6B'}
etiquetas_4 = {'titulo': '<b> Distribucion de personas que compran </b>',
               'ejex': '% de personas', 'ejey': 'probabilidad'}

sim_4_fig = g_histograma(param_val=sim_4, param_colores=colores_4, param_etiquetas=etiquetas_4)
