import pathlib
import pytest
from utipy.path import IOPaths
from utipy.path.prepare_paths import prepare_in_out_paths

CONTENT = "content"


def _empty_path_collections():
    return {
        "in_files": None,
        "in_dirs": None,
        "out_files": None,
        "out_dirs": None,
        "tmp_files": None,
        "tmp_dirs": None,
    }


def test_create_file(tmp_path):
    """
    This tests that the tmp path operations work on the current system.
    """
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(CONTENT)
    assert p.read_text() == CONTENT
    assert len(list(tmp_path.iterdir())) == 1


def test_in_out_paths_works(tmp_path):
    in_dir = tmp_path / "in"
    out_dir = tmp_path / "out"
    in_dir.mkdir()

    txt_file_path = in_dir / "x.txt"
    txt_file_path.write_text(CONTENT)
    assert txt_file_path.read_text() == CONTENT

    in_files = {
        "txt_file": txt_file_path,
        "stream": "-",
    }
    in_dirs = {
        "input_dir": str(in_dir),
    }
    out_dirs = {
        "out_dir": out_dir,
    }
    out_files = {
        "new_txt_file": out_dir / f"new.txt",
        "new_txt_file_2": str(out_dir / f"new_2.txt"),
    }

    # Create paths container with checks

    paths = IOPaths(
        in_files=in_files,
        in_dirs=in_dirs,
        out_files=out_files,
        out_dirs=out_dirs,
    )

    print(paths)

    # Create output directory
    paths.mk_output_dirs(collection="out_dirs")
    assert out_dir.is_dir()

    assert paths["txt_file"] == pathlib.Path(in_files["txt_file"])
    assert paths["stream"] == "-"
    assert paths["input_dir"] == pathlib.Path(in_dirs["input_dir"])
    assert paths["out_dir"] == pathlib.Path(out_dirs["out_dir"])
    assert paths["new_txt_file"] == pathlib.Path(out_files["new_txt_file"])
    assert paths["new_txt_file_2"] == pathlib.Path(out_files["new_txt_file_2"])


def test_io_paths_creates_out_files_dirs(tmp_path):
    out_dir = tmp_path / "out"

    out_dirs = {
        "out_dir": out_dir,
    }
    out_files = {
        "new_txt_file": out_dir / "subsub" / f"new.txt",
        "new_txt_file_2": str(out_dir / "subsub2" / f"new_2.txt"),
    }

    # Create paths container with checks

    paths = IOPaths(out_files=out_files, out_dirs=out_dirs)

    print(paths)

    # Create output directory
    paths.mk_output_dirs(collection="out_files")
    assert out_dir.is_dir()
    assert (out_dir / "subsub").is_dir()
    assert (out_dir / "subsub2").is_dir()


def test_io_paths_empty(tmp_path):
    paths = IOPaths()
    paths.set_path("out_dir", tmp_path / "out", "out_dirs")


def test_in_out_paths_fails(tmp_path):
    # TODO Test all the cases where it should raise an error

    # TODO Test duplicates are found correctly
    pass


def test_prepare_paths_missing_input_file_raises_file_not_found(tmp_path):
    collections = _empty_path_collections()
    collections["in_files"] = {"missing_file": tmp_path / "missing.txt"}

    with pytest.raises(FileNotFoundError, match="missing_file"):
        prepare_in_out_paths(collections)


def test_prepare_paths_existing_output_file_raises_file_exists(tmp_path):
    existing_file = tmp_path / "existing.txt"
    existing_file.write_text(CONTENT)

    collections = _empty_path_collections()
    collections["out_files"] = {"existing_file": existing_file}

    with pytest.raises(FileExistsError, match="existing_file"):
        prepare_in_out_paths(collections, allow_overwriting=False)


def test_prepare_paths_existing_tmp_dir_raises_file_exists(tmp_path):
    tmp_dir = tmp_path / "existing_tmp"
    tmp_dir.mkdir()

    collections = _empty_path_collections()
    collections["tmp_dirs"] = {"tmp_dir": tmp_dir}

    with pytest.raises(FileExistsError, match="tmp_dir"):
        prepare_in_out_paths(collections)


def test_io_paths_invalid_argument_types_raise_type_error():
    paths = IOPaths()

    with pytest.raises(TypeError, match="name"):
        paths.get_collection(1)

    with pytest.raises(TypeError, match="path"):
        paths.set_path("out", object(), "out_files")

    with pytest.raises(TypeError, match="paths"):
        paths.set_paths([], "out_files")

    with pytest.raises(TypeError, match="other"):
        paths.update(object())

    with pytest.raises(TypeError, match="other"):
        paths.difference(object())

    assert (paths == object()) is False


def test_rm_tmp_dirs_none_raises_value_error():
    paths = IOPaths()

    with pytest.raises(ValueError, match="tmp_dirs"):
        paths.rm_tmp_dirs(messenger=None)


def test_rm_tmp_dirs_with_rm_paths_false_keeps_nested_path_entries(tmp_path):
    parent_tmp_dir = tmp_path / "tmp_parent"
    child_tmp_dir = parent_tmp_dir / "tmp_child"

    paths = IOPaths(
        tmp_dirs={
            "parent_tmp_dir": parent_tmp_dir,
            "child_tmp_dir": child_tmp_dir,
        }
    )
    paths.mk_output_dirs(collection="tmp_dirs", messenger=None)

    assert parent_tmp_dir.is_dir()
    assert child_tmp_dir.is_dir()

    paths.rm_tmp_dirs(rm_paths=False, messenger=None)

    assert not parent_tmp_dir.exists()
    assert not child_tmp_dir.exists()
    assert set(paths.get_collection("tmp_dirs").keys()) == {
        "parent_tmp_dir",
        "child_tmp_dir",
    }
    assert set(paths.all_paths.keys()) == {"parent_tmp_dir", "child_tmp_dir"}


def test_rm_tmp_dirs_removes_nested_path_entries(tmp_path):
    parent_tmp_dir = tmp_path / "tmp_parent"
    child_tmp_dir = parent_tmp_dir / "tmp_child"
    tmp_file = child_tmp_dir / "tmp.txt"

    paths = IOPaths(
        tmp_files={"tmp_file": tmp_file},
        tmp_dirs={
            "parent_tmp_dir": parent_tmp_dir,
            "child_tmp_dir": child_tmp_dir,
        },
    )
    paths.mk_output_dirs(collection="tmp_dirs", messenger=None)
    tmp_file.write_text(CONTENT)

    paths.rm_tmp_dirs(messenger=None)

    assert not parent_tmp_dir.exists()
    assert paths.get_collection("tmp_dirs") == {}
    assert paths.get_collection("tmp_files") == {}
    assert paths.all_paths == {}


def test_stream_path_is_rejected_outside_in_files():
    with pytest.raises(ValueError, match="only allowed"):
        IOPaths(tmp_dirs={"stream": "-"})
