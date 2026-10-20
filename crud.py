from sqlalchemy.orm import Session
import models

# ==========================================
# GESTIÓN DE TESIS
# ==========================================

# 1. Registrar una nueva tesis en la BD con su archivo PDF
def registrar_tesis(
    db: Session, 
    titulo: str, 
    autor: str, 
    tutor: str, 
    carrera: str, 
    anio: int, 
    resumen: str, 
    cota_digital: str, 
    ruta_pdf: str
):
    nueva_tesis = models.Tesis(
        titulo=titulo,
        autor=autor,
        tutor=tutor,
        carrera=carrera,
        anio=anio,
        resumen=resumen,
        cota_digital=cota_digital,
        archivo_pdf=ruta_pdf
    )
    db.add(nueva_tesis)
    db.commit()
    db.refresh(nueva_tesis)
    return nueva_tesis

# 2. Buscar tesis por coincidencia en título, autor, carrera, resumen o cota digital
def buscar_tesis(db: Session, texto: str):
    patron = f"%{texto}%"
    return db.query(models.Tesis).filter(
        (models.Tesis.titulo.ilike(patron)) |
        (models.Tesis.autor.ilike(patron)) |
        (models.Tesis.carrera.ilike(patron)) |
        (models.Tesis.resumen.ilike(patron)) |
        (models.Tesis.cota_digital.ilike(patron))
    ).all()

# 3. Obtener el catálogo completo de tesis
def obtener_todas(db: Session):
    return db.query(models.Tesis).all()


# ==========================================
# GESTIÓN DE SOLICITUDES DE CORREO
# ==========================================

# 4. Crear una solicitud realizada por un estudiante
def crear_solicitud(db: Session, tesis_id: int, nombre: str, cedula: str, correo: str):
    nueva_solicitud = models.SolicitudTesis(
        tesis_id=tesis_id,
        nombre_estudiante=nombre,
        cedula_estudiante=cedula,
        correo_estudiante=correo
    )
    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)
    return nueva_solicitud

# 5. Obtener solicitudes pendientes para el panel de la profesora
def obtener_solicitudes_pendientes(db: Session):
    return db.query(models.SolicitudTesis).filter(
        models.SolicitudTesis.estado == "pendiente"
    ).all()