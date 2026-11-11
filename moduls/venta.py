from datetime import datetime

class venta:
    def __init__(self,id: int, usuario_id:int, total: float, fecha: datetime=None,detalles: list = None):
        self.id = id
        self.usuario_id = usuario_id
        self.total = total
        self.fecha = fecha
        self.detalles = detalles if detalles else []
    def __str__(self):
        return f"Venta #{self.id} | Total: {self.total:.2f} | Fecha {self.fecha}"    