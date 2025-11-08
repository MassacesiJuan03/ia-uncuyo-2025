# TP7B — Cross Validation (k‑folds)

## 1) Métodos

- create_folds(n, k, seed): genera una lista con k vectores de índices (1..n) que indican qué filas pertenecen a cada fold. Se usa una permutación aleatoria y se reparte en k grupos lo más parejo posible. Parámetros: n (tamaño del dataset), k (número de folds), seed (opcional para reproducibilidad).

- cross_validation(df, k, seed, formula): realiza k‑fold CV sobre el dataframe `df` usando la fórmula indicada y un árbol de decisión (`rpart`). Para cada fold entrena el modelo en k−1 folds y evalúa en el fold restante, recoge TP/TN/FP/FN y calcula Accuracy, Precision, Sensitivity y Specificity por fold.

## 2) Código de create_folds y cross_validation

```r
# create_folds: divide índices en k folds
create_folds <- function(n, k = 10, seed = NULL) {
  if (!is.null(seed)) set.seed(seed)
  ids <- sample.int(n)
  split(ids, rep(1:k, length.out = n))
}

# cross_validation: entrena rpart por fold y devuelve métricas por fold + resumen
cross_validation <- function(df, k = 10, seed = 123, formula = NULL) {
  if (is.null(formula))
    formula <- formula(inclinacion_peligrosa ~ altura + circ_tronco_cm + lat + long + nombre_seccion + especie)

  folds <- create_folds(nrow(df), k = k, seed = seed)
  res_list <- vector("list", length(folds))
  counts_list <- vector("list", length(folds))

  for (i in seq_along(folds)) {
    test_idx <- folds[[i]]
    train_idx <- setdiff(seq_len(nrow(df)), test_idx)
    train <- df[train_idx, , drop = FALSE]
    test <- df[test_idx, , drop = FALSE]

    # asegurar consistencia de factores
    train$nombre_seccion <- as.factor(train$nombre_seccion)
    train$especie <- as.factor(train$especie)
    test$nombre_seccion <- factor(test$nombre_seccion, levels = levels(train$nombre_seccion))
    test$especie <- factor(test$especie, levels = levels(train$especie))

    model <- rpart::rpart(formula, data = train, method = "class")
    preds <- suppressWarnings(as.integer(as.character(predict(model, test, type = "class"))))
    if (all(is.na(preds))) {
      lvls <- levels(predict(model, test, type = "class"))
      preds <- as.integer(match(predict(model, test, type = "class"), lvls) - 1)
    }

    cm <- confusion_metrics(test$inclinacion_peligrosa, preds)
    res_list[[i]] <- cm$metrics %>% mutate(Fold = i)
    counts_list[[i]] <- cm$counts %>% mutate(Fold = i)
  }

  metrics_tbl <- dplyr::bind_rows(res_list)
  counts_tbl <- dplyr::bind_rows(counts_list)
  summary_tbl <- metrics_tbl %>%
    dplyr::summarise(dplyr::across(dplyr::where(is.numeric), list(mean = ~mean(., na.rm = TRUE), sd = ~sd(., na.rm = TRUE))))

  list(per_fold = metrics_tbl, counts = counts_tbl, summary = summary_tbl)
}
```

## 3) Resultados (media y desviación estándar)

Se ejecutó validación cruzada 10‑fold sobre `arbolado-mendoza-dataset-train.csv`.

| Métrica     | Media    | Desviación estándar |
|:-----------|:--------:|:-------------------:|
| Accuracy    | 0.88884  | 0.00745             |
| Precision   | NA       | NA                  |
| Sensitivity | 0.00000  | 0.00000             |
| Specificity | 1.00000  | 0.00000             |


