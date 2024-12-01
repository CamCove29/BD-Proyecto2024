from SpimIndex import SPIMIIndexer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# Configurar CORS para permitir solicitudes desde el front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

indexer = None
extra_features = ["track_artist", "lyrics", "track_popularity", "track_album_id",
                  "track_album_name", "track_album_release_date", "playlist_name",
                  "playlist_id", "playlist_genre", "playlist_subgenre", "danceability",
                  "energy", "key", "loudness", "mode", "speechiness", "acousticness",
                  "instrumentalness", "liveness", "valence", "tempo", "duration_ms",
                  "language"]

@app.get("/")
def read_root():
    return {"Hello": "BD2"}

@app.post("/create_index")
def create_index(data: dict):
    """Crea un índice invertido desde un CSV."""
    if 'csv_path' not in data or 'block_size' not in data:
        return {"message": "csv_path and block_size are required", "status": 400}

    global indexer
    start_time = time.time()
    indexer = SPIMIIndexer(csv_path='C:/Users/Camila/Downloads/BD-Proyecto2024/backend/data/' + data['csv_path'],
                           block_size=data['block_size'])
    elapsed_time = time.time() - start_time
    return {"message": "Index created successfully", "time": elapsed_time, "status": 200}

@app.post("/search")
def search(data: dict):
    """Busca en el índice invertido."""
    if indexer is None:
        return {"message": "Index not created", "status": 404}

    if 'query' not in data or 'k' not in data:
        return {"message": "query and k are required", "status": 400}

    features = data.get('additional_features', [])
    for feature in features:
        if feature not in extra_features:
            return {"message": f"Invalid feature: {feature}", "status": 400}

    results = indexer.retrieve_top_k(data['query'], data['k'], additional_features=features)
    return {"result": results, "message": "Search completed", "status": 200}

# Si el script se ejecuta directamente, iniciar el servidor de FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
