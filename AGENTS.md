# App_Certificados - OpenCode

## Contexto del proyecto
Somos **Academia Horizonte**, un centro de formación que imparte programas técnicos a empresas. Al cerrar cada cohorte emitimos certificados por estudiante. Hoy el proceso es manual en Excel y Word; vamos a automatizarlo como una **APLICACIÓN WEB**.

## Arquitectura (3 piezas)
- **Bodega (datos)**: los Excel en `insumos/`. **NO se modifican**.
- **Cocina (backend)**: Python con Flask, en `app.py`. Toda la lógica va aquí, **NUNCA en la interfaz**.
- **Salón (frontend)**: páginas web HTML servidas por Flask. Solo muestra información; no calcula ni decide.

## Archivos de entrada
- `insumos/Maestro_Estudiantes.xlsx`: lista oficial de estudiantes (Identificacion, Nombre_Completo, Correo, Programa, Cohorte).
- `insumos/Registro_Evaluaciones.xlsx`: notas (0-100) y asistencia por módulo (Identificacion, Programa, Modulo, Nota, Asistencia_Pct, Fecha_Cierre).

## Reglas de negocio
- **Promedio** = suma de Notas / cantidad de módulos cursados.
- **Asistencia** = promedio de Asistencia_Pct.
- Se agrupa por **Identificacion + Programa**. Un certificado por estudiante y programa.
- **Aprobación** si Promedio >= 70 y Asistencia >= 80.
- **Participación** si Promedio < 70 y Asistencia >= 80.
- **Sin certificado** si Asistencia < 80. Los límites **INCLUYEN** el valor.

## Estilo de trabajo
- Código simple y comentado en español, señalando dónde están los ladrillos: variables, tipos, condicionales, bucles y funciones.
- Diseño web en **azul marino y dorado**.
- Explícame en español sencillo lo que vayas haciendo.

---

## Decisiones técnicas (actualizadas tras análisis)

### Stack tecnológico
| Capa | Elección | Justificación |
|------|----------|---------------|
| **Datos (Bodega)** | `pandas` + `openpyxl` | DataFrames nativos, merges/agrupaciones triviales, estándar en Python data |
| **Backend (Cocina)** | `Flask` + `Jinja2` | Minimalista, templates HTML server-side, alineado a arquitectura Salón/Cocina |
| **Frontend (Salón)** | HTML + CSS vanilla + JS mínimo | Sin build step, azul marino (`#001f3f`) + dorado (`#ffd700`), print-friendly |
| **Tests** | `pytest` | Estándar, fixtures, parametrize para casos límite |

### Estructura de archivos objetivo
```
app_certificados/
├── app.py                 # Flask app factory + rutas
├── config.py              # Rutas, umbrales (70/80), configuración
├── services/
│   ├── __init__.py
│   ├── data_loader.py     # Lectura/validación Excel (Bodega → Cocina)
│   ├── calculator.py      # Reglas de negocio puras (promedios, clasificación)
│   └── views.py           # Helpers para templates (filtrado, serialización)
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── certificados.html
│   └── certificado.html
├── static/
│   ├── css/style.css
│   └── js/main.js
├── tests/
│   ├── test_data_loader.py
│   ├── test_calculator.py
│   └── test_routes.py
├── requirements.txt
└── README.md
```

### Casos borde documentados (del análisis de datos)
| Caso | Hallazgo | Decisión |
|------|----------|----------|
| **ID en evaluaciones sin maestro** | `999880777` (4 módulos, Prom 83.8, Asist 90%) → Aprobación | **Rechazar con alerta**: flag `fantasma=True`, nombre "SIN MAESTRO - REVISAR", log WARNING. No emitir certificado real hasta confirmación. |
| **ID en maestro sin evaluaciones** | `304560321` (Espinoza Leon Javier) | No generar certificado. Mostrar en UI admin como "Sin datos de evaluación". |
| **Notas/Asistencia = 0** | Existen en rangos 0-100 | Incluir en promedio (regla actual). Si academia dice "no presentado ≠ 0", se añade filtro posterior. |
| **Distinto nº módulos/programa** | IA Aplicada: 4; Excel: 3 | Código agrupa dinámicamente por Identificacion+Programa y cuenta módulos reales. ✓ |

### Resultados esperados (datos actuales)
- **Total certificados emitibles: 23** (20 Aprobación + 3 Participación)
- **1 fantasma** (`999880777`) → bloqueado con alerta
- **1 sin evaluaciones** (`304560321`) → sin certificado
- **Por programa**: IA Aplicada 14 est. (12A/2P/1SC/1SD), Excel 10 est. (8A/1P)

### Comandos de desarrollo (documentar al crear)
```bash
# Instalación
pip install -r requirements.txt

# Ejecución desarrollo
flask --app app run --debug

# Tests
pytest -v

# Validación datos standalone
python -m services.data_loader
python -m services.calculator
```

### Principios de código (recordatorio)
- **Cocina calcula, Salón muestra** — cero lógica en templates (solo `if`, `for`, variables)
- **Funciones puras** en `calculator.py` (mismos inputs → mismos outputs, testables)
- **Validación temprana** en `data_loader.py` (fallar rápido, mensajes claros)
- **Comentarios en español** explicando variables, tipos, condicionales, bucles, funciones