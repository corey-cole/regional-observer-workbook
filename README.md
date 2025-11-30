# Regional Observer Workbook

## Background
This Python library encapsulates the logic for extracting content from SPC/FFA regional observer workbooks.
It maintains original images and bounding boxes for forms.  It also includes logic to align scans to an original using
OpenCV's homography capabilities.

In addition to the library, there is a simple CLI utility that can perform two tasks.  The first task is to extract each unique bounding box to an image.
The second task is to draw the bounding boxes on an aligned scan.  The capabilities are useful as examples of how to use the library as well being visual debugging aids.


## Work-in-Progress

Additional form types and bounding boxes for recent purse seine observer workbooks are a work in progress.