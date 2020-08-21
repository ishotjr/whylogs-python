"""
"""
import datasketches

from whylogs.util import dsketch

EMPTY_HIST_BYTES = b"\x02\x01\x0f\x01\x00\x01\x08\x00"
FULL_HIST_BYTES = b"\x05\x01\x0f\x00\x00\x01\x08\x00d\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x9c\x00\x00\x00\x00\x00\x00\x00\xc3u!C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xcd\xcc\x84A\\\x8f\x86B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc3u!CR\xb8\xb4A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
EMPTY_STRING_SKETCH = b"\x01\x01\n\x05\x03\x04\x00\x00"
FULL_STRING_SKETCH = b"\x04\x01\n\x05\x03\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x13\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00C\x01\x00\x00\x00F\x01\x00\x00\x00B\x01\x00\x00\x00E\x01\x00\x00\x00D\x01\x00\x00\x00A"


def test_deserialize_empty_hist_returns_none():
    x = dsketch.deserialize_kll_floats_sketch(EMPTY_HIST_BYTES)
    assert x is None


def test_deserialize_full_hist_returns_sketch():
    x = dsketch.deserialize_kll_floats_sketch(FULL_HIST_BYTES)
    assert isinstance(x, (datasketches.kll_floats_sketch, datasketches.kll_ints_sketch))
    assert x.get_n() == 100


def test_deserialize_empty_strings_returns_none():
    x = dsketch.deserialize_frequent_strings_sketch(EMPTY_STRING_SKETCH)
    assert x is None


def test_deserialize_full_strings_returns_sketch():
    x = dsketch.deserialize_frequent_strings_sketch(FULL_STRING_SKETCH)
    assert isinstance(x, datasketches.frequent_strings_sketch)
    assert x.get_num_active_items() == 6
    freq_strings = x.get_frequent_items(
        datasketches.frequent_items_error_type.NO_FALSE_NEGATIVES, 7
    )
    assert freq_strings == [
        ("C", 36, 36, 36),
        ("B", 22, 22, 22),
        ("A", 19, 19, 19),
        ("D", 14, 14, 14),
    ]
