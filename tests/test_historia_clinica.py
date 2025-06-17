import unittest
from modelo.historia_clinica import HistoriaClinica
from modelo.paciente import Paciente
from modelo.medico import Medico
from modelo.turno import Turno
from modelo.receta import Receta
from modelo.especialidad import Especialidad
from modelo.clinica import Clinica
from datetime import datetime

class TestHistoriaClinica(unittest.TestCase):

    def setUp(self):
        self.clinica = Clinica()

    def test_agregar_y_obtener_turnos(self):
        paciente = Paciente("Raúl Ponte", "11112222", "05/08/1975")
        medico = Medico("Diego Ventin", "MP789")
        turno = Turno(paciente, medico, datetime(2025, 6, 20, 10, 0), "Pediatría")

        historia = HistoriaClinica(paciente)
        historia.agregar_turno(turno)
        turnos = historia.obtener_turnos()

        self.assertEqual(len(turnos), 1)
        self.assertEqual(turnos[0], turno)

    def test_agregar_y_obtener_recetas(self):
        paciente = Paciente("Raúl Ponte", "11112222", "05/08/1975")
        medico = Medico("Diego Ventin", "MP789")
        receta = Receta(paciente, medico, ["Amoxicilina 500mg"])

        historia = HistoriaClinica(paciente)
        historia.agregar_receta(receta)
        recetas = historia.obtener_recetas()

        self.assertEqual(len(recetas), 1)
        self.assertEqual(recetas[0], receta)

    def test_str_historia_clinica(self):
        paciente = Paciente("Raúl Ponte", "11112222", "05/08/1975")
        medico = Medico("Diego Ventin", "MP789")
        historia = HistoriaClinica(paciente)
        receta = Receta(paciente, medico, ["Amoxicilina"])
        turno = Turno(paciente, medico, datetime(2025, 6, 20, 10, 0), "Pediatría")
        historia.agregar_turno(turno)
        historia.agregar_receta(receta)

        texto = str(historia)
        self.assertIn("Raúl Ponte", texto)
        self.assertIn("Amoxicilina", texto)
        self.assertIn("Pediatría", texto)

    def test_turno_y_receta_se_guardan_en_historia_clinica(self):
        paciente = Paciente("Test", "400", "01/01/2000")
        medico = Medico("Doc", "MP400")
        especialidad = Especialidad("Clinica", ["miércoles"])
        medico.agregar_especialidad(especialidad)

        self.clinica.agregar_paciente(paciente)
        self.clinica.agregar_medico(medico)

        fecha = datetime(2025, 6, 18, 12, 0)  # miércoles
        self.clinica.agendar_turno("400", "MP400", "Clinica", fecha)
        self.clinica.emitir_receta("400", "MP400", ["Paracetamol"])

        historia = self.clinica.obtener_historia_clinica("400")
        self.assertEqual(len(historia.obtener_turnos()), 1)
        self.assertEqual(len(historia.obtener_recetas()), 1)


if __name__ == "__main__":
    unittest.main()
