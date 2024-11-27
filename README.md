# BD-Proyecto2024
## Integrantes:
- Camila Milagros Coveñas Rojas
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
