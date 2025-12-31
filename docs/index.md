# Regional Observer Workbook

This library contains utilities for performing OCR on SPC/FFA Regional Observer Workbooks.  It can align scanned documents
to a fixed frame of reference provided by the print master of a form.  It also provides named access to bounding boxes
of form fields in a Pythonic fashion.

Actual OCR happens elsewhere.  See [this repository](https://github.com/corey-cole/ps4-ocr-demo) for a demo of how to use this library and
OCR models from Huggingface Transformers for complete OCR.

## Installation

The library is published to PyPI and can be installed via `pip install regional-observer-workbook` 

## Usage

```python
from regional_observer_workbook.consts import (
    FormName,
    Revision,
)
from regional_observer_workbook.form_original import load, load_bounding_boxes
from regional_observer_workbook.operations import (
    align_to_original,
    get_cell,
    image_as_grayscale,
)

original = load(revision=Revision.v2018, form_name=FormName.PS4)
bbox_grid = load_bounding_boxes(
    revision=Revision.v2018, form_name=FormName.PS4, bbox_name="sample-data"
)

scan_image = image_as_grayscale(cv2.imread("clc_test_scan.png"))
if scan_image is None:
    raise ValueError("Unable to load sample image")

# Scan has been aligned to enable use of "get_cell" method from library
scan_image = align_to_original(
    scan_image,
    original,
    max_features=1500,
    keep_percent=0.2,
)
# species_code_1 contains numpy array representation of the contents
# of the species code half of box #1 from the scanned PS-4
species_code_1 = get_cell(0, 0, scan_image, bbox_grid)
```




