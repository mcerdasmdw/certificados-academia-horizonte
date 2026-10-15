import pandas as pd

# ============================================================
# 1. LEER ARCHIVOS EXCEL (Bodega)
# ============================================================
maestro = pd.read_excel('Insumos/Maestro_Estudiantes.xlsx')
evaluaciones = pd.read_excel('Insumos/Registro_Evaluaciones.xlsx')

print("=" * 70)
print("RESUMEN DE DATOS")
print("=" * 70)

# Estudiantes por programa
print("\n📚 ESTUDIANTES POR PROGRAMA (Maestro):")
print(maestro.groupby('Programa')['Identificacion'].nunique())

# Cantidad de evaluaciones
print("\n📝 EVALUACIONES POR PROGRAMA:")
print(evaluaciones.groupby('Programa')['Identificacion'].count())

# Módulos existentes
print("\n📦 MÓDULOS EXISTENTES:")
print(evaluaciones['Modulo'].unique())

# Rango de notas
print("\n📊 RANGO DE NOTAS:")
print(f"   Mínima: {evaluaciones['Nota'].min()}")
print(f"   Máxima: {evaluaciones['Nota'].max()}")

print("\n📊 RANGO DE ASISTENCIA (%):")
print(f"   Mínima: {evaluaciones['Asistencia_Pct'].min()}")
print(f"   Máxima: {evaluaciones['Asistencia_Pct'].max()}")

# ============================================================
# 2. FUNCIONES DE NEGOCIO (Cocina) - con ladrillos comentados
# ============================================================

def calcular_promedio(notas_lista):
    """
    LADRILLO - FUNCIÓN: recibe una lista de notas, devuelve el promedio.
    LADRILLO - VARIABLE: suma_notas (acumulador, tipo numérico)
    LADRILLO - VARIABLE: cantidad (contador, tipo entero)
    LADRILLO - BUCLE: for para recorrer cada nota
    LADRILLO - CONDICIONAL: if para evitar división por cero
    """
    # Variables: inicializamos acumuladores
    suma_notas = 0          # Variable numérica (float/int)
    cantidad = 0            # Variable entera (int)
    
    # Bucle: recorremos cada nota de la lista
    for nota in notas_lista:
        suma_notas = suma_notas + nota  # Acumulamos
        cantidad = cantidad + 1         # Contamos
    
    # Condicional: evitamos división por cero
    if cantidad > 0:
        promedio = suma_notas / cantidad  # Variable resultado
    else:
        promedio = 0
    
    return promedio


def calcular_asistencia_promedio(asistencias_lista):
    """
    LADRILLO - FUNCIÓN: calcula promedio de asistencias (mismo patrón).
    """
    suma_asist = 0
    cantidad = 0
    
    for asist in asistencias_lista:
        suma_asist = suma_asist + asist
        cantidad = cantidad + 1
    
    if cantidad > 0:
        return suma_asist / cantidad
    else:
        return 0


def decidir_certificado(promedio, asistencia):
    """
    LADRILLO - FUNCIÓN: decide tipo de certificado según reglas.
    LADRILLO - CONDICIONALES: if / elif / else en cascada
    LADRILLO - VARIABLES: promedio (float), asistencia (float)
    LADRILLO - RETORNO: string con el tipo
    """
    # Regla 1: Sin certificado si asistencia < 80 (límite INCLUIDO)
    if asistencia < 80:
        return "Sin certificado"
    
    # Regla 2: Aprobación si promedio >= 70 Y asistencia >= 80
    elif promedio >= 70:
        return "Aprobación"
    
    # Regla 3: Participación si promedio < 70 Y asistencia >= 80
    else:
        return "Participación"


# ============================================================
# 3. CRUZAR DATOS Y CALCULAR POR ESTUDIANTE+PROGRAMA
# ============================================================

print("\n" + "=" * 70)
print("CÁLCULO DE CERTIFICADOS POR ESTUDIANTE + PROGRAMA")
print("=" * 70)

# Agrupar evaluaciones por Identificacion + Programa
grupos = evaluaciones.groupby(['Identificacion', 'Programa'])

resultados = []  # Lista para acumular resultados (variable lista)

