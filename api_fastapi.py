from fastapi import FastAPI
import mysql.connector
import uvicorn
from db_config import config, configRemote

app = FastAPI()

#Cambiar a config si la base remota empieza a fallar
cnx = mysql.connector.connect(**configRemote)
cursor = cnx.cursor(dictionary=True)


@app.get('/cines')
def cines():
    cursor.callproc('sp_getCines')
    for data in cursor.stored_results():
        cines = data.fetchall()
    return cines


@app.get('/cine/{id}')
def cine(id: int):
    cursor.callproc('sp_getCine', (id,))
    for data in cursor.stored_results():
        cine = data.fetchone()
        
    cursor.callproc('sp_getCinePeliculas', (id,))
    for data in cursor.stored_results():
        peliculas = data.fetchall()
        
    cursor.callproc('sp_getCineTarifas', (id,))
    for data in cursor.stored_results():
        tarifas = data.fetchall()
     
    cine['peliculas']  = peliculas
    cine['tarifas']=tarifas
    return cine


@app.get('/peliculas/{id}')
def peliculas(id: str):
    id = 1 if id == 'cartelera' else 2 if id == 'estrenos' else 0
    if id == 0:
        return
    
    cursor.callproc('sp_getPeliculas', (id,))
    for data in cursor.stored_results():
        peliculas = data.fetchall()
        return peliculas


@app.get('/pelicula/{id}')
def pelicula(id: int):
    cursor.callproc('sp_getPelicula', (id,))
    for data in cursor.stored_results():
        pelicula =  data.fetchone()
    return pelicula 
    
if __name__ == '__main__':
    uvicorn.run(app)
