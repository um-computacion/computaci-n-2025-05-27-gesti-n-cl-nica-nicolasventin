class Especialidad:
    def __init__(self, tipo, dias):
        self.__tipo__ = tipo
        self.__dias__ = [d.lower() for d in dias]

    def obtener_especialidad(self):
        return self.__tipo__

    def verificar_dia(self, dia):
        return dia.lower() in self.__dias__

    def __str__(self):
        dias_str = ", ".join(self.__dias__)
        return f"{self.__tipo__} (Días: {dias_str})"
