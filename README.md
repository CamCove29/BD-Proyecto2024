# BD-Proyecto2024
  - [Introducción](#introducción)
    - [Objetivo del Proyecto](#objetivo-del-proyecto)
    - [Descripción del Dataset](#descripción-del-dataset)
    - [Importancia de Aplicar Indexación](#importancia-de-aplicar-indexación)
  - [Backend: Índice Invertido](#backend-índice-invertido)
    - [Construcción del Índice Invertido en Memoria Secundaria](#construcción-del-índice-invertido-en-memoria-secundaria)
    - [Ejecución Óptima de Consultas Aplicando Similitud de Coseno](#ejecución-óptima-de-consultas-aplicando-similitud-de-coseno)
  - [Índice Invertido en PostgreSQL](#índice-invertido-en-postgresql)
    - [Creación de la Tabla](#creación-de-la-tabla)
    - [Carga de Datos](#carga-de-datos)
    - [Creación de Columnas para Vectores de Texto Ponderados](#creación-de-columnas-para-vectores-de-texto-ponderados)
    - [Actualización de Columnas con Valores Ponderados](#actualización-de-columnas-con-valores-ponderados)
    - [Creación del Índice GIN](#creación-del-índice-gin)
    - [Consultas de Búsqueda de Texto Completo](#consultas-de-búsqueda-de-texto-completo)
  - [Ejecución de Consultas en PostgreSQL](#ejecución-de-consultas-en-postgresql)
  - [Frontend](#frontend)
    - [Diseño de la GUI](#diseño-de-la-gui)
      - [Al crear el índice invertido](#al-crear-el-índice-invertido)
      - [Después de crear el índice invertido](#después-de-crear-el-índice-invertido)
    - [Mini-manual de Usuario](#mini-manual-de-usuario)
      - [Al crear el índice invertido](#al-crear-el-índice-invertido-1)
      - [Al realizar una consulta](#al-realizar-una-consulta)
    - [Screenshots de la GUI](#screenshots-de-la-gui)
      - [Creación del Índice Invertido](#creación-del-índice-invertido)
      - [Consulta de Texto Libre](#consulta-de-texto-libre)
    - [Análisis Comparativo Visual con Otras Implementaciones](#análisis-comparativo-visual-con-otras-implementaciones)
  - [Experimentación](#experimentación)
    - [Tablas y Gráficos de los Resultados Experimentales](#tablas-y-gráficos-de-los-resultados-experimentales)
      - [Tiempo de Creación del Índice Invertido](#tiempo-de-creación-del-índice-invertido)
      - [Tiempo de Ejecución de Consultas (Top-K = 10)](#tiempo-de-ejecución-de-consultas-top-k--10)
    - [Análisis y Discusión](#análisis-y-discusión)
  - [Ejecución del Proyecto](#ejecución-del-proyecto)
    - [Backend](#backend)
    - [Frontend](#frontend)
  - [Autores](#autores)
  - [Referencias](#referencias)

## Introducción
### Objetivo del Proyecto
Este proyecto está enfocado en desarrollar un proyecto integral de base de datos que soporte tanto el modelo relacional basado en tablas como técnicas avanzadas de recuperación de información basadas en el contenido de documentos textuales y objetos multimedia. 

![image](https://github.com/user-attachments/assets/6e632e19-a646-4e2b-9a05-3150b073720d)
### Descripción del Dataset
El dataset se encuentra en el Kaggle(https://www.kaggle.com/datasets/imuhammad/audio-features-and-lyrics-of-spotify-songs) y tiene mas de 18000 canciones de Spotify incluyendo, artista, álbum, características de audio, letras, el lenguaje de la letra, géneros y subgénero. 
| Variable               | Class       | Descripción                                                                                         |
|------------------------|-------------|-----------------------------------------------------------------------------------------------------|
| `track_id`            | character   | ID único de la canción                                                                              |
| `track_name`          | character   | Nombre de la canción                                                                               |
| `track_artist`        | character   | Artista de la canción                                                                              |
| `lyrics`              | character   | Letras de la canción                                                                               |
| `track_popularity`    | double      | Popularidad de la canción (0-100), donde un valor más alto indica mayor popularidad                |
| `track_album_id`      | character   | ID único del álbum                                                                                 |
| `track_album_name`    | character   | Nombre del álbum                                                                                   |
| `track_album_release_date` | character   | Fecha de lanzamiento del álbum                                                                    |
| `playlist_name`       | character   | Nombre de la playlist                                                                              |
| `playlist_id`         | character   | ID de la playlist                                                                                  |
| `playlist_genre`      | character   | Género de la playlist                                                                              |
| `playlist_subgenre`   | character   | Subgénero de la playlist                                                                           |
| `danceability`        | double      | Nivel de aptitud para bailar (0.0 a 1.0), donde valores más altos indican mayor facilidad para bailar |
| `energy`              | double      | Intensidad y actividad (0.0 a 1.0), valores más altos indican mayor energía                        |
| `key`                 | double      | Tono general estimado de la canción, basado en la notación de Clase de Tonos                      |
| `loudness`            | double      | Sonoridad promedio de la canción en decibelios (dB)                                               |
| `mode`                | double      | Modalidad de la canción: 1 para mayor, 0 para menor                                               |
| `speechiness`         | double      | Presencia de palabras habladas (0.0 a 1.0), valores altos indican más parecido al habla           |
| `acousticness`        | double      | Confianza (0.0 a 1.0) de que la canción es acústica                                               |
| `instrumentalness`    | double      | Probabilidad (0.0 a 1.0) de que la canción no tenga voces                                         |
| `liveness`            | double      | Probabilidad (0.0 a 1.0) de que la canción sea en vivo, valores altos indican grabaciones en vivo |
| `valence`             | double      | Positividad (0.0 a 1.0), valores altos indican un sonido más alegre                              |
| `tempo`               | double      | Tempo estimado en pulsaciones por minuto (BPM)                                                   |
| `duration_ms`         | double      | Duración de la canción en milisegundos                                                           |
| `language`            | character   | Idioma de las letras de la canción                                                                |

### Importancia de Aplicar Indexación
La indexación es clave para organizar grandes volúmenes de datos y mejorar la eficiencia en la recuperación de información. Permite realizar búsquedas rápidas y precisas, optimizando consultas complejas como filtrar por popularidad, género o artista. Esto es especialmente útil en sistemas con millones de registros, ya que reduce tiempos de respuesta, mejora el rendimiento y facilita análisis en tiempo real, como recomendaciones personalizadas o tendencias

## Backend: Índice Invertido
### Construcción del Índice Invertido en Memoria Secundaria
![image](https://github.com/user-attachments/assets/621015f2-05ae-4c81-bd98-f80afe7d273c)

Se implementó un índice invertido en almacenamiento secundario mediante el uso del algoritmo SPIMI (Single-Pass In-Memory Indexing). Este enfoque divide la construcción del índice en dos etapas fundamentales: primero, la construcción de bloques, y luego, la fusión de dichos bloques. En la fase de construcción de bloques, se procesan los datos de manera eficiente en memoria, creando fragmentos temporales del índice. Posteriormente, en la fase de fusión, estos bloques se combinan para generar un índice global coherente, optimizando tanto el uso de memoria como el rendimiento en la creación del índice invertido.
1. **Comienzo**:
   - Cargamos el dataset que tendrán las letras de canciones y la información adicional de los mismos.
   - Definimos el tamaño de los bloques, el directorio temporal para almacenar los índices parciales y el archivo final donde se guardará el índice invertido completo.
2. **Procesamiento del Texto**:
   - Tokenización: Divide el texto en palabras individuales (tokens)
   - Eliminacion de Stopwords: Eliminar palabras comunes que no aportann un significado significativo. También se eliminara los signos de puntuación
   - Stemming: reduce cada palabra a su raiz, dependiendo del idioma en el que se ecuentra, español o inglés.
3. **Procesamiento en Bloques**:
   - Los docuemntos se procesan en bloques que tiene un tamaña predefinido.
   - Por cada bloque, se crea un diccionario temporal donde cada palabra se asocia a una lista de documentos en los que aparece junto con su frecuencia de aparición.
4. **Almacenamiento Temporal**:
   - Cada bloque es guardado como un archivo temporal en el directorio designado.
   - Los archivos temporales contineen el directorio de términos y las normas de los documentos correspondientes al bloque.
5. **Fusión de Bloques**:
   - Los archivos temporales se cargan y se juntan en un solo índice invertido.
   - Utilizamos una estructura de datos de tipo heap para ordenar y combinar las listas de postings de cada término de los diferentes bloques.
   - Las normas de los documentos se calcularán al final de todo antes de terminar de hacer el merge.
6. **índice Final**:
   - El índice invertido final, que tienen los términos, las listas de los documentos asociados y las normas de los documentos, se guarda en un archivo en la memoria secundaria

### Ejecución Óptima de Consultas Aplicando Similitud de Coseno
1. **Preprocesamiento de la Consulta**:
   - La consulta ingresada por el usuario se tokeniza, se eliminan los atopwprds y se aplica stemming, siguiendo el mismo proceso que para los documentos.
2. **Cáculo de pesos TF-IDF para la consulta**:
   - Se calcula el peso TF-IDF para cada término de la consulta.
     - TF (Term Frequency): es la frecuencia del término de la consulta
     - IDF(Inverse Document Frequency): se calcula en función de la cantidad de documentos en los que aparece el término
3. **Normalización del Vector de la Consulta**:
   - Se calcula la norma del vector de la consulta para normalizar los pesos TF-IDF
4. **Cálculo de Similitud de Cosenos**:
   - Para cada término en la consulta se busca en el pindice invertido los documentis que contienen el término
   - Calculamos la similitud de coseno entre la consulta y cada documento relevante. Luego miltiplicamos los pesos TF-IDF del término de la consulta y la del documento, y dividiendo por el producto de las normas de los vectores del documento y la consulta.
5. **Ranking de Documentos**:
   - Los documentos se ordenan en función de la similitud del coseno calculada (mayor a menor).
   - Seleccionamos los documentos de mayor similitud para formar el Top-K resultados.
6. **Presentación de Resultados**:
   - Se mostrará los documentos mas relevantes, incluyendo información como el nombre de la pista, el artista y la similitud del coseno. Además se procesará el tiempo total que tomó procesar la consulta.

Así garantizaremos que las consultas esten ejecutadas de manera eficiente y que los documentos mas relevantes se recuperen y se presenten al usuario.

### Índice Invertido en PostgresSQL
PostgresSQL es un sistema de gestión de bases de datos relacional que ofrece funciones avanzadas para realizar búsquedas de texto completo de manera eficiente. Esto se logra usando los índces GIN(Generalized Inverted Index), posteriormente explicamos cómo se implementa un índice de busqueda optimizada en PostgreSQL y como se realiza la búsqueda de texto completo utilizando este índice:
1. **Creación de Tabla**:
   - Crear la tabla `songs` que almacenan las canciones con sus respectivos datos y letras.
   - Se definen las columnas necesarias para almacenar los datos 
   ```sql
   DROP TABLE IF EXISTS songs;
   CREATE TABLE songs (
       track_id TEXT PRIMARY KEY,
       track_name TEXT,
       track_artist TEXT NULL,
       track_album_name TEXT,
       lyrics TEXT
   );
   ```
2. **Carga de Datos:**:
   - Se cargan los datos del archivo CSV a la tabla `songs`:
   ```sql
   COPY Public."songs" FROM 'PROYECTO-BD2/backend/csv/spotify_songs.csv' DELIMITER ',' CSV HEADER;
   ```
3. **Creación de Columnas para Vectores de Texto Ponderados**:
   - Se añaden nuevas columnas `weighted_tsv` y `weighted_tsv2` a la tabla `songs` para almacenar los vectores de texto ponderados.

   ```sql
   ALTER TABLE songs ADD COLUMN weighted_tsv tsvector;
   ALTER TABLE songs ADD COLUMN weighted_tsv2 tsvector;
   ```

4. **Actualización de Columnas con Valores Ponderados**:
   - Se actualizan las columnas `weighted_tsv` y `weighted_tsv2` con valores ponderados usando las funciones `setweight` y `to_tsvector`. Estas funciones asignan pesos a diferentes partes del texto (por ejemplo, mayor peso a los nombres de las pistas y menor peso a las letras).

   ```sql
   UPDATE songs SET
   weighted_tsv = x.weighted_tsv,
   weighted_tsv2 = x.weighted_tsv
   FROM (
       SELECT track_id,
       setweight(to_tsvector('english', COALESCE(track_name,'')), 'A') ||
       setweight(to_tsvector('english', COALESCE(lyrics,'')), 'B')
       AS weighted_tsv
       FROM songs
   ) AS x
   WHERE x.track_id = songs.track_id;
   ```

5. **Creación del Índice GIN**:
   - Se crea un índice GIN en la columna `weighted_tsv2` para optimizar las consultas de búsqueda de texto completo.

   ```sql
   CREATE INDEX weighted_tsv_idx1e3 ON songs USING GIN (weighted_tsv2);
   ```

6. **Consultas de Búsqueda de Texto Completo**:
   - Se realizan consultas de búsqueda de texto completo utilizando el operador `@@` y la función `ts_rank_cd` para calcular la relevancia de los documentos.
   - La consulta se ejecuta primero sin el índice para comparar el rendimiento, y luego con el índice para optimizar la búsqueda.

   ```sql
   -- Sin índice:
   vacuum analyze;
   EXPLAIN ANALYZE
   SELECT track_id, track_name, ts_rank_cd(weighted_tsv, query) AS rank
   FROM songs, to_tsquery('english', 'imagination') query
   WHERE query @@ weighted_tsv
   ORDER BY rank DESC
   LIMIT 8;

   -- Con índice:
   ANALYZE songs;
   SET enable_seqscan = OFF;
   EXPLAIN ANALYZE
   SELECT track_id, track_name, ts_rank_cd(weighted_tsv2, query) AS rank
   FROM songs, to_tsquery('english', 'imagination') query
   WHERE query @@ weighted_tsv2
   ORDER BY rank DESC
   LIMIT 8;
   ```
