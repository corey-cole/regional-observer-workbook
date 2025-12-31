from regional_observer_workbook.form_original import (
    load,
    load_bounding_boxes,
    load_named_fields,
)
from regional_observer_workbook.consts import FormName, PS4_SAMPLING_DATA, Revision
import numpy as np
import pytest


def test_load_existing_asset():
    img = load(Revision.v2018, FormName.PS4, "page1")
    assert img is not None
    assert isinstance(img, np.ndarray)
    assert img.ndim == 2  # Grayscale image should have 2 dimensions


def test_load_nonexistent_asset():
    with pytest.raises(FileNotFoundError) as exc_info:
        load(Revision.v2018, FormName.PS4, "nonexistent_page")
        assert "No such file" in str(exc_info.value)


def test_load_bounding_boxes_existing_asset():
    bboxes = load_bounding_boxes(Revision.v2018, FormName.PS4, PS4_SAMPLING_DATA)
    assert bboxes is not None
    assert isinstance(bboxes, np.ndarray)
    assert bboxes.ndim >= 1  # Bounding boxes should have at least 1 dimension

def test_load_named_fields():
    field_data = load_named_fields(Revision.v2018, FormName.PS4)
    assert field_data is not None
    assert isinstance(field_data.observer_name, list)
