# -*- coding: utf-8 -*-
"""
app.py - LA COCINA (Backend Flask)
Academia Horizonte - Sistema de Certificados
Toda la lógica de negocio vive aquí, NUNCA en las plantillas.
"""

from pathlib import Path
from flask import Flask, render_template, request
import pandas as pd


# ============================================================
# CONFIGURACIÓN - Rutas absolutas usando pathlib
# ============================================================
# Obtener la carpeta donde está este archivo (app.py)
BASE_DIR = Path(__file__).parent.resolve()
# Carpeta Insumos siempre está al lado de app.py
INSUMOS_DIR = BASE_DIR / "Insumos"

RUTA_MAESTRO = INSUMOS_DIR / "Maestro_Estudiantes.xlsx"
RUTA_EVALUACIONES = INSUMOS_DIR / "Registro_Evaluaciones.xlsx"


# ============================================================
# FUNCIONES DE NEGOCIO (Ladrillos: funciones, variables, bucles, condicionales)
# ============================================================

def cargar_datos():
    """
    LADRILLO - FUNCIÓN: Lee los dos Excel y devuelve dos DataFrames.
    LADRILLO - VARIABLES: maestro (DataFrame), evaluaciones (DataFrame)
    """
    maestro = pd.read_excel(RUTA_MAESTRO)
    evaluaciones = pd.read_excel(RUTA_EVALUACIONES)
    return maestro, evaluaciones


def calcular_promedio(notas_lista):
    """
    LADRILLO - FUNCIÓN: Calcula el promedio de una lista de notas.
    LADRILLO - VARIABLES: suma_notas (float), cantidad (int)
    LADRILLO - BUCLE: for nota in notas_lista
    LADRILLO - CONDICIONAL: if cantidad > 0
    """
    suma_notas = 0.0      # Variable acumuladora (tipo float)
    cantidad = 0          # Variable contadora (tipo int)
    
    # Bucle: recorremos cada nota
    for nota in notas_lista:
        suma_notas = suma_notas + nota
        cantidad = cantidad + 1
    
    # Condicional: evitamos división por cero
    if cantidad > 0:
        promedio = suma_notas / cantidad
    else:
        promedio = 0.0
    
    return promedio


def calcular_asistencia_promedio(asistencias_lista):
    """
    LADRILLO - FUNCIÓN: Calcula el promedio de asistencias (mismo patrón).
    """
    suma_asist = 0.0
    cantidad = 0
    
    for asist in asistencias_lista:
        suma_asist = suma_asist + asist
        cantidad = cantidad + 1
    
    if cantidad > 0:
        return suma_asist / cantidad
    else:
        return 0.0


def decidir_certificado(promedio, asistencia):
    """
    LADRILLO - FUNCIÓN: Decide el tipo de certificado según reglas de negocio.
    LADRILLO - CONDICIONALES: if / elif / else en cascada
    LADRILLO - VARIABLES: promedio (float), asistencia (float)
    REGLAS:
      - Sin certificado si asistencia < 80 (límite INCLUIDO)
      - Aprobación si promedio >= 70 Y asistencia >= 80
      - Participación si promedio < 70 Y asistencia >= 80
    """
    # Regla 1: Sin certificado (asistencia menor a 80)
    if asistencia < 80:
        return "Sin certificado"
    
    # Regla 2: Aprobación (promedio 70 o más, y asistencia 80 o más)
    elif promedio >= 70:
        return "Aprobación"
    
    # Regla 3: Participación (promedio menor a 70, pero asistencia 80 o más)
    else:
        return "Participación"