# Bucle: recorremos cada grupo (estudiante + programa)
for (identificacion, programa), grupo_df in grupos:
    
    # Extraer listas de notas y asistencias (variables tipo lista)
    lista_notas = grupo_df['Nota'].tolist()
    lista_asist = grupo_df['Asistencia_Pct'].tolist()
    modulos_cursados = len(lista_notas)  # Variable entera
    
    # Llamar a nuestras funciones (ladrillo: llamada a función)
    promedio = calcular_promedio(lista_notas)
    asistencia_prom = calcular_asistencia_promedio(lista_asist)
    tipo_certificado = decidir_certificado(promedio, asistencia_prom)
    
    # Buscar nombre en maestro (merge manual)
    fila_maestro = maestro[
        (maestro['Identificacion'] == identificacion) & 
        (maestro['Programa'] == programa)
    ]
    
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
    
    # Acumular resultado (diccionario = variable estructura)
    resultados.append({
        'Identificacion': identificacion,
        'Nombre': nombre,
        'Programa': programa,
        'Cohorte': cohorte,
        'Correo': correo,
        'Modulos_Cursados': modulos_cursados,
        'Promedio': round(promedio, 2),
        'Asistencia_Promedio': round(asistencia_prom, 2),
        'Tipo_Certificado': tipo_certificado,
        'En_Maestro': en_maestro
    })

# Convertir a DataFrame para ordenar y mostrar bonito
df_resultados = pd.DataFrame(resultados)

# Ordenar por Programa y Nombre
df_resultados = df_resultados.sort_values(['Programa', 'Nombre']).reset_index(drop=True)

# ============================================================
# 4. MOSTRAR TABLA COMPLETA
# ============================================================
print("\n📋 TABLA COMPLETA DE CERTIFICADOS (ordenada por Programa, Nombre):")
print("-" * 70)

for _, row in df_resultados.iterrows():
    flag = "" if row['En_Maestro'] else " ⚠️ FANTASMA"
    print(f"{row['Identificacion']} | {row['Nombre']:<30} | {row['Programa']:<25} | "
          f"Mod:{row['Modulos_Cursados']} | Prom:{row['Promedio']:>5.1f} | "
          f"Asist:{row['Asistencia_Promedio']:>5.1f} | {row['Tipo_Certificado']}{flag}")

# ============================================================
# 5. RESUMEN POR TIPO
# ============================================================
print("\n" + "=" * 70)
print("RESUMEN POR TIPO DE CERTIFICADO")
print("=" * 70)
conteo = df_resultados['Tipo_Certificado'].value_counts()
for tipo, cant in conteo.items():
    print(f"   {tipo}: {cant}")

# ============================================================
# 6. INCONSISTENCIAS (Reporte aparte)
# ============================================================
print("\n" + "=" * 70)
print("INCONSISTENCIAS DETECTADAS")
print("=" * 70)

# 6.1 Estudiantes en maestro SIN evaluaciones
est_maestro = set(zip(maestro['Identificacion'].astype(str), maestro['Programa'].astype(str)))
est_eval = set(zip(evaluaciones['Identificacion'].astype(str), evaluaciones['Programa'].astype(str)))

sin_evaluaciones = est_maestro - est_eval
print(f"\n❌ ESTUDIANTES EN MAESTRO SIN EVALUACIONES: {len(sin_evaluaciones)}")
for ident, prog in sorted(sin_evaluaciones):
    nombre = maestro[
        (maestro['Identificacion'].astype(str) == ident) & 
        (maestro['Programa'].astype(str) == prog)
    ]['Nombre_Completo'].values[0]
    print(f"   - {ident} | {prog} | {nombre}")

# 6.2 Identificaciones en evaluaciones NO en maestro
sin_maestro = est_eval - est_maestro
print(f"\n⚠️  IDENTIFICACIONES EN EVALUACIONES SIN MAESTRO: {len(sin_maestro)}")
for ident, prog in sorted(sin_maestro):
    # Mostrar sus datos de evaluación
    datos = evaluaciones[
        (evaluaciones['Identificacion'].astype(str) == ident) & 
        (evaluaciones['Programa'].astype(str) == prog)
    ]
    prom = datos['Nota'].mean()
    asist = datos['Asistencia_Pct'].mean()
    mods = len(datos)
    print(f"   - {ident} | {prog} | Módulos:{mods} | Prom:{prom:.1f} | Asist:{asist:.1f} → FANTASMA")

print("\n" + "=" * 70)
print("FIN DEL ANÁLISIS")
print("=" * 70)