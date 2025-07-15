import pandas as pd

# Se encarga de leer y cargar el archivo csv
def cargar_historial_datos(ruta_archivo_csv):
    
    try:
        df = pd.read_csv(ruta_archivo_csv)
        print(f"Archivo '{ruta_archivo_csv}' cargado exitosamente.")
        return df
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo_csv}' no fue encontrado.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al cargar el archivo CSV: {e}")
        return None


#Se encarga de guardar el DataFrame manejado con Pandas y transformarlo en formato csv y actualizar la data del csv
def guardar_historial_datos(df, ruta_archivo_csv):
    
    try:
        df.to_csv(ruta_archivo_csv, index=False)
        print(f"Datos guardados exitosamente en '{ruta_archivo_csv}'.")
    except Exception as e:
        print(f"Ocurrió un error al guardar el archivo CSV: {e}")





# Eliminar día existente
def eliminar_dia_interactivo(df):
    if df.empty:
        print("El DataFrame está vacío. No hay días para eliminar.")
        return df

    while True:
        try:
            numero_dia_a_eliminar_str = input("Ingrese el número del Día que desea eliminar (o 'salir' para cancelar): ").strip()
            if numero_dia_a_eliminar_str.lower() == 'salir':
                print("Eliminación cancelada.")
                return df
            

            try:
                numero_dia_a_eliminar = int(numero_dia_a_eliminar_str)
            except ValueError:
                numero_dia_a_eliminar = numero_dia_a_eliminar_str 

            fila_a_eliminar = df[df['Dia'] == numero_dia_a_eliminar]

            if fila_a_eliminar.empty:
                print(f"Advertencia: El Día '{numero_dia_a_eliminar}' no se encontró en el historial. Intente de nuevo.")
                continue 
            
            print(f"\n--- Datos del Día {numero_dia_a_eliminar} a eliminar ---")
            print(fila_a_eliminar.to_string(index=False)) 

            confirmacion = input(f"¿Está seguro de que desea eliminar el Día {numero_dia_a_eliminar}? (s/n): ").strip().lower()

            if confirmacion == 's':
                df_actualizado = df[df['Dia'] != numero_dia_a_eliminar].reset_index(drop=True)
                print(f"Día {numero_dia_a_eliminar} eliminado exitosamente.")
                return df_actualizado 
            elif confirmacion == 'n':
                print(f"Eliminación del Día {numero_dia_a_eliminar} cancelada.")
                return df 
            else:
                print("Opción no válida. Por favor, ingrese 's' para sí o 'n' para no.")
        
        except Exception as e:
            print(f"Ocurrió un error inesperado durante la eliminación: {e}")
            return df 




# Buscar entre los días existentes, para editar en las columnas de Temperatura, Condición y Humedad
def editar_dia_interactivo(df):
    
    if df.empty:
        print("El DataFrame está vacío. No hay días para editar.")
        return df

    while True:
        try:
            numero_dia_a_editar = input("Ingrese el número del Día que desea editar (o 'salir' para cancelar): ").strip()
            if numero_dia_a_editar.lower() == 'salir':
                print("Edición cancelada.")
                return df
            
            try:
                numero_dia_a_editar = int(numero_dia_a_editar)
            except ValueError:
                pass 

            fila_a_editar = df[df['Dia'] == numero_dia_a_editar]

            if fila_a_editar.empty:
                print(f"Advertencia: El Día '{numero_dia_a_editar}' no se encontró en el historial. Intente de nuevo.")
                continue
            
            print(f"\n--- Datos actuales del Día {numero_dia_a_editar} ---")
            print(fila_a_editar.drop(columns=['Dia'], errors='ignore').to_string(index=False)) 

            columnas_disponibles = [col for col in df.columns if col != 'Dia']
            if not columnas_disponibles:
                print("No hay columnas editables aparte de 'Dia'.")
                return df

            print("\nColumnas disponibles para editar:")
            for i, col in enumerate(columnas_disponibles):
                print(f"{i+1}. {col}")
            
            while True:
                try:
                    opcion_columna = input("Seleccione el número de la columna a editar (o 'cancelar' para finalizar la edición de este día): ").strip()
                    decision_columna_seleccion = opcion_columna 

                    if decision_columna_seleccion.lower() == "cancelar": 
                        print(f"Edición del Día {numero_dia_a_editar} finalizada.")
                        return df 
                    
                    idx_columna = int(opcion_columna) - 1
                    if 0 <= idx_columna < len(columnas_disponibles):
                        columna_seleccionada = columnas_disponibles[idx_columna]
                        
                        valores_unicos_columna = df[columna_seleccionada].unique().tolist()
                        print(f"Valores existentes para '{columna_seleccionada}': {sorted(valores_unicos_columna)}")
                        
                        nuevo_valor = input(f"Ingrese el nuevo valor para '{columna_seleccionada}': ").strip()
                        
                        if nuevo_valor not in valores_unicos_columna and len(valores_unicos_columna) > 0:
                            print(f"Advertencia: '{nuevo_valor}' no es un valor existente para '{columna_seleccionada}'.")
                            confirm_new_val = input("¿Desea usar este nuevo valor de todos modos? (s/n): ").strip().lower()
                            if confirm_new_val != 's':
                                print("Valor no aplicado. Seleccione otra columna o cancele.")
                                continue 

                        df.loc[df['Dia'] == numero_dia_a_editar, columna_seleccionada] = nuevo_valor
                        print(f"'{columna_seleccionada}' del Día {numero_dia_a_editar} actualizado a '{nuevo_valor}'.")
                        
                        print(f"\n--- Datos actualizados del Día {numero_dia_a_editar} ---")
                        print(df[df['Dia'] == numero_dia_a_editar].drop(columns=['Dia'], errors='ignore').to_string(index=False))
                        
                        otra_columna = input("¿Desea editar otra columna de este día? (s/n): ").lower()
                        if otra_columna != 's':
                            print(f"Edición del Día {numero_dia_a_editar} finalizada.")
                            return df 
                        else:
                            print("\nColumnas disponibles para editar:")
                            for i, col in enumerate(columnas_disponibles):
                                print(f"{i+1}. {col}")
                            continue 

                    else:
                        print("Opción de columna no válida. Intente de nuevo.")
                except ValueError:
                    print("Entrada no válida. Por favor, ingrese un número.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")




