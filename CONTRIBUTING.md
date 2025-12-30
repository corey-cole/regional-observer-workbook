
## Adding New Forms


### Form Original Image

Convert the print master into a high quality grayscale PNG.  ImageMagick/GraphicsMagick can handle this with an command invocation similar to that below.

```bash
# This assumes a single page PDF document, or that the desired page is the first page
gm convert -quality 100 -density 150 print-master.pdf output-file-name.png
```

Save the file into the `src/regional_observer_workbook/assets` directory using the following naming convention `{Revision}/{Form Name}/page{page number}.png`.

Add the Revision and Form name to `src/regional_observer_workbook/consts.py` (if necessary).



### Bounding Boxes

Bounding boxes are stored as serialized Numpy arrays.  The easiest way to create this files is:

1. Identify the bounding box in column major format.  A bounding box record is "x0,y0,w,h".  A tool like ImageJ is useful as it
can zoom in and provides live x/y coordinates.  For tightly grouped boxes, capture all 4 values for the first row.  For the second row,
capture just `y0` and `h` as `x0` and `w` should be the same for subsequent rows.

2. Save this information in a CSV file.  Excel or Google Sheets may be helpful here.  The format of the CSV should match the example below
(multiple rows have be elided for clarity)

```
Row,Column,x,y,w,h
0,0,45,1433,55,27
0,1,45,1433,96,27
...
1,0,45,1463,55,26
1,1,45,1463,96,26
1,2,45,1463,38,26
```

3. Convert the CSV to Numpy format using code similar to that shown below.
```python
import numpy as np
# Format of tuple argument to `np.zeros` is row_count, column_count, 4
bbox_grid = np.zeros((3,12,4), dtype=int)
raw_data = np.loadtxt('column-totals.csv', delimiter=',', skiprows=1, dtype=int)
rows = raw_data[:,0]
cols = raw_data[:,1]
coords = raw_data[:,2:]
bbox_grid[rows, cols] = coords
"""
# Sample output from REPL
>>> bbox_grid
array([[[  45, 1433,   55,   27],
        [  45, 1433,   96,   27],
        [  45, 1433,   38,   27],
        [  45, 1433,   94,   27],
        [  45, 1433,   43,   27],
        [  45, 1433,   98,   27],
        [  45, 1433,   47,   27],
        [  45, 1433,   89,   27],
        [  45, 1433,   66,   27],
        [  45, 1433,  125,   27],
        [  45, 1433,   44,   27],
        [  45, 1433,  134,   27]],

       [[  45, 1463,   55,   26],
        [  45, 1463,   96,   26],
        [  45, 1463,   38,   26],
        [  45, 1463,   94,   26],
        [  45, 1463,   43,   26],
        [  45, 1463,   98,   26],
        [  45, 1463,   47,   26],
        [  45, 1463,   89,   26],
        [  45, 1463,   66,   26],
        [  45, 1463,  125,   26],
        [  45, 1463,   44,   26],
        [  45, 1463,  134,   26]],

       [[  45, 1492,   55,   33],
        [  45, 1492,   96,   33],
        [  45, 1492,   38,   33],
        [  45, 1492,   94,   33],
        [  45, 1492,   43,   33],
        [  45, 1492,   98,   33],
        [  45, 1492,   47,   33],
        [  45, 1492,   89,   33],
        [  45, 1492,   66,   33],
        [  45, 1492,  125,   33],
        [  45, 1492,   44,   33],
        [  45, 1492,  134,   33]]])
"""
with open('column-totals.npy', 'wb') as f:
    np.save(f, bbox_grid)
```

4. Save the `.npy` file in the `assets` subdirectory that holds the original reference image used to create the bounding boxes.
It is not mandatory, but it is recommended to update `consts.py` with a friendly name for the bounding box.  Check previous revisions for similar bounding box names.

5. The utility CLI published with this package can be used to display the bounding boxes as a final quality control check.

```bash
# Use the form's original as the scan argument
uv run form-extract-cli show-bounding-boxes --output-dir scratch --scan src/regional_observer_workbook/assets/2018/PS-4/page1.png --bounding-box-name columns-totals 
```

If submitting a PR, please include the image output from this invocation as evidence.

The CSV file may be left in the assets directory if desired.  It is not used at runtime, but it is easier to visually inspect than a serialized Numpy file.