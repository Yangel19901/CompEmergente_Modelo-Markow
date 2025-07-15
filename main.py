import pandas as pd
import os 

#Importar las funciones del manejo del CSV y el modelo Markov
from CSV import (
    cargar_historial_datos,
    guardar_historial_datos,
    agregar_dia_interactivo,
    eliminar_dia_interactivo,
    editar_dia_interactivo,
)


from Markov import (
    inicializar_modelo_markov,
    entrenar_modelo_markov,
    predecir_siguiente_dia_interactivo,
)



def mostrar_menu():
   
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Cargar historial de datos (CSV)")
    print("2. Guardar historial de datos (CSV)")
    print("3. Agregar nuevo día al historial")
    print("4. Editar día existente en el historial")
    print("5. Eliminar día del historial")
    print("6. Inicializar modelo de Markov")
    print("7. Entrenar modelo de Markov")
    print("8. Predecir siguiente día con modelo de Markov")
    print("9. Mostrar DataFrame actual")
    print("0. Salir")
    print("----------------------")


#Manejo del menú que interactúa con el usuario
def main():
    
    df_historial = None
    modelo_markov_entrenado = None
    estados_unicos = None # Necesario para inicializar/entrenar el modelo
    ruta_csv = 'datos_clima.csv'

    # Crear un archivo de ejemplo si no existe, para que el usuario pueda empezar
    if not os.path.exists(ruta_csv):
        print(f"El archivo '{ruta_csv}' no existe. Creando un archivo de ejemplo...")
        try:
            with open(ruta_csv, 'w') as f:
                f.write("Dia,Temperatura,Condicion,Humedad\n")
                f.write("1,Calido,Soleado,Baja\n")
                f.write("2,Calido,Soleado,Baja\n")
                f.write("3,Templado,Nublado,Media\n")
                f.write("4,Frio,Lluvia,Alta\n")
                f.write("5,Templado,Nublado,Media\n")
                f.write("6,Calido,Soleado,Baja\n")
                f.write("8,Templado,Nublado,Media\n") # Día 7 falta intencionalmente
                f.write("9,Frio,Lluvia,Alta\n")
            print(f"Archivo de ejemplo '{ruta_csv}' creado exitosamente.")
        except Exception as e:
            print(f"Error al crear el archivo de ejemplo: {e}")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1': 
            df_historial = cargar_historial_datos(ruta_csv)
            if df_historial is not None:
                
                try:
                    df_historial['Dia'] = pd.to_numeric(df_historial['Dia'], errors='coerce')
                    df_historial = df_historial.sort_values(by='Dia').reset_index(drop=True)
                except Exception as e:
                    print(f"Advertencia: No se pudo convertir 'Dia' a numérico para ordenar. Se ordenará como string. Error: {e}")
                    df_historial = df_historial.sort_values(by='Dia').reset_index(drop=True)
                print("\nDataFrame cargado y ordenado por 'Dia'.")
                print(df_historial)
            else:
                print("No se pudo cargar el DataFrame. Por favor, asegúrese de que el archivo CSV exista y sea válido.")
                
        elif opcion == '2': 
            if df_historial is not None:
                guardar_historial_datos(df_historial, ruta_csv)
            else:
                print("No hay historial cargado para guardar.")

        elif opcion == '3': # Agregar día
            if df_historial is not None:
                df_historial = agregar_dia_interactivo(df_historial)
                modelo_markov_entrenado = None 
                estados_unicos = None
                print("\nRecuerda inicializar y entrenar el modelo de Markov de nuevo después de modificar el historial.")
            else:
                print("Por favor, cargue el historial de datos primero (Opción 1).")

        elif opcion == '4': # Editar día
            if df_historial is not None:
                df_historial = editar_dia_interactivo(df_historial)
                modelo_markov_entrenado = None 
                estados_unicos = None
                print("\nRecuerda inicializar y entrenar el modelo de Markov de nuevo después de modificar el historial.")
            else:
                print("Por favor, cargue el historial de datos primero (Opción 1).")

        elif opcion == '5': 
            if df_historial is not None:
                df_historial = eliminar_dia_interactivo(df_historial)
                # Reinicializar y reentrenar modelo si se modifica el DF
                modelo_markov_entrenado = None 
                estados_unicos = None
                print("\nRecuerda inicializar y entrenar el modelo de Markov de nuevo después de modificar el historial.")
            else:
                print("Por favor, cargue el historial de datos primero (Opción 1).")

        elif opcion == '6': # Inicializar modelo
            if df_historial is not None:
                modelo_markov_entrenado = None # Asegurarse de que se reinicializa
                modelo_inicial, estados_unicos = inicializar_modelo_markov(df_historial)
                print("\nModelo de Markov inicializado. Ahora puedes entrenarlo (Opción 7).")
            else:
                print("Por favor, cargue el historial de datos primero (Opción 1).")
        
        elif opcion == '7': # Entrenar modelo
            if df_historial is not None:
                # Siempre inicializar justo antes de entrenar para asegurar la estructura base correcta
                # 'modelo_base_para_entrenar' recibirá el DICCIONARIO del modelo inicial.
                # 'estados_unicos' (la variable global) recibirá la LISTA DE TUPLAS de estados.
                modelo_base_para_entrenar, estados_unicos = inicializar_modelo_markov(df_historial)
                
                # Ahora, pasamos el diccionario del modelo base y la lista de tuplas de estados
                modelo_markov_entrenado = entrenar_modelo_markov(df_historial, modelo_base_para_entrenar, estados_unicos)
                print("\nModelo de Markov entrenado exitosamente. Ahora puedes predecir (Opción 8).")
            else:
                print("Por favor, cargue el historial de datos primero (Opción 1).")

        elif opcion == '8': 
            if modelo_markov_entrenado is not None and df_historial is not None:
                predecir_siguiente_dia_interactivo(df_historial, modelo_markov_entrenado)
            else:
                print("Por favor, entrene el modelo de Markov primero (Opción 7) y asegúrese de tener el historial cargado.")

        elif opcion == '9':
            if df_historial is not None:
                print("\n--- DataFrame Actual ---")
                print(df_historial)
            else:
                print("No hay historial de datos cargado.")

        elif opcion == '0': 
            print("Saliendo del programa. ¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
        
        input("\nPresione Enter para continuar...") 

if __name__ == "__main__":
    main()