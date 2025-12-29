from regional_observer_workbook.operations import get_cell, image_validator
from regional_observer_workbook.errors import InvalidImageError
import numpy as np
import pytest


@pytest.mark.parametrize("row,column", [(4, 5), (0, 5)])
def test_bounds_checking(row, column):
    fake_image = np.zeros((100, 100), dtype=np.uint8)
    fake_bbox = np.zeros((5, 5, 4), dtype=np.int32)
    with pytest.raises(IndexError):
        get_cell(row, column, fake_image, fake_bbox)


class TestImageValidator:
    """Tests for the image_validator function."""

    def test_valid_2d_image(self):
        """Test that a valid 2D uint8 image passes validation."""
        valid_image = np.zeros((100, 100), dtype=np.uint8)
        # Should not raise any exception
        image_validator(valid_image, "test_image")

    def test_valid_3d_image(self):
        """Test that a valid 3D uint8 image passes validation."""
        valid_image = np.zeros((100, 100, 3), dtype=np.uint8)
        # Should not raise any exception
        image_validator(valid_image, "test_image")

    def test_not_ndarray(self):
        """Test that a non-NDArray raises InvalidImageError."""
        with pytest.raises(InvalidImageError, match="test_param is not a NumPy NDArray object"):
            image_validator([1, 2, 3], "test_param")

    def test_not_ndarray_with_different_param_name(self):
        """Test that param name is included in the error message."""
        with pytest.raises(InvalidImageError, match="my_image is not a NumPy NDArray object"):
            image_validator("not an array", "my_image")

    def test_wrong_dimensions_1d(self):
        """Test that a 1D array raises InvalidImageError."""
        image_1d = np.zeros(100, dtype=np.uint8)
        with pytest.raises(InvalidImageError, match="test_image must be a 2D or 3D array"):
            image_validator(image_1d, "test_image")

    def test_wrong_dimensions_4d(self):
        """Test that a 4D array raises InvalidImageError."""
        image_4d = np.zeros((10, 10, 3, 3), dtype=np.uint8)
        with pytest.raises(InvalidImageError, match="test_image must be a 2D or 3D array"):
            image_validator(image_4d, "test_image")

    def test_image_too_small_width(self):
        """Test that an image with width < 10 raises InvalidImageError."""
        small_image = np.zeros((10, 5), dtype=np.uint8)
        with pytest.raises(InvalidImageError, match="test_image image is too small to process"):
            image_validator(small_image, "test_image")

    def test_image_too_small_height(self):
        """Test that an image with height < 10 raises InvalidImageError."""
        small_image = np.zeros((5, 10), dtype=np.uint8)
        with pytest.raises(InvalidImageError, match="test_image image is too small to process"):
            image_validator(small_image, "test_image")

    def test_image_too_small_both_dimensions(self):
        """Test that an image with both dimensions < 10 raises InvalidImageError."""
        small_image = np.zeros((5, 5), dtype=np.uint8)
        with pytest.raises(InvalidImageError, match="test_image image is too small to process"):
            image_validator(small_image, "test_image")

    def test_minimum_valid_size(self):
        """Test that a 10x10 image is valid."""
        min_image = np.zeros((10, 10), dtype=np.uint8)
        # Should not raise any exception
        image_validator(min_image, "test_image")

