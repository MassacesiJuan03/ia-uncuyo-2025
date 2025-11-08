## Parte 2

### i) Preprocesamiento
- Se limpiaron y transformaron las columnas más relevantes:
  - `altura` → `altura_m` (se extrajo el valor numérico en metros).
  - `diametro_tronco` → `diametro_num` (se mapeó a valores numéricos).
- Se crearon variables derivadas sencillas, por ejemplo la razón entre circunferencia y altura.
- Las variables categóricas principales (`especie`, `nombre_seccion`) se codificaron mediante codificación por objetivo suavizada; el cálculo se realizó únicamente con datos de entrenamiento dentro de cada partición para evitar fuga de información.

### ii) Resultados en validación
- Validación: k‑fold estratificado (k = 5), métrica AUC ROC.
- Resultado principal (OOF): ≈ 0.755

### iii) Resultado en la competición (Kaggle)
- Último puntaje público en la competición: 0.71618

### iv) Algoritmo (resumen)
- Modelo base: XGBoost. Se calculó un peso para la clase positiva según el desbalance de clases para mitigar su efecto.
- Flujo resumido:
  1. Preparación y creación de variables.
  2. Codificación por objetivo para variables categóricas (aplicada por partición para evitar fuga de información).
  3. Validación fuera de la muestra con k‑fold estratificado (k = 5) para obtener una estimación realista del desempeño.
  4. Búsqueda de hiperparámetros con Optuna (30 pruebas) optimizando la AUC.
  5. Reentrenamiento final con los mejores hiperparámetros y generación del archivo para la competición.
