"""
Tests for httpie/cli/dicts.py

Place this file inside the `tests/` folder of the cli_darkknight (httpie)
project, then run:

    python -m pytest tests/test_dicts.py -v
"""

import pytest
from httpie.cli.dicts import (
    BaseMultiDict,
    HTTPHeadersDict,
    RequestJSONDataDict,
)


class TestBaseMultiDict:
    def test_is_a_multidict(self):
        d = BaseMultiDict()
        d.add("a", "1")
        d.add("a", "2")
        assert d.getall("a") == ["1", "2"]


class TestHTTPHeadersDict:
    def test_basic_add_and_get(self):
        headers = HTTPHeadersDict()
        headers.add("Content-Type", "application/json")
        assert headers["Content-Type"] == "application/json"

    def test_case_insensitive(self):
        headers = HTTPHeadersDict()
        headers.add("Content-Type", "application/json")
        # Headers should be retrievable regardless of case
        assert headers["content-type"] == "application/json"
        assert headers["CONTENT-TYPE"] == "application/json"

    def test_add_supports_multiple_values(self):
        headers = HTTPHeadersDict()
        headers.add("X-Custom", "one")
        headers.add("X-Custom", "two")
        assert headers.getall("X-Custom") == ["one", "two"]

    def test_add_none_overwrites_previous_values(self):
        headers = HTTPHeadersDict()
        headers.add("X-Custom", "one")
        headers.add("X-Custom", "two")
        # Passing None should wipe out prior values and set it to None
        headers.add("X-Custom", None)
        assert headers.getall("X-Custom") == [None]

    def test_add_after_none_replaces_none(self):
        headers = HTTPHeadersDict()
        headers.add("X-Custom", None)
        headers.add("X-Custom", "real-value")
        # The None placeholder should be discarded once a real value is given
        assert headers.getall("X-Custom") == ["real-value"]

    def test_remove_item(self):
        headers = HTTPHeadersDict()
        headers.add("X-Custom", "one")
        headers.add("X-Custom", "two")
        headers.add("X-Custom", "three")

        headers.remove_item("X-Custom", "two")

        assert headers.getall("X-Custom") == ["one", "three"]

    def test_remove_item_removes_only_matching_value(self):
        headers = HTTPHeadersDict()
        headers.add("X-Custom", "dup")
        headers.add("X-Custom", "dup")
        headers.add("X-Custom", "keep")

        headers.remove_item("X-Custom", "dup")

        # remove() only removes the first match, so one "dup" should remain
        assert headers.getall("X-Custom") == ["dup", "keep"]

    def test_remove_item_raises_if_value_not_present(self):
        headers = HTTPHeadersDict()
        headers.add("X-Custom", "one")
        with pytest.raises(ValueError):
            headers.remove_item("X-Custom", "does-not-exist")


class TestRequestJSONDataDict:
    def test_behaves_like_ordered_dict(self):
        d = RequestJSONDataDict()
        d["b"] = 2
        d["a"] = 1
        # Insertion order should be preserved
        assert list(d.keys()) == ["b", "a"]
        assert d["a"] == 1
        assert d["b"] == 2
        
print('AFA_PAPA')