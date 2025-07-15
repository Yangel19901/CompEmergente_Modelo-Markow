import pandas as pd
import random 




# Función encargada de recolectar las combinaciones únicas de Temperatura, Condición y Humedad que se encuentra entre los días. 
# Devuelve Estados combinados únicos
# Los Días inicializados, es decir un estado probilidad general
def inicializar_modelo_markov(df_inicial):
    
    #Por cada fila, agarrar los datos que no pertenezca de la columna día
    atributos = [col for col in df_inicial.columns if col != 'Dia']
    
    #Generar una lista donde se guarden las combinaciones unicas de los tres estados que son tomados en cuenta
    estados_observados = []
    for index, row in df_inicial.iterrows():
        estado = tuple(row[atributo] for atributo in atributos)
        estados_observados.append(estado)
    
    
    todos_los_estados_unicos = sorted(list(set(estados_observados)))
    
    print("\nEstados únicos identificados en el historial:")
    for estado in todos_los_estados_unicos:
        print(f"- {estado}")

    #Se crea el Modelo Markov y se observa el numero de estados unicos y se genera 
    modelo_markov_inicial = {}
    num_estados = len(todos_los_estados_unicos)

    if num_estados > 0:
        probabilidad_uniforme = 1.0 / num_estados
    else:
        probabilidad_uniforme = 0 

    for estado_anterior in todos_los_estados_unicos:
        modelo_markov_inicial[estado_anterior] = {}
        for estado_actual in todos_los_estados_unicos:
            modelo_markov_inicial[estado_anterior][estado_actual] = probabilidad_uniforme

    print("\nModelo de Markov inicializado con probabilidades uniformes.")
    return modelo_markov_inicial, todos_los_estados_unicos


# Se encargar aprender probabilidades de Transición entre los estados, es decir, entrenar Markov. 
# Se obtiene un diccionario con todos los estados con las probabilidades posibles
def entrenar_modelo_markov(df_historial, modelo_markov_inicial, todos_los_estados_unicos):
    print("\n--- Iniciando el Entrenamiento del Modelo de Markov ---")

    conteo_transiciones = {}
    for estado_anterior in todos_los_estados_unicos:
        conteo_transiciones[estado_anterior] = {estado_actual: 0 for estado_actual in todos_los_estados_unicos}

    try:
        df_historial_sorted = df_historial.copy()
        df_historial_sorted['Dia'] = pd.to_numeric(df_historial_sorted['Dia'], errors='coerce')
        df_historial_sorted = df_historial_sorted.sort_values(by='Dia').reset_index(drop=True)
    except:
        df_historial_sorted = df_historial.sort_values(by='Dia').reset_index(drop=True)

    atributos_estado = [col for col in df_historial_sorted.columns if col != 'Dia']

    # Se realiza el estudio de trancisiones, revisar los días son continuos y determinar las probailidades
    for i in range(len(df_historial_sorted) - 1):
        dia_actual_valor = df_historial_sorted.loc[i, 'Dia']
        dia_siguiente_valor = df_historial_sorted.loc[i + 1, 'Dia']

        es_consecutivo = False
        try:
            if int(dia_siguiente_valor) == int(dia_actual_valor) + 1:
                es_consecutivo = True
        except ValueError:
            pass 

        if es_consecutivo:
            estado_anterior_valores = tuple(df_historial_sorted.loc[i, atributo] for atributo in atributos_estado)
            estado_actual_valores = tuple(df_historial_sorted.loc[i + 1, atributo] for atributo in atributos_estado)

            if estado_anterior_valores in conteo_transiciones and \
               estado_actual_valores in conteo_transiciones[estado_anterior_valores]:
                conteo_transiciones[estado_anterior_valores][estado_actual_valores] += 1
            else:
                print(f"Advertencia: Transición inesperada o estado no inicializado: {estado_anterior_valores} -> {estado_actual_valores}")

    modelo_markov_entrenado = {}
    for estado_anterior, transiciones in conteo_transiciones.items():
        total_salidas_desde_estado = sum(transiciones.values())
        modelo_markov_entrenado[estado_anterior] = {}
        if total_salidas_desde_estado > 0:
            for estado_actual, conteo in transiciones.items():
                probabilidad = conteo / total_salidas_desde_estado
                modelo_markov_entrenado[estado_anterior][estado_actual] = probabilidad
        else:
            num_estados = len(todos_los_estados_unicos)
            prob_uniforme = 1.0 / num_estados if num_estados > 0 else 0
            for estado_actual in todos_los_estados_unicos:
                modelo_markov_entrenado[estado_anterior][estado_actual] = prob_uniforme

    print("\n--- Modelo de Markov Entrenado ---")
    print("El modelo muestra las probabilidades de transición de un estado (día anterior) a otro estado (día siguiente).")
    print("Formato: Estado_Anterior -> {Estado_Siguiente: Probabilidad}")
    for estado_anterior, transiciones in modelo_markov_entrenado.items():
        print(f"\nDesde: {estado_anterior}")
        for estado_actual, prob in transiciones.items():
            prob = prob*100
            print(f"  -> {estado_actual}: {prob:.1f} %")

    return modelo_markov_entrenado




