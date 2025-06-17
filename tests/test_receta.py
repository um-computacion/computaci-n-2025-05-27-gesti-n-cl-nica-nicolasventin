import unittest
from datetime import datetime
from modelo.receta import Receta
from modelo.paciente import Paciente
from modelo.medico import Medico

class TestReceta(unittest.TestCase):

    def test_creacion_receta(self):
        paciente = Paciente("Claudia Elaskar", "56789012", "15/05/1980")
        medico = Medico("Guillermo Ventin", "MP456")
        medicamentos = ["Ibuprofeno 600mg", "Paracetamol 500mg"]

        receta = Receta(paciente, medico, medicamentos)

        self.assertEqual(receta._Receta__paciente, paciente)
        self.assertEqual(receta._Receta__medico, medico)
        self.assertEqual(receta._Receta__medicamentos, medicamentos)
        self.assertIsInstance(receta._Receta__fecha, datetime)

    def test_str_receta(self):
        paciente = Paciente("Claudia Elaskar", "56789012", "15/05/1980")
        medico = Medico("Guillermo Ventin", "MP456")
        medicamentos = ["Ibuprofeno 600mg", "Paracetamol 500mg"]
        receta = Receta(paciente, medico, medicamentos)
        texto = str(receta)

        self.assertIn("Claudia Elaskar", texto)
        self.assertIn("Guillermo Ventin", texto)
        self.assertIn("Ibuprofeno", texto)

if __name__ == "__main__":
    unittest.main()