def procesar_certificados(maestro, evaluaciones):
    """
    LADRILLO - FUNCIÓN: Procesa todos los estudiantes y genera lista de resultados.
    LADRILLO - BUCLE: for (ident, prog), grupo in grupos
    LADRILLO - VARIABLES: resultados (lista), fila_maestro (DataFrame)
    LADRILLO - CONDICIONAL: if len(fila_maestro) > 0
    """
    # Agrupar evaluaciones por Identificacion + Programa
    grupos = evaluaciones.groupby(['Identificacion', 'Programa'])
    
    resultados = []           # Variable lista para acumular resultados
    inconsistencias = {       # Variable diccionario para inconsistencias
        'sin_evaluaciones': [],
        'sin_maestro': []
    }
    
    # Conjuntos para detectar inconsistencias (variables tipo set)
    est_maestro = set(zip(maestro['Identificacion'].astype(str), maestro['Programa'].astype(str)))
    est_eval = set(zip(evaluaciones['Identificacion'].astype(str), evaluaciones['Programa'].astype(str)))
    
    # 1. Estudiantes en maestro SIN evaluaciones
    for ident, prog in sorted(est_maestro - est_eval):
        fila = maestro[
            (maestro['Identificacion'].astype(str) == ident) & 
            (maestro['Programa'].astype(str) == prog)
        ]
        if len(fila) > 0:
            inconsistencias['sin_evaluaciones'].append({
                'identificacion': ident,
                'programa': prog,
                'nombre': fila.iloc[0]['Nombre_Completo']
            })
    
    # 2. Identificaciones en evaluaciones SIN maestro
    for ident, prog in sorted(est_eval - est_maestro):
        datos = evaluaciones[
            (evaluaciones['Identificacion'].astype(str) == ident) & 
            (evaluaciones['Programa'].astype(str) == prog)
        ]
        prom = datos['Nota'].mean()
        asist = datos['Asistencia_Pct'].mean()
        mods = len(datos)
        inconsistencias['sin_maestro'].append({
            'identificacion': ident,
            'programa': prog,
            'modulos': mods,
            'promedio': round(prom, 2),
            'asistencia': round(asist, 2)
        })
    
    # 3. Procesar cada grupo (estudiante + programa) que SÍ tiene evaluaciones
    for (identificacion, programa), grupo_df in grupos:
        
        # Extraer listas de notas y asistencias
        lista_notas = grupo_df['Nota'].tolist()
        lista_asist = grupo_df['Asistencia_Pct'].tolist()
        modulos_cursados = len(lista_notas)
        
        # Llamar a nuestras funciones de negocio
        promedio = calcular_promedio(lista_notas)
        asistencia_prom = calcular_asistencia_promedio(lista_asist)
        tipo_certificado = decidir_certificado(promedio, asistencia_prom)
        
        # Buscar nombre en maestro
        fila_maestro = maestro[
            (maestro['Identificacion'] == identificacion) & 
            (maestro['Programa'] == programa)
        ]
        
        # Condicional: ¿está en el maestro?
        if len(fila_maestro) > 0:
            nombre = fila_maestro.iloc[0]['Nombre_Completo']
            correo = fila_maestro.iloc[0]['Correo']
            cohorte = fila_maestro.iloc[0]['Cohorte']
            en_maestro = True
        else:
            nombre = "SIN MAESTRO - REVISAR"
            correo = ""
            cohorte = ""
            en_maestro = False
        
        # Acumular resultado
        resultados.append({
            'identificacion': identificacion,
            'nombre': nombre,
            'programa': programa,
            'cohorte': cohorte,
            'correo': correo,
            'modulos_cursados': modulos_cursados,
            'promedio': round(promedio, 2),
            'asistencia_promedio': round(asistencia_prom, 2),
            'tipo_certificado': tipo_certificado,
            'en_maestro': en_maestro
        })
    
    # Ordenar por programa y nombre
    resultados.sort(key=lambda x: (x['programa'], x['nombre']))
    
    return resultados, inconsistencias


def contar_por_tipo(resultados):
    """
    LADRILLO - FUNCIÓN: Cuenta certificados por tipo para los contadores.
    LADRILLO - VARIABLES: conteo (dict), r (dict en bucle)
    LADRILLO - BUCLE: for r in resultados
    LADRILLO - CONDICIONAL: if/elif/else
    """
    conteo = {
        'Aprobación': 0,
        'Participación': 0,
        'Sin certificado': 0
    }
    
    for r in resultados:
        # Solo contamos los que están en el maestro (no fantasmas)
        if r['en_maestro']:
            tipo = r['tipo_certificado']
            if tipo in conteo:
                conteo[tipo] = conteo[tipo] + 1
    
    return conteo


# ============================================================
# APP FLASK
# ============================================================
app = Flask(__name__)


# Cargar datos al iniciar (cache simple en memoria)
MAESTRO_DF, EVALUACIONES_DF = cargar_datos()
RESULTADOS, INCONSISTENCIAS = procesar_certificados(MAESTRO_DF, EVALUACIONES_DF)
CONTEOS = contar_por_tipo(RESULTADOS)
PROGRAMAS = sorted(MAESTRO_DF['Programa'].unique())


@app.route('/')
def index():
    """
    Ruta principal: muestra la tabla con filtros y contadores.
    El SALÓN solo recibe datos ya calculados.
    """
    # Obtener filtro de programa (query parameter)
    programa_filtro = request.args.get('programa', 'todos')
    
    # Filtrar resultados si se seleccionó un programa
    if programa_filtro != 'todos':
        resultados_filtrados = [r for r in RESULTADOS if r['programa'] == programa_filtro]
    else:
        resultados_filtrados = RESULTADOS
    
    # Contadores para el filtro actual
    conteos_filtrados = contar_por_tipo(resultados_filtrados)
    
    return render_template(
        'index.html',
        resultados=resultados_filtrados,
        programas=PROGRAMAS,
        programa_actual=programa_filtro,
        conteos=conteos_filtrados,
        inconsistencias=INCONSISTENCIAS,
        total_resultados=len(resultados_filtrados)
    )


@app.route('/health')
def health():
    """Endpoint de salud para verificar que la app está viva."""
    return {'status': 'ok', 'estudiantes': len(RESULTADOS)}


if __name__ == '__main__':
    # Ejecutar en modo debug para desarrollo
    app.run(debug=True, host='0.0.0.0', port=5000)