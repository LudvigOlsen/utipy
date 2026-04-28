import importlib

import numpy as np
import pandas as pd
import pytest

resemble_module = importlib.import_module("utipy.pandas.resemble")


def test_resemble_shuffle_returns_shuffled_copy_with_original_dtype(monkeypatch):

    def reverse_in_place(values):
        values[:] = values[::-1]

    monkeypatch.setattr(resemble_module, "shuffle", reverse_in_place)

    x = pd.Series([1, 2, 3, 4])

    generated = resemble_module.resemble(x, distribution="shuffle")

    assert isinstance(generated, np.ndarray)
    assert generated.dtype == x.dtype
    assert generated.tolist() == [4, 3, 2, 1]
    assert x.tolist() == [1, 2, 3, 4]


def test_resemble_sampling_distributions_return_expected_dtype_and_values(monkeypatch):

    x = pd.Series([2, 2, 2, 2], dtype="int64")

    def fake_uniform(low, high, size):
        assert low == 2
        assert high == 2
        assert size == 4
        return np.array([2.9, 2.1, 2.0, 2.5])

    def fake_normal(loc, scale, size):
        assert loc == 2
        assert scale == 0
        assert size == 4
        return np.array([2.9, 2.1, 2.0, 2.5])

    def fake_poisson(lam, size):
        assert lam == 2
        assert size == 4
        return np.array([2, 3, 1, 0])

    monkeypatch.setattr(resemble_module.np.random, "uniform", fake_uniform)
    monkeypatch.setattr(resemble_module.np.random, "normal", fake_normal)
    monkeypatch.setattr(resemble_module.np.random, "poisson", fake_poisson)

    uniform = resemble_module.resemble(x, distribution="uniform")
    gaussian = resemble_module.resemble(x, distribution="gaussian")
    robust_gaussian = resemble_module.resemble(x, distribution="robust gaussian")
    poisson = resemble_module.resemble(x, distribution="poisson")

    assert uniform.dtype == x.dtype
    assert gaussian.dtype == x.dtype
    assert robust_gaussian.dtype == x.dtype
    assert poisson.dtype == x.dtype
    assert uniform.tolist() == [2, 2, 2, 2]
    assert gaussian.tolist() == [2, 2, 2, 2]
    assert robust_gaussian.tolist() == [2, 2, 2, 2]
    assert poisson.tolist() == [2, 3, 1, 0]


def test_resemble_unknown_distribution_raises_value_error():

    with pytest.raises(ValueError, match="Unknown distribution"):
        resemble_module.resemble([1, 2, 3], distribution="bad")
