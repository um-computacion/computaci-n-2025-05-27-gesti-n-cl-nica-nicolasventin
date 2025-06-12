import unittest
from datetime import datetime
from modelo.turno import Turno
from modelo.paciente import Paciente
from modelo.medico import Medico
from modelo.especialidad import Especialidad

class TestTurno(unittest.TestCase):

    def test_creacion_turno(self):
        paciente = Paciente("Luciano Miranda", "12345678", "01/01/1990")
        medico = Medico("Pablo Rizzo", "MP001")
        especialidad = Especialidad("Cardiología", ["lunes", "miércoles"])
        medico.agregar_especialidad(especialidad)
        fecha = datetime(2025, 6, 17, 14, 30)

        turno = Turno(paciente, medico, fecha, "Cardiología")

        self.assertEqual(turno.obtener_medico(), medico)
        self.assertEqual(turno.obtener_fecha_hora(), fecha)
        self.assertIn("Luciano Miranda", str(turno))
        self.assertIn("Pablo Rizzo", str(turno))
        self.assertIn("Cardiología", str(turno))

if __name__ == "__main__":
    unittest.main()
