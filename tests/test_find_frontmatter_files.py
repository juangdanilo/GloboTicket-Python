from pathlib import Path

import pytest

from globoticket.frontmatter import find_frontmatter_file

FM_PATH = Path(__file__).parent / "product_info"


def test_find_file_toplevel() -> None:
    """
    Locate a yaml file at toplevel directory.
    """
    assert find_frontmatter_file("111222", FM_PATH) == FM_PATH / "111222.yml"


def test_find_file_subdirs() -> None:
    """
    Locate a yaml file in a subdirectory.
    """
    assert find_frontmatter_file("123456", FM_PATH) == FM_PATH / "hiphop" / "123456.yml"
    assert find_frontmatter_file("654321", FM_PATH) == FM_PATH / "reggae" / "654321.yml"


def test_find_file_not_found() -> None:
    """
    Test that a FileNotFoundError is raised if the file is not found.
    """
    with pytest.raises(FileNotFoundError):
        find_frontmatter_file("000000", FM_PATH)
