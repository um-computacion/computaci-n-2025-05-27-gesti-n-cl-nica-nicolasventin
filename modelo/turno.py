class Turno:
    def __init__(self, paciente, medico, fecha_hora, especialidad):
        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__fecha_hora__ = fecha_hora
        self.__especialidad__ = especialidad

    def obtener_medico(self):
        return self.__medico__

    def obtener_fecha_hora(self):
        return self.__fecha_hora__

    def __str__(self):
        return (
            f"Turno de {self.__paciente__} con {self.__medico__} "
            f"por {self.__especialidad__} el {self.__fecha_hora__}"
        )
