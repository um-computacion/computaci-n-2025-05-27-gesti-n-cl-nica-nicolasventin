from datetime import datetime

class Receta:
    def __init__(self, paciente, medico, medicamentos):
        self.__paciente = paciente
        self.__medico = medico
        self.__medicamentos = medicamentos
        self.__fecha = datetime.now()

    def __str__(self):
        meds = ", ".join(self.__medicamentos)
        return (
            f"Receta para {self.__paciente} emitida por {self.__medico} "
            f"el {self.__fecha.strftime('%d/%m/%Y')} con medicamentos: {meds}"
        )

if __name__ == "__main__":
    receta = Receta("Paciente de prueba", "Médico de prueba", ["Ibuprofeno"])
    print("Acceso directo:", receta._Receta__paciente)
