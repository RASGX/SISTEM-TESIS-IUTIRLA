from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), default="administrador") 


class Tesis(Base):
    __tablename__ = "tesis"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), index=True, nullable=False)
    autor = Column(String(150), index=True, nullable=False)
    tutor = Column(String(150), nullable=False)
    carrera = Column(String(100), nullable=False)
    anio = Column(Integer, nullable=False)
    resumen = Column(Text, nullable=False)
    cota_digital = Column(String(50), unique=True, nullable=False) # Código único digital (Ej: ING-2026-001)
    archivo_pdf = Column(String(255), nullable=False) # Ruta del PDF digital guardado en servidor
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    # Relación con solicitudes
    solicitudes = relationship("SolicitudTesis", back_populates="tesis")


class SolicitudTesis(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    tesis_id = Column(Integer, ForeignKey("tesis.id"), nullable=False)
    nombre_estudiante = Column(String(150), nullable=False)
    cedula_estudiante = Column(String(20), nullable=False)
    correo_estudiante = Column(String(100), nullable=False)
    estado = Column(String(20), default="pendiente") # pendiente, enviado, rechazado
    fecha_solicitud = Column(DateTime, default=datetime.utcnow)

    # Relación con la tesis solicitada
    tesis = relationship("Tesis", back_populates="solicitudes")