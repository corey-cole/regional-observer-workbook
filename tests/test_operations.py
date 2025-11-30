from regional_observer_workbook.operations import get_cell
import numpy as np
import pytest


@pytest.mark.parametrize("row,column", [(4, 5), (0, 5)])
def test_bounds_checking(row, column):
    fake_image = np.zeros((100, 100), dtype=np.uint8)
    fake_bbox = np.zeros((5, 5, 4), dtype=np.int32)
    with pytest.raises(IndexError):
        get_cell(row, column, fake_image, fake_bbox)
