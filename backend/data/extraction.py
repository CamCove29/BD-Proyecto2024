import pandas as pd

# Tamaños de datos a procesar
data_size = [1000, 2000, 4000, 8000, 16000, 32000, 64000]
for i in data_size:
    # Ruta del archivo CSV original
    input_file_path = r"C:\Users\Camila\Downloads\BD-Proyecto2024\backend\data\spotify_songs.csv"

    # Ruta para el nuevo archivo CSV con el tamaño especificado
    output_file_path = rf"C:\Users\Camila\Downloads\BD-Proyecto2024\backend\data\spotify_songs_{i}.csv"

    # Leer las primeras i filas del archivo CSV original
    df = pd.read_csv(input_file_path, nrows=i)

    # Seleccionar las columnas necesarias
    df_selected = df[['track_id', 'track_name', 'track_artist', 'track_album_name', 'lyrics']]

    # Guardar los datos seleccionados en un nuevo archivo CSV
    df_selected.to_csv(output_file_path, index=False)

    print(f"Archivo CSV creado con {i} filas en: {output_file_path}")



