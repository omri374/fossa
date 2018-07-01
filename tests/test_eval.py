"""Test evaluation functionality."""
import math
import os

import pandas as pd

from fossa import LatestWindowAnomalyDetector
from fossa.eval import read_data, eval_models, f_beta

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def test_read_data():
    path = 'dummy.txt'
    df = read_data(path)
    index = df.index
    # assert index is pd.MultiIndex
    assert len(df) == 16
    assert isinstance(df.index, pd.MultiIndex)

def test_eval_models_all_true():
    path = os.path.join(THIS_DIR, os.pardir, 'tests/dummy2.txt')
    df = read_data(path)

    from tests.mock_model import MockModel
    model = MockModel()
    models = [model]
    X = df[['value']]
    y = df[['is_anomaly']]
    res = eval_models(X, y, models)
    assert res['MockModel()']['f1'] == 1.0
    assert res['MockModel()']['precision'] == 1.0
    assert res['MockModel()']['recall'] == 1.0

def test_eval_models_all_false():
    path = os.path.join(THIS_DIR, os.pardir, 'tests/dummy2.txt')
    df = read_data(path)
    df['is_anomaly'] = 0
    from tests.mock_model import MockModel
    model = MockModel()
    models = [model]
    X = df[['value']]
    y = df[['is_anomaly']]
    res = eval_models(X, y, models)
    print(res)
    assert math.isnan(res['MockModel()']['f1'])
    assert res['MockModel()']['precision'] == 0.0
    assert math.isnan(res['MockModel()']['recall'])

def test_eval_models_half_false():
    path = os.path.join(THIS_DIR, os.pardir, 'tests/dummy2.txt')
    df = read_data(path)
    df['is_anomaly'] = 0
    df.iloc[-1]['is_anomaly'] = 1
    df.iloc[-2]['is_anomaly'] = 1
    from tests.mock_model import MockModel
    model = MockModel()
    models = [model]
    X = df[['value']]
    y = df[['is_anomaly']]
    res = eval_models(X, y, models)
    print(res)
    assert res['MockModel()']['precision'] == 0.5
    assert res['MockModel()']['recall'] == 1.0

def test_real_model():
    path = os.path.join(THIS_DIR, os.pardir, 'tests/dummy.txt')
    df = read_data(path)
    model = LatestWindowAnomalyDetector(p_threshold=0.05)
    models = [model]
    X = df[['value']]
    y = df[['is_anomaly']]
    res = eval_models(X, y, models)
    print(res)


def test_f_beta1():
    precision = 0.6
    recall = 1.0
    beta = 1
    f = f_beta(precision, recall, beta)
    assert (f > 0.74) and (f < 0.76)

def test_f_beta3():
    precision = 0.6
    recall = 1.0
    beta = 3
    f = f_beta(precision, recall, beta)
    assert (f > 0.937) and (f < 0.938)


if __name__ == '__main__':
    test_read_data()
    test_eval_models_all_true()
    test_eval_models_all_false()
    test_eval_models_half_false()
    test_f_beta1()
    test_f_beta3()

    test_real_model()
