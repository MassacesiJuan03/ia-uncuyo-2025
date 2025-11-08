# TP7B - Ejercicio 7

# Dependencias mínimas
pkgs <- c('readr','dplyr','rpart','tibble')
userlib <- Sys.getenv('R_LIBS_USER')
if (userlib == '') userlib <- file.path(Sys.getenv('USERPROFILE'), 'Documents','R','win-library', paste0('R-', R.version$major, '.', R.version$minor))
dir.create(userlib, recursive = TRUE, showWarnings = FALSE)
.libPaths(userlib)
for(p in pkgs) if(!requireNamespace(p, quietly = TRUE)) install.packages(p, repos='https://cran.rstudio.com', lib = userlib)
library(readr); library(dplyr); library(rpart); library(tibble)

# helper: métricas básicas a partir de vectores truth/pred
confusion_metrics <- function(truth, pred){
  tp <- sum(truth == 1 & pred == 1, na.rm=TRUE)
  tn <- sum(truth == 0 & pred == 0, na.rm=TRUE)
  fp <- sum(truth == 0 & pred == 1, na.rm=TRUE)
  fn <- sum(truth == 1 & pred == 0, na.rm=TRUE)
  n <- length(truth)
  acc <- (tp+tn)/n
  prec <- if((tp+fp)==0) NA else tp/(tp+fp)
  sens <- if((tp+fn)==0) NA else tp/(tp+fn)
  spec <- if((tn+fp)==0) NA else tn/(tn+fp)
  list(counts = tibble(TP=tp,TN=tn,FP=fp,FN=fn), metrics = tibble(accuracy=acc, precision=prec, sensitivity=sens, specificity=spec))
}

# create_folds: vector de índices por fold
create_folds <- function(n, k=10, seed=NULL){ if(!is.null(seed)) set.seed(seed); ids <- sample.int(n); split(ids, rep(1:k, length.out=n)) }

# cross_validation: retorna tabla por fold y resumen (mean, sd)
cross_validation <- function(df, k=10, seed=123, formula=NULL){
  if(is.null(formula)) formula <- formula(inclinacion_peligrosa ~ altura + circ_tronco_cm + lat + long + nombre_seccion + especie)
  folds <- create_folds(nrow(df), k=k, seed=seed)
  res_list <- vector('list', length(folds))
  counts_list <- vector('list', length(folds))
  for(i in seq_along(folds)){
    test_idx <- folds[[i]]
    train_idx <- setdiff(seq_len(nrow(df)), test_idx)
    train <- df[train_idx, , drop=FALSE]; test <- df[test_idx, , drop=FALSE]
    # asegura factores coherentes
    train$nombre_seccion <- as.factor(train$nombre_seccion); train$especie <- as.factor(train$especie); train$inclinacion_peligrosa <- as.integer(train$inclinacion_peligrosa)
    test$nombre_seccion <- factor(test$nombre_seccion, levels=levels(train$nombre_seccion)); test$especie <- factor(test$especie, levels=levels(train$especie)); test$inclinacion_peligrosa <- as.integer(test$inclinacion_peligrosa)
    model <- rpart::rpart(formula, data=train, method='class')
    preds <- suppressWarnings(as.integer(as.character(predict(model, test, type='class'))))
    if(all(is.na(preds))){ lvls <- levels(predict(model, test, type='class')); preds <- as.integer(match(predict(model, test, type='class'), lvls)-1) }
    cm <- confusion_metrics(test$inclinacion_peligrosa, preds)
    res_list[[i]] <- cm$metrics %>% mutate(Fold=i)
    counts_list[[i]] <- cm$counts %>% mutate(Fold=i)
  }
  metrics_tbl <- bind_rows(res_list)
  counts_tbl <- bind_rows(counts_list)
  summary_tbl <- metrics_tbl %>% summarise(across(where(is.numeric), list(mean=~mean(., na.rm=TRUE), sd=~sd(., na.rm=TRUE))))
  list(per_fold=metrics_tbl, counts=counts_tbl, summary=summary_tbl)
}

# Ejecuta 10-fold CV y guarda resultados
train_path <- 'tp7-ml/data/arbolado-mendoza-dataset-train.csv'
if(!file.exists(train_path)) stop('Falta: ', train_path)
df <- read_csv(train_path, show_col_types=FALSE)
cat('Ejecutando 10-fold CV...\n')
cv <- cross_validation(df, k=10, seed=42)
write_csv(cv$per_fold, 'tp7-ml/code/eda-clasif-cv/cv_per_fold_metrics.csv')
write_csv(cv$counts, 'tp7-ml/code/eda-clasif-cv/cv_per_fold_counts.csv')
