## Cómo ejecutar el sistema

1. Abrí una terminal.
2. Navegá a la carpeta raíz del proyecto.
3. Ejecutá el siguiente comando:

```bash
python cli/main.py
```

> Asegurate de tener Python 3 instalado y el módulo `modelo` en la misma raíz.

---

## Cómo ejecutar las pruebas

1. Desde la raíz del proyecto, corré:

```bash
python -m unittest discover -s tests
```

Esto ejecuta **todos los archivos de prueba** dentro de la carpeta `tests/`.

> Todos los tests están escritos con `unittest` y validan las funciones principales del modelo.

---

## Explicación de diseño general

El sistema está diseñado usando **programación orientada a objetos**. Se divide en:

### Módulo `modelo/`
Contiene las clases principales:
- `Paciente`, `Medico`, `Especialidad`, `Turno`, `Receta`, `HistoriaClinica`, `Clinica`
- Cada clase representa una entidad real del sistema.
- Las validaciones se hacen **desde el modelo**, no desde la interfaz.

### Módulo `cli/`
- Implementa una interfaz de consola (`CLI`) para interactuar con el usuario.
- Presenta un menú, recoge datos y los envía al modelo.
- Maneja errores y entradas inválidas (como turnos mal cargados o matrículas inexistentes).
- Se utilizan estructuras como `listas`, `diccionarios` y `índices` para manejar pasos de ingreso dinámico de datos.
- También se usan estructuras de control como `while` para recorrer pasos de ingreso, y `for` para mostrar resultados o recorrer listas de datos.

### Módulo `tests/`
- Contiene pruebas automáticas para todas las clases del modelo.
- Usa `unittest` para verificar funcionamiento y validaciones.

### Validaciones
- Se usan **excepciones personalizadas** para manejar errores del dominio.
- Se **normalizan** textos para evitar errores por tildes, mayúsculas o espacios extra.

---

##  Estructuras y conceptos utilizados

- **Diccionarios**: para almacenar pacientes (`dni → Paciente`), médicos (`matrícula → Médico`), y acceder rápidamente a sus datos.
- **Listas**: para guardar turnos, recetas y pasos del CLI.
- **Índices**: para controlar el flujo paso a paso del ingreso de datos en la consola.
- **Bucles `while`**: para permitir al usuario navegar por los pasos, volver atrás o cancelar.
- **Bucles `for`**: para mostrar listas de pacientes, médicos, turnos o especialidades.
- **Funciones personalizadas**: para normalizar textos, validar formatos y encapsular lógica de negocio.

##  Índice de archivos de test

A continuación se detalla qué funcionalidades testea cada archivo dentro del directorio `tests/`:

### `test_paciente.py`
- Registro válido de paciente.
- ❌ No se permite crear paciente con:
  - Nombre vacío
  - DNI vacío
  - Fecha de nacimiento vacía

### `test_medico.py`
- Registro válido de médico.
- ❌ No se permite crear médico con:
  - Nombre vacío
  - Matrícula vacía
- ❌ No se puede agregar una especialidad duplicada.

### `test_clinica.py`
- Registro de pacientes y médicos.
- ❌ No se permite agregar pacientes/médicos duplicados.
- ❌ No se puede agendar turno si:
  - El médico no existe.
  - El paciente no existe.
  - El turno está duplicado.
  - El médico no atiende esa especialidad.
  - El médico no trabaja ese día.
- ❌ No se puede emitir receta si:
  - No hay medicamentos.
  - El paciente no existe.
  - El médico no existe.
- ✅ Confirmación de que turnos y recetas se guardan en la historia clínica.

### `test_historia_clinica.py`
- ✅ Confirma que los turnos y recetas emitidos se almacenan correctamente.