# Seleccionar una combinación de estados (Temperatura, Condición y Humedad)
def predecir_siguiente_dia_interactivo(df_historial, modelo_markov_entrenado):
    
    
    print("\n--- Predicción del Siguiente Día ---")
    
    if df_historial.empty or not modelo_markov_entrenado:
        print("No hay historial de datos o el modelo de Markov no está entrenado. No se puede predecir.")
        return

    atributos_estado = [col for col in df_historial.columns if col != 'Dia']
    if not atributos_estado:
        print("No hay atributos de estado definidos en el DataFrame para hacer una predicción.")
        return

    estado_actual_input = {}
    print("Por favor, ingrese los valores para el estado actual (día de partida):")

    for col in atributos_estado:
        valores_unicos_columna = df_historial[col].unique().tolist()
        
        while True:
            print(f"\n--- Atributo: '{col}' ---")
            if len(valores_unicos_columna) > 0:
                print(f"Valores existentes para '{col}': {sorted(valores_unicos_columna)}")
            
            valor = input(f"Ingrese el valor para '{col}': ").strip()

            if valor not in valores_unicos_columna and len(valores_unicos_columna) > 0:
                print(f"Advertencia: '{valor}' no es un valor existente para '{col}'.")
                confirm_val = input("¿Desea usar este valor de todos modos? (s/n): ").strip().lower()
                if confirm_val != 's':
                    print("Por favor, ingrese un valor de nuevo.")
                    continue
            estado_actual_input[col] = valor
            break
    
    estado_actual_tupla = tuple(estado_actual_input[col] for col in atributos_estado)

    if estado_actual_tupla in modelo_markov_entrenado:
        posibles_siguientes_estados = modelo_markov_entrenado[estado_actual_tupla]
        
        
        estados_con_probabilidad = {k: v for k, v in posibles_siguientes_estados.items() if v > 0}

        if not estados_con_probabilidad:
            print(f"\nDesde el estado {estado_actual_tupla}, no se han observado transiciones a otros estados en el historial de días consecutivos.")
            print("El modelo no puede hacer una predicción específica para este estado basado en los datos existentes.")
            return

        
        estado_mas_probable = max(estados_con_probabilidad, key=estados_con_probabilidad.get)
        prob_mas_probable = estados_con_probabilidad[estado_mas_probable]
        
        print(f"\n--- Resultados de la Predicción ---")
        print(f"Estado de partida: {estado_actual_tupla}")
        print(f"El estado más probable para el día siguiente es: {estado_mas_probable} (Probabilidad: {prob_mas_probable:.4f})")

        
        estados = list(estados_con_probabilidad.keys())
        probabilidades = list(estados_con_probabilidad.values())
        
       
        if sum(probabilidades) > 0:
            estado_sugerido_probabilistico = random.choices(estados, weights=probabilidades, k=1)[0]
            print(f"Una sugerencia de estado aleatorio basado en las probabilidades es: {estado_sugerido_probabilistico}")
            print("\nConsidera este como una posible evolución, aunque no sea el más probable matemáticamente, podría ocurrir.")
        else:
            print("No se pudo sugerir un estado aleatorio debido a probabilidades nulas.")

        print("\n--- Probabilidades Detalladas ---")
        for siguiente_estado, prob in sorted(estados_con_probabilidad.items(), key=lambda item: item[1], reverse=True):
            prob = prob*100
            print(f"  -> {siguiente_estado}: {prob:.1f}")

    else:
        print(f"El estado '{estado_actual_tupla}' no se encontró como un estado de partida en el modelo de Markov entrenado.")
        print("El modelo no tiene información para predecir desde este estado.")
    

