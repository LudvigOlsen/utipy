import pandas as pd

import utipy as ut


def test_group_default_first_column_runs_and_adds_balanced_groups():

    df = pd.DataFrame({"x": [10, 20, 30, 40]})

    grouped = ut.group(df, n=2)

    assert grouped.columns.tolist() == ["x", "group"]
    assert grouped["x"].tolist() == [10, 20, 30, 40]
    assert grouped["group"].value_counts().sort_index().to_dict() == {1: 2, 2: 2}


def test_fold_default_first_column_runs_and_removes_sorting_index():

    df = pd.DataFrame({"x": [10, 20, 30, 40]})

    folded = ut.fold(df, n=2)

    assert folded.columns.tolist() == ["x", "group"]
    assert folded["x"].tolist() == [10, 20, 30, 40]
    assert folded["group"].value_counts().sort_index().to_dict() == {1: 2, 2: 2}


def test_partition_default_first_column_runs_and_returns_expected_sizes():

    df = pd.DataFrame({"x": [10, 20, 30, 40]})

    partitions = ut.partition(df, p=0.5)

    assert len(partitions) == 2
    assert sorted([partition.shape for partition in partitions]) == [(2, 1), (2, 1)]
    assert all(partition.columns.tolist() == ["x"] for partition in partitions)

    partition_values = []
    for partition in partitions:
        partition_values.extend(partition["x"].tolist())

    assert sorted(partition_values) == [10, 20, 30, 40]