# Agregar un día y ordenando el diccionario en orden de menor a mayor según el número del día
# Si existe el día, te da la opción de editarlo
def agregar_dia_interactivo(df):
    
    while True:
        try:
            numero_dia_str = input("Ingrese el número del Nuevo Día (o 'cancelar' para salir): ").strip()
            if numero_dia_str.lower() == 'cancelar':
                print("Adición de día cancelada.")
                return df
            
            try:
                numero_dia = int(numero_dia_str)
            except ValueError:
                numero_dia = numero_dia_str 

            if numero_dia in df['Dia'].values:
                print(f"Advertencia: El Día '{numero_dia}' ya existe en el historial.")
                accion = input("¿Desea editarlo en su lugar (e) o intentar con un nuevo día (n)? (e/n): ").strip().lower()
                if accion == 'e':
                    print("\nRedirigiendo a la edición del día...")
                    return editar_dia_interactivo(df)
                elif accion == 'n':
                    continue 
                else:
                    print("Opción no válida. Por favor, intente de nuevo.")
                    continue
            else:
                break 

        except Exception as e:
            print(f"Ocurrió un error al ingresar el número de día: {e}")
            return df 

    datos_nuevo_dia = {'Dia': numero_dia}
    columnas_a_pedir = [col for col in df.columns if col != 'Dia']

    if not columnas_a_pedir and 'Dia' in df.columns:
        print("El DataFrame solo tiene la columna 'Dia'. No hay otros atributos que agregar.")
        df_actualizado = pd.concat([df, pd.DataFrame([datos_nuevo_dia])], ignore_index=True)
        # --- Modificación: Ordenar el DataFrame ---
        try:
            df_actualizado['Dia'] = pd.to_numeric(df_actualizado['Dia'], errors='coerce')
            df_actualizado = df_actualizado.sort_values(by='Dia').reset_index(drop=True)
        except:
            df_actualizado = df_actualizado.sort_values(by='Dia').reset_index(drop=True)
        print(f"Día {numero_dia} agregado exitosamente con solo la columna 'Dia'.")
        return df_actualizado


    print("\nAhora, ingrese los datos para cada columna del nuevo día:")
    for col in columnas_a_pedir:
        valores_unicos_columna = df[col].unique().tolist()
        
        while True:
            print(f"\n--- Columna: '{col}' ---")
            if len(valores_unicos_columna) > 0:
                print(f"Valores existentes sugeridos: {sorted(valores_unicos_columna)}")
            
            valor_input = input(f"Ingrese el valor para '{col}': ").strip()

            if valor_input not in valores_unicos_columna and len(valores_unicos_columna) > 0:
                print(f"Advertencia: '{valor_input}' no es un valor existente para '{col}'.")
                confirm_new_val = input("¿Desea usar este nuevo valor de todos modos? (s/n): ").strip().lower()
                if confirm_new_val != 's':
                    print("Por favor, ingrese un valor de nuevo.")
                    continue 
            
            datos_nuevo_dia[col] = valor_input
            break 

    
    df_actualizado = pd.concat([df, pd.DataFrame([datos_nuevo_dia])], ignore_index=True)
    
    
    try:
        df_actualizado['Dia'] = pd.to_numeric(df_actualizado['Dia'], errors='coerce')
        df_actualizado = df_actualizado.sort_values(by='Dia').reset_index(drop=True)
    except:
        df_actualizado = df_actualizado.sort_values(by='Dia').reset_index(drop=True)

    print(f"\n--- Día {numero_dia} agregado exitosamente al historial ---")
    print(df_actualizado[df_actualizado['Dia'] == numero_dia].to_string(index=False)) 
    
    return df_actualizado


