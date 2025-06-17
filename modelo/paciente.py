class Paciente:
    def __init__(self, nombre, dni, fecha_nacimiento):
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if not dni.strip():
            raise ValueError("El DNI no puede estar vacío")
        if not fecha_nacimiento.strip():
            raise ValueError("La fecha de nacimiento no puede estar vacía")

        self.__nombre__ = nombre
        self.__dni__ = dni
        self.__fecha_nacimiento__ = fecha_nacimiento

    def obtener_dni(self):
        return self.__dni__

    def __str__(self):
        return f"{self.__nombre__} (DNI: {self.__dni__})"
