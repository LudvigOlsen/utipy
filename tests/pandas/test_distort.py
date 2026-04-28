import importlib

import numpy as np
import pandas as pd
import pytest

distort_module = importlib.import_module("utipy.pandas.distort")


def test_distort_blends_numeric_columns_with_expected_values(monkeypatch):

    def add_twenty(values, distribution):
        return values.to_numpy() + 20

    monkeypatch.setattr(distort_module, "resemble", add_twenty)

    df = pd.DataFrame({"a": [10, 20], "b": [100, 200]})

    distorted = distort_module.distort(df, distribution="shuffle", amount=0.5)

    expected = pd.DataFrame({"a": [20.0, 30.0], "b": [110.0, 210.0]})
    assert distorted.equals(expected)


def test_distort_excluded_columns_are_real_nan_and_preserve_index(monkeypatch):

    def add_ten(values, distribution):
        return values.to_numpy() + 10

    monkeypatch.setattr(distort_module, "resemble", add_ten)

    df = pd.DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6]},
        index=["row_a", "row_b", "row_c"],
    )

    distorted = distort_module.distort(df, distribution="shuffle", exclude=["b"])

    expected = pd.DataFrame(
        {"a": [11, 12, 13], "b": [np.nan, np.nan, np.nan]},
        index=["row_a", "row_b", "row_c"],
    )
    assert distorted.equals(expected)
    assert distorted["b"].isna().all()


def test_distort_label_column_can_be_kept_or_replaced(monkeypatch):

    def add_one(values, distribution):
        return values.to_numpy() + 1

    monkeypatch.setattr(distort_module, "resemble", add_one)

    df = pd.DataFrame({"a": [1, 2], "label": ["x", "y"]})

    kept = distort_module.distort(df, distribution="shuffle", label_column="label")
    replaced = distort_module.distort(
        df,
        distribution="shuffle",
        label_column="label",
        keep_labels=False,
        new_label="noise",
    )

    assert kept.equals(pd.DataFrame({"a": [2, 3], "label": ["x", "y"]}))
    assert replaced.equals(pd.DataFrame({"a": [2, 3], "label": ["noise", "noise"]}))


def test_distort_requires_nonnumeric_columns_to_be_label_or_excluded():
    df = pd.DataFrame({"a": [1, 2], "category": ["x", "y"]})

    with pytest.raises(ValueError, match="Only numeric columns"):
        distort_module.distort(df, distribution="shuffle")


def test_distort_validates_amount_and_size():
    df = pd.DataFrame({"a": [1, 2]})

    with pytest.raises(ValueError, match="amount"):
        distort_module.distort(df, amount=1.2)

    with pytest.raises(ValueError, match="size"):
        distort_module.distort(df, size=-0.1)


def test_distort_validates_label_and_excluded_columns():
    df = pd.DataFrame({"a": [1, 2]})

    with pytest.raises(ValueError, match="label_column"):
        distort_module.distort(df, label_column="missing")

    with pytest.raises(ValueError, match="exclude"):
        distort_module.distort(df, exclude=["missing"])
