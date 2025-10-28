import pandas as pd
import matplotlib.pyplot as plt

# Leer el CSV
df = pd.read_csv("resultados_agentes.csv")

# Definir el orden correcto de tamaños
size_order = ['2x2', '16x16', '2x2', '32x32', '4x4', '64x64', '8x8', '128x128']

# ==================== BOXPLOTS POR DIRT_RATE Y TAMAÑO ====================

# Generar boxplots para 4x4 y 64x64 por separado
sizes_for_boxplot = ['4x4', '64x64']

for size in sizes_for_boxplot:
    df_size = df[df['size'] == size].copy()
    dirt_rates = sorted(df_size['dirt_rate'].unique())
    
    # Boxplots de EFECTIVIDAD para este tamaño
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Boxplot de Efectividad por Agente ({size}) - Separado por Dirt Rate', fontsize=16, fontweight='bold')
    
    for idx, dirt_rate in enumerate(dirt_rates):
        ax = axes[idx // 2, idx % 2]
        df_filtrado = df_size[df_size['dirt_rate'] == dirt_rate]
        df_filtrado.boxplot(column='efectividad', by='agente', ax=ax)
        ax.set_title(f'Dirt Rate = {dirt_rate}', fontsize=12, fontweight='bold')
        ax.set_xlabel('Agente')
        ax.set_ylabel('Efectividad (performance / total_dirt)')
        ax.get_figure().suptitle('')
    
    plt.tight_layout()
    filename = f"boxplot_efectividad_{size.replace('x', '')}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Boxplot guardado: {filename}")
    plt.close()
    
    # Boxplots de EFICIENCIA para este tamaño
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Boxplot de Eficiencia por Agente ({size}) - Separado por Dirt Rate', fontsize=16, fontweight='bold')
    
    for idx, dirt_rate in enumerate(dirt_rates):
        ax = axes[idx // 2, idx % 2]
        df_filtrado = df_size[df_size['dirt_rate'] == dirt_rate]
        df_filtrado.boxplot(column='eficiencia', by='agente', ax=ax)
        ax.set_title(f'Dirt Rate = {dirt_rate}', fontsize=12, fontweight='bold')
        ax.set_xlabel('Agente')
        ax.set_ylabel('Eficiencia (performance / steps)')
        ax.get_figure().suptitle('')
    
    plt.tight_layout()
    filename = f"boxplot_eficiencia_{size.replace('x', '')}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Boxplot guardado: {filename}")
    plt.close()

# ==================== GRÁFICOS DE BARRAS (TODOS LOS TAMAÑOS) ====================

# Función para ordenar sizes correctamente
def get_size_number(size_str):
    # Extraer el número de la cadena (e.g., "2x2" -> 2, "128x128" -> 128)
    return int(size_str.split('x')[0])

# Ordenar los tamaños
sizes_sorted = sorted(df['size'].unique(), key=get_size_number)

# --- Gráfico 1: % de limpieza por TODOS los tamaños ---
agrupado_efectividad = df.groupby(['size', 'agente'])['efectividad'].mean().reset_index()
pivot_efectividad = agrupado_efectividad.pivot(index='size', columns='agente', values='efectividad')
# Reordenar usando los tamaños ordenados
pivot_efectividad = pivot_efectividad.reindex(sizes_sorted)

pivot_efectividad.plot(kind='bar', figsize=(10, 6))
plt.ylabel('% de limpieza promedio')
plt.xlabel('Tamaño del entorno')
plt.title('% de limpieza por tamaño de entorno y agente')
plt.legend(title='Agente')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("efectividad_por_size_y_agente.png", dpi=300)
print("✅ Gráfico de barras guardado: efectividad_por_size_y_agente.png")
plt.close()

# --- Gráfico 2: Eficiencia promedio por TODOS los tamaños ---
agrupado_eficiencia = df.groupby(['size', 'agente'])['eficiencia'].mean().reset_index()
pivot_eficiencia = agrupado_eficiencia.pivot(index='size', columns='agente', values='eficiencia')
# Reordenar usando los tamaños ordenados
pivot_eficiencia = pivot_eficiencia.reindex(sizes_sorted)

pivot_eficiencia.plot(kind='bar', figsize=(10, 6))
plt.ylabel('Eficiencia promedio')
plt.xlabel('Tamaño del entorno')
plt.title('Eficiencia promedio por tamaño de entorno y agente')
plt.legend(title='Agente')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("eficiencia_por_size_y_agente.png", dpi=300)
print("✅ Gráfico de barras guardado: eficiencia_por_size_y_agente.png")
plt.close()

print("\n✅ Todos los gráficos generados correctamente:"
      "\n   - 4 boxplots separados:"
      "\n     * boxplot_efectividad_4x4.png (4x4)"
      "\n     * boxplot_eficiencia_4x4.png (4x4)"
      "\n     * boxplot_efectividad_64x64.png (64x64)"
      "\n     * boxplot_eficiencia_64x64.png (64x64)"
      "\n   - 2 gráficos de barras (efectividad y eficiencia) con todos los tamaños ordenados")