import os
import shutil
import crud
import models
from database import engine, get_db
from email_service import enviar_tesis_por_correo
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# Crear las tablas en la base de datos automáticamente al iniciar el servidor
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
      title="Sistema de Control y Búsqueda de Tesis - IUTIRLA",
      version="1.0.0"
      )

# Montar los archivos estáticos de la interfaz web
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def inicio():
    return {
        "mensaje": "Servidor de Control de Tesis activo",
        "estado": "Base de datos sincronizada y directorio estático montado"
    }

# Endpoint para registrar tesis con su PDF
@app.post("/tesis/registrar")
def registrar_nueva_tesis(
    titulo: str = Form(...),
    autor: str = Form(...),
    tutor: str = Form(...),
    carrera: str = Form(...),
    anio: int = Form(...),
    resumen: str = Form(...),
    cota_digital: str = Form(...),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    os.makedirs("uploads", exist_ok=True)
    ruta_pdf = f"uploads/{archivo.filename}"

    with open(ruta_pdf, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    return crud.registrar_tesis(
        db=db, titulo=titulo, autor=autor, tutor=tutor,
        carrera=carrera, anio=anio, resumen=resumen,
        cota_digital=cota_digital, ruta_pdf=ruta_pdf
    )

# Endpoint para buscar tesis en el catálogo
@app.get("/tesis/buscar")
def buscar_tesis_en_catalogo(texto: str, db: Session = Depends(get_db)):
    return crud.buscar_tesis(db, texto)

# Endpoint para registrar la solicitud del estudiante
@app.post("/solicitudes/crear")
def pedir_tesis(tesis_id: int, nombre: str = Form(...), cedula: str = Form(...), correo: str = Form(...), db: Session = Depends(get_db)):
    return crud.crear_solicitud(db, tesis_id, nombre, cedula, correo)

# Endpoint para aprobar y enviar el correo SMTP
@app.post("/solicitudes/aprobar/{solicitud_id}")
def aprobar_y_enviar(solicitud_id: int, db: Session = Depends(get_db)):
    solicitud = db.query(models.SolicitudTesis).filter(models.SolicitudTesis.id == solicitud_id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    exito = enviar_tesis_por_correo(
        correo_destino=solicitud.correo_estudiante,
        nombre_estudiante=solicitud.nombre_estudiante,
        titulo_tesis=solicitud.tesis.titulo,
        ruta_pdf=solicitud.tesis.archivo_pdf
    )

    if exito:
        solicitud.estado = "enviado"
        db.commit()
        return {"mensaje": "Tesis enviada con éxito al correo del estudiante"}
    else:
        raise HTTPException(status_code=500, detail="Error al enviar el correo electrónico")