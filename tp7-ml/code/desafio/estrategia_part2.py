#!/usr/bin/env python3
"""Optuna hyperparameter tuning for XGBoost using OOF StratifiedKFold and target-encoding.

Outputs:
- out_full/optuna_study.json (best params)
- out_full/metrics_optuna.json (best OOF AUC)
- out_full/submission_kaggle_test_optuna.csv
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier
import joblib

def altura_to_numeric(s: str):
    if pd.isna(s):
        return np.nan
    s = str(s)
    import re
    m = re.search(r"(\d+)\s*-\s*(\d+)", s)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return (a + b) / 2.0
    m = re.search(r">\s*(\d+)", s)
    if m:
        v = int(m.group(1))
        return v + 2.0
    m = re.search(r"(\d+)", s)
    if m:
        return float(m.group(1))
    return np.nan

def map_diametro(s: str):
    if pd.isna(s):
        return np.nan
    s = str(s).strip().lower()
    if s.startswith("ch") or "chico" in s:
        return 1.0
    if s.startswith("me") or "mediano" in s:
        return 2.0
    if s.startswith("gra") or "grande" in s:
        return 3.0
    try:
        return float(s)
    except Exception:
        return np.nan

def prepare_basic(df: pd.DataFrame):
    df = df.copy()
    df['circ_tronco_cm'] = pd.to_numeric(df['circ_tronco_cm'], errors='coerce')
    df['area_seccion'] = pd.to_numeric(df['area_seccion'], errors='coerce')
    df['altura_m'] = df['altura'].apply(altura_to_numeric)
    df['diametro_num'] = df['diametro_tronco'].apply(map_diametro)
    df['circ_altura_ratio'] = df['circ_tronco_cm'] / df['altura_m'].replace({0:np.nan})
    df['diam_circ_ratio'] = df['circ_tronco_cm'] / df['diametro_num'].replace({0:np.nan})
    return df

def compute_te_map(tr_df, col, target, alpha=20):
    agg = tr_df.groupby(col)[target].agg(['count','mean']).reset_index()
    global_mean = tr_df[target].mean()
    agg['te'] = (agg['mean'] * agg['count'] + global_mean * alpha) / (agg['count'] + alpha)
    return dict(zip(agg[col], agg['te'])), global_mean

def apply_te(series, te_map, global_mean):
    return series.map(lambda x: te_map.get(x, global_mean))

def objective(trial):
    # hyperparameter search space
    params = {
        'max_depth': trial.suggest_int('max_depth', 3, 9),
        'learning_rate': trial.suggest_loguniform('learning_rate', 0.01, 0.3),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.4, 1.0),
        'reg_alpha': trial.suggest_loguniform('reg_alpha', 1e-8, 10.0),
        'reg_lambda': trial.suggest_loguniform('reg_lambda', 1e-8, 10.0),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'gamma': trial.suggest_float('gamma', 0.0, 5.0),
    }

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    oof = np.zeros(len(df))
    test_preds_local = np.zeros(len(df_test))

    for tr_idx, val_idx in skf.split(df, df['inclinacion_peligrosa']):
        tr = df.iloc[tr_idx].copy()
        va = df.iloc[val_idx].copy()

        te_es_map, gmean = compute_te_map(tr, 'especie', 'inclinacion_peligrosa', alpha=20)
        te_sec_map, _ = compute_te_map(tr, 'nombre_seccion', 'inclinacion_peligrosa', alpha=20)

        tr['te_especie'] = apply_te(tr['especie'], te_es_map, gmean)
        tr['te_seccion'] = apply_te(tr['nombre_seccion'], te_sec_map, gmean)
        va['te_especie'] = apply_te(va['especie'], te_es_map, gmean)
        va['te_seccion'] = apply_te(va['nombre_seccion'], te_sec_map, gmean)

        Xt = df_test.copy()
        Xt['te_especie'] = apply_te(Xt['especie'], te_es_map, gmean)
        Xt['te_seccion'] = apply_te(Xt['nombre_seccion'], te_sec_map, gmean)

        Xtr = tr[features].fillna(-999)
        ytr = tr['inclinacion_peligrosa'].astype(int)
        Xv = va[features].fillna(-999)
        yv = va['inclinacion_peligrosa'].astype(int)

        neg = (ytr==0).sum(); pos=(ytr==1).sum()
        scale_pos_weight = neg / max(1, pos)

        model = XGBClassifier(n_estimators=1000, use_label_encoder=False, eval_metric='logloss', n_jobs=4,
                              scale_pos_weight=scale_pos_weight, random_state=42, **params)
        try:
            model.fit(Xtr, ytr, eval_set=[(Xv,yv)], early_stopping_rounds=30, verbose=False)
        except TypeError:
            model.fit(Xtr, ytr, eval_set=[(Xv,yv)], verbose=False)

        oof[val_idx] = model.predict_proba(Xv)[:,1]
        test_preds_local += model.predict_proba(Xt[features].fillna(-999))[:,1]

    test_preds_local /= skf.n_splits
    auc = roc_auc_score(df['inclinacion_peligrosa'], oof)
    return auc

def run_optuna(n_trials=30):
    import optuna
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)
    return study

if __name__ == '__main__':
    repo_root = Path(__file__).resolve().parents[3]
    data_dir = repo_root / 'tp7-ml' / 'data'
    train_csv = data_dir / 'arbolado-mza-dataset.csv'
    test_csv = data_dir / 'arbolado-mza-dataset-test.csv'
    valid_csv = data_dir / 'arbolado-mendoza-dataset-validation.csv'

    out_dir = Path(__file__).resolve().parent / 'out_full'
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(train_csv)
    df = prepare_basic(df)
    df_test = pd.read_csv(test_csv)
    df_test = prepare_basic(df_test)

    features = ['circ_tronco_cm','area_seccion','altura_m','diametro_num','circ_altura_ratio','diam_circ_ratio','te_especie','te_seccion','lat','long']

    # run Optuna
    try:
        study = run_optuna(n_trials=30)
    except Exception as e:
        print('Optuna failed:', e)
        raise

    best = study.best_params
    print('Best params:', best)
    with open(out_dir / 'optuna_study.json','w',encoding='utf8') as f:
        json.dump({'best_params': best, 'best_value': study.best_value}, f, indent=2)

    # Retrain final model on full train using best params, with early stopping on provided validation set
    df_full = pd.read_csv(train_csv)
    df_full = prepare_basic(df_full)
    df_val = pd.read_csv(valid_csv)
    df_val = prepare_basic(df_val)

    te_es_map, gmean = compute_te_map(df_full, 'especie', 'inclinacion_peligrosa', alpha=20)
    te_sec_map, _ = compute_te_map(df_full, 'nombre_seccion', 'inclinacion_peligrosa', alpha=20)
    df_full['te_especie'] = apply_te(df_full['especie'], te_es_map, gmean)
    df_full['te_seccion'] = apply_te(df_full['nombre_seccion'], te_sec_map, gmean)
    df_val['te_especie'] = apply_te(df_val['especie'], te_es_map, gmean)
    df_val['te_seccion'] = apply_te(df_val['nombre_seccion'], te_sec_map, gmean)
    df_test['te_especie'] = apply_te(df_test['especie'], te_es_map, gmean)
    df_test['te_seccion'] = apply_te(df_test['nombre_seccion'], te_sec_map, gmean)

    X_full = df_full[features].fillna(-999)
    y_full = df_full['inclinacion_peligrosa'].astype(int)
    Xv = df_val[features].fillna(-999)
    yv = df_val['inclinacion_peligrosa'].astype(int)

    neg = (y_full==0).sum(); pos=(y_full==1).sum()
    scale_pos_weight = neg / max(1, pos)

    final_model = XGBClassifier(n_estimators=2000, use_label_encoder=False, eval_metric='logloss', n_jobs=4,
                                scale_pos_weight=scale_pos_weight, random_state=42, **best)
    try:
        final_model.fit(X_full, y_full, eval_set=[(Xv,yv)], early_stopping_rounds=50, verbose=True)
    except TypeError:
        final_model.fit(X_full, y_full, eval_set=[(Xv,yv)], verbose=True)

    joblib.dump(final_model, out_dir / 'xgb_model_optuna.joblib')

    # predict on test and save submission
    proba_t = final_model.predict_proba(df_test[features].fillna(-999))[:,1]
    pred_t = (proba_t >= 0.5).astype(int)
    sub = pd.DataFrame({'ID': df_test['id'].astype(int), 'inclinacion_peligrosa': pred_t})
    sub_path = out_dir / 'submission_kaggle_test_optuna.csv'
    sub.to_csv(sub_path, index=False)

    # compute OOF of best model using StratifiedKFold to report OOF AUC
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    oof = np.zeros(len(df))
    for tr_idx, val_idx in skf.split(df, df['inclinacion_peligrosa']):
        tr = df.iloc[tr_idx].copy()
        va = df.iloc[val_idx].copy()
        te_es_map_t, gmean_t = compute_te_map(tr, 'especie', 'inclinacion_peligrosa', alpha=20)
        te_sec_map_t, _ = compute_te_map(tr, 'nombre_seccion', 'inclinacion_peligrosa', alpha=20)
        tr['te_especie'] = apply_te(tr['especie'], te_es_map_t, gmean_t)
        tr['te_seccion'] = apply_te(tr['nombre_seccion'], te_sec_map_t, gmean_t)
        va['te_especie'] = apply_te(va['especie'], te_es_map_t, gmean_t)
        va['te_seccion'] = apply_te(va['nombre_seccion'], te_sec_map_t, gmean_t)
        model = XGBClassifier(n_estimators=1000, use_label_encoder=False, eval_metric='logloss', n_jobs=4,
                              scale_pos_weight=scale_pos_weight, random_state=42, **best)
        try:
            model.fit(tr[features].fillna(-999), tr['inclinacion_peligrosa'].astype(int),
                      eval_set=[(va[features].fillna(-999), va['inclinacion_peligrosa'].astype(int))], early_stopping_rounds=30, verbose=False)
        except TypeError:
            model.fit(tr[features].fillna(-999), tr['inclinacion_peligrosa'].astype(int),
                      eval_set=[(va[features].fillna(-999), va['inclinacion_peligrosa'].astype(int))], verbose=False)
        oof[val_idx] = model.predict_proba(va[features].fillna(-999))[:,1]

    oof_auc = float(roc_auc_score(df['inclinacion_peligrosa'], oof))
    with open(out_dir / 'metrics_optuna.json','w',encoding='utf8') as f:
        json.dump({'oof_roc_auc': oof_auc}, f, indent=2)

    print('Final submission saved:', sub_path)
    print('OOF AUC final:', oof_auc)
