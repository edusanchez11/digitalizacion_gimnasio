from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum

'''
Este archivo  define los modelos de datos del 
sistema. Es decir, como se representan los usuarios 
y las facturas del gimnasio.
'''

class EstadoFactura(str, Enum):
    PENDIENTE = "Pendiente"
    PAGADA = "Pagada"
    CANCELADA = "Cancelada"

@dataclass
class Usuario:
    ''' Clase que representa a un usuario del gimnasio. '''
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    fecha_registro: datetime = field(default_factory=datetime.now)
    id: str = ""
    facturas: List['Factura'] = field(default_factory=list)

@dataclass
class Factura:
    ''' Clase que representa una factura del gimnasio. '''
    descripcion: str
    monto: float
    estado: EstadoFactura = EstadoFactura.PENDIENTE
    fecha: datetime = field(default_factory=datetime.now)
    id: str = ""
    usuario_id: str = ""

    def __post_init__(self):
        ''' Este método se ejecuta después de crear una factura y verifica que el monto sea mayor que cero. 
        Si no lo es, lanza un error. '''
        if self.monto < 0:
            raise ValueError("El monto de la factura no puede ser negativo.")

