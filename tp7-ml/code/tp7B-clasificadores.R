# TP7B - Clasificadores (ejercicio 4 y 5)

# Prepara biblioteca de usuario y dependencias
userlib <- Sys.getenv('R_LIBS_USER')
if (userlib == '') userlib <- file.path(Sys.getenv('USERPROFILE'), 'Documents', 'R', 'win-library', paste0('R-', R.version$major, '.', R.version$minor))
dir.create(userlib, recursive = TRUE, showWarnings = FALSE)
.libPaths(userlib)

if (!requireNamespace('dplyr', quietly = TRUE)) install.packages('dplyr', repos='https://cran.rstudio.com', lib = userlib)
if (!requireNamespace('readr', quietly = TRUE)) install.packages('readr', repos='https://cran.rstudio.com', lib = userlib)

library(dplyr)
library(readr)

# Rutas de archivos
validation_path <- 'tp7-ml/data/arbolado-mendoza-dataset-validation.csv'
out_random_csv <- 'tp7-ml/data/arbolado-mendoza-dataset-validation-predictions-random.csv'
out_bigger_csv <- 'tp7-ml/data/arbolado-mendoza-dataset-validation-predictions-biggerclass.csv'
md_out <- 'tp7-ml/tp7B-clasificadores.md'

if (!file.exists(validation_path)) stop('Archivo de validacion no encontrado: ', validation_path)

# Carga dataframe de validacion
df_val <- read_csv(validation_path, show_col_types = FALSE)

# (4a) funcion que agrega columna prediction_prob aleatoria
add_prediction_prob <- function(df){
  df %>% mutate(prediction_prob = runif(n()))
}

# (4b) random_classifier: usa prediction_prob para generar prediction_class
random_classifier <- function(df){
  df %>% mutate(prediction_class = ifelse(prediction_prob > 0.5, 1L, 0L))
}

# (5a) biggerclass_classifier: asigna siempre la clase mayoritaria (segun columna inclinacion_peligrosa)
biggerclass_classifier <- function(df){
  maj <- df %>% count(inclinacion_peligrosa) %>% arrange(desc(n)) %>% slice(1) %>% pull(inclinacion_peligrosa)
  maj_int <- as.integer(maj)
  df %>% mutate(prediction_class = rep(maj_int, n()))
}

# helper: calcula confusion y metricas
compute_confusion_and_metrics <- function(df, truth_col = 'inclinacion_peligrosa', pred_col = 'prediction_class'){
  tp <- sum(df[[truth_col]] == 1 & df[[pred_col]] == 1, na.rm = TRUE)
  tn <- sum(df[[truth_col]] == 0 & df[[pred_col]] == 0, na.rm = TRUE)
  fp <- sum(df[[truth_col]] == 0 & df[[pred_col]] == 1, na.rm = TRUE)
  fn <- sum(df[[truth_col]] == 1 & df[[pred_col]] == 0, na.rm = TRUE)
  n <- nrow(df)
  accuracy <- (tp + tn) / n
  precision <- if ((tp + fp) == 0) NA else tp / (tp + fp)
  sensitivity <- if ((tp + fn) == 0) NA else tp / (tp + fn)
  specificity <- if ((tn + fp) == 0) NA else tn / (tn + fp)
  list(counts = tibble::tibble(TP = tp, TN = tn, FP = fp, FN = fn), metrics = tibble::tibble(accuracy = accuracy, precision = precision, sensitivity = sensitivity, specificity = specificity))
}

# --- Aplica clasificador aleatorio ---
df_random <- df_val %>% add_prediction_prob() %>% random_classifier()
res_random <- compute_confusion_and_metrics(df_random)
write_csv(df_random, out_random_csv)

# --- Aplica clasificador por clase mayoritaria ---
df_bigger <- df_val %>% biggerclass_classifier()
res_bigger <- compute_confusion_and_metrics(df_bigger)
write_csv(df_bigger, out_bigger_csv)

# --- Genera archivo md con resultados ---
md_lines <- c('# TP7B — Clasificadores', '', '## Clasificador aleatorio', '', '### Matriz de confusión (conteos)', '')
md_lines <- c(md_lines, '', '| | Pred=1 | Pred=0 |', '|---:|---:|---:|')
md_lines <- c(md_lines, sprintf('| Real=1 | %d | %d |', res_random$counts$TP, res_random$counts$FN))
md_lines <- c(md_lines, sprintf('| Real=0 | %d | %d |', res_random$counts$FP, res_random$counts$TN))
md_lines <- c(md_lines, '', '### Métricas', '', sprintf('- Accuracy: %.4f', res_random$metrics$accuracy), sprintf('- Precision: %s', ifelse(is.na(res_random$metrics$precision), 'NA', sprintf('%.4f', res_random$metrics$precision))), sprintf('- Sensitivity (Recall): %s', ifelse(is.na(res_random$metrics$sensitivity), 'NA', sprintf('%.4f', res_random$metrics$sensitivity))), sprintf('- Specificity: %s', ifelse(is.na(res_random$metrics$specificity), 'NA', sprintf('%.4f', res_random$metrics$specificity))), '')

md_lines <- c(md_lines, '## Clasificador por clase mayoritaria', '', '### Matriz de confusión (conteos)', '', '| | Pred=1 | Pred=0 |', '|---:|---:|---:|')
md_lines <- c(md_lines, sprintf('| Real=1 | %d | %d |', res_bigger$counts$TP, res_bigger$counts$FN))
md_lines <- c(md_lines, sprintf('| Real=0 | %d | %d |', res_bigger$counts$FP, res_bigger$counts$TN))
md_lines <- c(md_lines, '', '### Métricas', '', sprintf('- Accuracy: %.4f', res_bigger$metrics$accuracy), sprintf('- Precision: %s', ifelse(is.na(res_bigger$metrics$precision), 'NA', sprintf('%.4f', res_bigger$metrics$precision))), sprintf('- Sensitivity (Recall): %s', ifelse(is.na(res_bigger$metrics$sensitivity), 'NA', sprintf('%.4f', res_bigger$metrics$sensitivity))), sprintf('- Specificity: %s', ifelse(is.na(res_bigger$metrics$specificity), 'NA', sprintf('%.4f', res_bigger$metrics$specificity))), '')

writeLines(md_lines, md_out)

# --- Resumen por consola ---
cat('Random classifier: ', '\n')
print(res_random)
cat('\nBiggerclass classifier: ', '\n')
print(res_bigger)
cat('\nArchivos generados:\n')
cat('-', out_random_csv, '\n')
cat('-', out_bigger_csv, '\n')
cat('-', md_out, '\n')

