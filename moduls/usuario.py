class Usuario:

    def __init__(self, nombre, correo, password, rol="cliente", id=None):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.password = password
        self.rol = rol

    def __str__(self):
        return f"Usuario[{self.id}]: {self.nombre} ({self.rol})"