"""
Generación de boxplots para visualizar resultados CSP.

Genera:
- Boxplot de tiempos de ejecución por algoritmo y tamaño
- Boxplot de estados explorados por algoritmo y tamaño
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def generate_boxplots(csv_path: str, output_dir: str = '../images'):
    """Genera boxplots de tiempos y estados explorados."""
    # Leer datos
    df = pd.read_csv(csv_path)
    
    # Crear directorio de salida si no existe
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Configurar estilo
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (14, 6)
    
    # ========== BOXPLOT: ESTADOS EXPLORADOS ==========
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Distribución de Estados Explorados por Algoritmo CSP', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    sizes = sorted(df['size'].unique())
    colors = {'backtracking': '#3498db', 'forward_checking': '#2ecc71'}
    
    for idx, size in enumerate(sizes):
        ax = axes[idx]
        data_size = df[df['size'] == size]
        
        # Preparar datos para boxplot
        data_to_plot = []
        labels = []
        box_colors = []
        
        for algorithm in ['backtracking', 'forward_checking']:
            data_alg = data_size[data_size['algorithm_name'] == algorithm]['nodes']
            data_to_plot.append(data_alg)
            label = 'Backtracking' if algorithm == 'backtracking' else 'Forward Checking'
            labels.append(label)
            box_colors.append(colors[algorithm])
        
        # Crear boxplot
        bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True,
                       widths=0.6, showmeans=True,
                       meanprops=dict(marker='D', markerfacecolor='red', markersize=8))
        
        # Colorear cajas
        for patch, color in zip(bp['boxes'], box_colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_title(f'Tablero {size}x{size}', fontsize=14, fontweight='bold')
        ax.set_ylabel('Estados Explorados', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Añadir valores promedio como texto
        for i, algorithm in enumerate(['backtracking', 'forward_checking']):
            mean_val = data_size[data_size['algorithm_name'] == algorithm]['nodes'].mean()
            ax.text(i+1, mean_val, f'{mean_val:.1f}', 
                   ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    output_file = output_path / 'boxplot_estados_csp.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Guardado: {output_file}")
    plt.close()
    
    # ========== BOXPLOT: TIEMPOS DE EJECUCIÓN ==========
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Distribución de Tiempos de Ejecución por Algoritmo CSP', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    for idx, size in enumerate(sizes):
        ax = axes[idx]
        data_size = df[df['size'] == size]
        
        # Convertir tiempo a milisegundos para mejor visualización
        data_size_ms = data_size.copy()
        data_size_ms['time'] = data_size_ms['time'] * 1000
        
        # Preparar datos para boxplot
        data_to_plot = []
        labels = []
        box_colors = []
        
        for algorithm in ['backtracking', 'forward_checking']:
            data_alg = data_size_ms[data_size_ms['algorithm_name'] == algorithm]['time']
            data_to_plot.append(data_alg)
            label = 'Backtracking' if algorithm == 'backtracking' else 'Forward Checking'
            labels.append(label)
            box_colors.append(colors[algorithm])
        
        # Crear boxplot
        bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True,
                       widths=0.6, showmeans=True,
                       meanprops=dict(marker='D', markerfacecolor='red', markersize=8))
        
        # Colorear cajas
        for patch, color in zip(bp['boxes'], box_colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_title(f'Tablero {size}x{size}', fontsize=14, fontweight='bold')
        ax.set_ylabel('Tiempo (ms)', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Añadir valores promedio como texto
        for i, algorithm in enumerate(['backtracking', 'forward_checking']):
            mean_val = data_size_ms[data_size_ms['algorithm_name'] == algorithm]['time'].mean()
            ax.text(i+1, mean_val, f'{mean_val:.3f}', 
                   ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    output_file = output_path / 'boxplot_tiempos_csp.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Guardado: {output_file}")
    plt.close()
    
    # ========== GRÁFICO COMPARATIVO DE EFICIENCIA ==========
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Comparación de Eficiencia: Backtracking vs Forward Checking', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    # Calcular promedios por tamaño
    summary = df.groupby(['algorithm_name', 'size']).agg({
        'nodes': 'mean',
        'time': 'mean'
    }).reset_index()
    
    bt_summary = summary[summary['algorithm_name'] == 'backtracking']
    fc_summary = summary[summary['algorithm_name'] == 'forward_checking']
    
    # Gráfico de estados
    x = range(len(sizes))
    width = 0.35
    
    ax1.bar([i - width/2 for i in x], bt_summary['nodes'], width, 
            label='Backtracking', color='#3498db', alpha=0.8)
    ax1.bar([i + width/2 for i in x], fc_summary['nodes'], width, 
            label='Forward Checking', color='#2ecc71', alpha=0.8)
    
    ax1.set_xlabel('Tamaño del Tablero', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Estados Explorados (promedio)', fontsize=12, fontweight='bold')
    ax1.set_title('Estados Explorados', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'{s}x{s}' for s in sizes])
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Añadir valores sobre las barras
    for i, (bt_val, fc_val) in enumerate(zip(bt_summary['nodes'], fc_summary['nodes'])):
        ax1.text(i - width/2, bt_val, f'{bt_val:.0f}', 
                ha='center', va='bottom', fontweight='bold', fontsize=10)
        ax1.text(i + width/2, fc_val, f'{fc_val:.0f}', 
                ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        # Añadir porcentaje de reducción
        reduction = ((bt_val - fc_val) / bt_val) * 100
        mid_height = max(bt_val, fc_val) * 1.1
        ax1.text(i, mid_height, f'-{reduction:.0f}%', 
                ha='center', va='bottom', fontweight='bold', 
                fontsize=11, color='red')
    
    # Gráfico de tiempos (en ms)
    bt_time_ms = bt_summary['time'] * 1000
    fc_time_ms = fc_summary['time'] * 1000
    
    ax2.bar([i - width/2 for i in x], bt_time_ms, width, 
            label='Backtracking', color='#3498db', alpha=0.8)
    ax2.bar([i + width/2 for i in x], fc_time_ms, width, 
            label='Forward Checking', color='#2ecc71', alpha=0.8)
    
    ax2.set_xlabel('Tamaño del Tablero', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Tiempo (ms)', fontsize=12, fontweight='bold')
    ax2.set_title('Tiempo de Ejecución', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'{s}x{s}' for s in sizes])
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Añadir valores sobre las barras
    for i, (bt_val, fc_val) in enumerate(zip(bt_time_ms, fc_time_ms)):
        ax2.text(i - width/2, bt_val, f'{bt_val:.3f}', 
                ha='center', va='bottom', fontweight='bold', fontsize=9)
        ax2.text(i + width/2, fc_val, f'{fc_val:.3f}', 
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    output_file = output_path / 'comparacion_eficiencia_csp.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Guardado: {output_file}")
    plt.close()
    
    print("\n✅ Todos los gráficos generados exitosamente")


if __name__ == "__main__":
    csv_path = Path(__file__).parent / 'csp_results.csv'
    generate_boxplots(csv_path)
