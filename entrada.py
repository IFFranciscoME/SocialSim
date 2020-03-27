
# .. ................................................................................... .. #
# .. Proyecto: SocialSim - Plataforma de simulacion de proyectos socioproductivos        .. #
# .. Archivo: entrada.py - diccionario con datos de entrada                              .. #
# .. Desarrolla: ITERA LABS, SAPI de CV                                                  .. #
# .. Licencia: Todos los derechos reservados                                             .. #
# .. Repositorio: https://github.com/                                                    .. #
# .. ................................................................................... .. #

SocialSim = {'simulaciones': {'periodos': 24, 'cantidad': 10000,
                              'tendencias': {'segmento_a': 0.65,
                                             'segmento_b': 0.65,
                                             'segmento_c': 0.70}},
             'motor_crecimiento': {'pres_pub_mens': 500,
                                   'cpm': {'segmento_a': 100, 'segmento_b': 100}},
             'canal_ITESO': {'subsegmentos': {'alumnos': 10000, 'egresados': 35000,
                                              'tiempofijo': 300, 'tiempovariable': 1100},
                             'alcance_inst': 0.02},
             'canal_KIOSKO': {'subsegmentos': {'segmento_a': 200, 'segmento_b': 100}},
             'canal_ASAMBLEAS': {'subsegmentos': {'segmento_c': 214}},
             'productos': {'cantidad_en_venta': 2,
                           'producto_tipo1': {'nombre_de_tipo': 'plantas',
                                              'porcentaje_compran': 0.45,
                                              'insumos_por_producto': 1.50,
                                              'lista_nombres': ["planta1", "planta2",
                                                                 "planta3", "planta4",
                                                                 "planta5"],
                                              'lista_precios': [55, 45, 90, 95, 120],
                                              'lista_costos': [16.5, 13.5, 27, 28.5, 36],
                                              'lista_hrs_trabajo': [0.50, 1.0, 1.5, 2.0, 3.0]},

                           'producto_tipo2': {'nombre_de_tipo': 'alimentos',
                                              'porcentaje_compran': 0.70,
                                              'insumos_por_producto': 2.50,
                                              'lista_nombres': ["comida1", "comida2",
                                                                "comida3", "comida4"],
                                              'lista_precios': [10, 30, 90, 130],
                                              'lista_costos': [4, 12, 36, 52],
                                              'lista_hrs_trabajo': [0.10, 0.10, 0.15, 0.2]}},
             'distribuciones': {
                 'segmento_a': [[
                     # Canal 1: Facebook
                     [1.5, 4, 0.05, 0.10], [4, 2, 0.10, 0.20],
                     [1, 2, 0.15, 0.45], [4.5, 1.5, 0.55, 0.70]], [
                     # Canal 2: Iteso
                     [1.5, 4, 0.05, 0.5], [4, 2, 0.05, 0.15],
                     [1, 2, 0.45, 0.65], [4.5, 1.5, 0.65, 0.70]], [
                     # Canal 3: Plaza tlajomulco
                     [4, 2, 0.1, 0.2], [1, 2, 0.10, 0.25],
                     [4.5, 1.5, 0.25, 0.60]]],
                 'segmento_b': [[
                     # Canal 1: Facebook
                     [1.5, 4, 0.05, 0.07], [4, 2, 0.10, 0.18],
                     [1, 2, 0.15, 0.35], [4.5, 1.5, 0.55, 0.70]], [
                     # Canal 2: Iteso
                     [1.5, 4, 0.05, 0.5], [4, 2, 0.05, 0.15],
                     [1, 2, 0.35, 0.55], [4.5, 1.5, 0.60, 0.70]], [
                     # Canal 3: Plaza tlajomulco
                     [4, 2, 0.10, 0.20], [1, 2, 0.15, 0.25],
                     [4.5, 1.5, 0.25, 0.45]]],
                 'segmento_c': [[
                     # Venden Plantas
                     [4, 2, 0.20, 0.40], [1, 2, 0.05, 0.15],
                     [4.5, 1.5, 0.07, 0.15]], [
                     # Venden Comida
                     [4, 2, 0.20, 0.40], [1, 2, 0.05, 0.10],
                     [4.5, 1.5, 0.05, 0.10]]]}
             }
