import unittest
from modelo.paciente import Paciente

class TestPaciente(unittest.TestCase):

    def test_creacion_paciente(self):
        paciente = Paciente("Juan Pérez", "12345678", "01/01/1990")
        self.assertEqual(paciente.obtener_dni(), "12345678")

    def test_str_paciente(self):
        paciente = Paciente("Ana Gómez", "87654321", "10/10/1985")
        texto = str(paciente)
        self.assertIn("Ana Gómez", texto)
        self.assertIn("87654321", texto)

    def test_no_se_puede_crear_paciente_con_nombre_vacio(self):
        with self.assertRaises(ValueError):
            Paciente("", "123", "01/01/2000")

    def test_no_se_puede_crear_paciente_con_dni_vacio(self):
        with self.assertRaises(ValueError):
            Paciente("Nico", "", "01/01/2000")

    def test_no_se_puede_crear_paciente_con_fecha_vacia(self):
        with self.assertRaises(ValueError):
            Paciente("Nico", "123", "")


if __name__ == "__main__":
    unittest.main()
