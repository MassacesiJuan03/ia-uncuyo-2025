import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import concurrent.futures

DATA_DIR = "/home/juan-ignacio/Escritorio/Facultad/IA1/tp2-agentes-racionales/vacuum-cleaner-world/game_data"
resultados = []

def procesar_archivo(ruta):
    try:
        with open(ruta, "r") as f:
            data = json.load(f)

        meta = data.get("metadata", None)
        if not meta:
            return None

        agente = meta.get("agent_type", os.path.basename(os.path.dirname(os.path.dirname(ruta))))
        size = "x".join(map(str, meta.get("environment_size", [])))
        dirt_rate = meta.get("dirt_rate", None)
        total_dirt = meta.get("total_dirt_cells", 0)
        performance = meta.get("final_performance", 0)
        steps = meta.get("steps_to_completion", 0)

        efectividad = performance / total_dirt if total_dirt > 0 else 0
        eficiencia = performance / steps if steps > 0 else 0

        return {
            "agente": agente,
            "size": size,
            "dirt_rate": dirt_rate,
            "total_dirt": total_dirt,
            "performance": performance,
            "steps": steps,
            "efectividad": efectividad,
            "eficiencia": eficiencia
        }
    except Exception:
        return None

# Recopilar rutas de archivos JSON
rutas_json = []
for root, dirs, files in os.walk(DATA_DIR):
    for archivo in files:
        if archivo.endswith(".json"):
            rutas_json.append(os.path.join(root, archivo))

# Procesar en paralelo
with concurrent.futures.ThreadPoolExecutor() as executor:
    resultados = list(filter(None, executor.map(procesar_archivo, rutas_json)))

procesados = len(resultados)
descartados = len(rutas_json) - procesados

print(f"✔️ Archivos procesados: {procesados}")
print(f"⚠️ Archivos descartados: {descartados}")

# Convertir a DataFrame
df = pd.DataFrame(resultados)

# Guardar en CSV para análisis posterior
df.to_csv("resultados_agentes.csv", index=False)
print("✅ Resultados guardados en resultados_agentes.csv")

# Agrupar por agente y dirt_rate
agrupado = df.groupby(["agente", "size", "dirt_rate"]).agg({
    "performance": ["mean", "std"],
    "steps": ["mean", "std"],
    "efectividad": "mean",
    "eficiencia": "mean"
}).reset_index()

print("\n📊 Resumen de desempeño:\n")
print(agrupado)
# --- Gráfico de dispersión: performance vs steps ---
fig, ax = plt.subplots(figsize=(10, 6))
for agente, grupo in df.groupby("agente"):
    ax.scatter(grupo["steps"], grupo["performance"], label=agente, alpha=0.6)
ax.set_xlabel("Pasos")
ax.set_ylabel("Performance")
ax.set_title("Comparación de agentes")
ax.legend()
plt.tight_layout()
plt.savefig("comparacion_agentes.png")  # Guarda el gráfico como imagen
print("✅ Gráfico guardado en comparacion_agentes.png")

# plt.show()  # Ya no es necesario, se guarda directamente
# --- Gráfico de barras: efectividad promedio por agente ---
agrupado_efectividad = df.groupby("agente")["efectividad"].mean().reset_index()
agrupado_efectividad.plot(kind='bar', x='agente', y='efectividad', figsize=(10, 6), legend=False)
plt.ylabel('% de limpieza promedio')
plt.xlabel('Agente')
plt.title('% de limpieza promedio por agente')
plt.tight_layout()
plt.savefig("efectividad_por_agente.png")
print("✅ Gráfico de barras guardado en efectividad_por_agente.png")

# --- Gráfico de barras agrupadas: % de limpieza (efectividad) por tamaño de entorno y agente ---
agrupado_size = df.groupby(['size', 'agente'])['efectividad'].mean().reset_index()

# Pivot para barras agrupadas
pivot = agrupado_size.pivot(index='size', columns='agente', values='efectividad')

pivot.plot(kind='bar', figsize=(10,6))
plt.ylabel('% de limpieza promedio')
plt.xlabel('Tamaño del entorno')
plt.title('% de limpieza por tamaño de entorno y agente')
plt.legend(title='Agente')
plt.tight_layout()
plt.savefig("efectividad_por_size_y_agente.png")
print("✅ Gráfico de barras guardado en efectividad_por_size_y_agente.png")

# --- Gráfico de barras agrupadas: pasos promedio por tamaño de entorno y agente ---
agrupado_steps = df.groupby(['size', 'agente'])['steps'].mean().reset_index()
pivot_steps = agrupado_steps.pivot(index='size', columns='agente', values='steps')

pivot_steps.plot(kind='bar', figsize=(10,6))
plt.ylabel('Pasos promedio')
plt.xlabel('Tamaño del entorno')
plt.title('Pasos promedio por tamaño de entorno y agente')
plt.legend(title='Agente')
plt.tight_layout()
plt.savefig("pasos_promedio_por_size_y_agente.png")
print("✅ Gráfico de barras guardado en pasos_promedio_por_size_y_agente.png")

