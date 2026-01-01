# PS-4

## Description

This document describes the available fields for this form and revision

{% set form = load_form_data("2018", "PS-4") %}

{% import 'renderers.md' as tables %}

{% set table_rows %}
{{ tables.render_field_table(form) }}
{% endset %}

This form has four "cellular" bounding boxes:

`sampling-patterns` is the 24x2 table containing brail fullness and samples per brail.
`sample-data` is the species and length data.
`column-totals` is the count/sum-of-lengths data that appears directly under the sample data.
`page-totals` is the calculation of average length by species at the bottom of the form.

Note that all forms are accessed by row and column, and that both row and column start at zero rather than one.
For example, this means that the species code and length in box 1 are access as cell 0 and cell 1 in row 0.
Box 2 is cell 1 and cell 1 in row 1, while box 21 is cell 2 and cell 3 in row 0.

The `brail_tallies` bounding boxes are unique on this form in that they are subtractive.  The box for an
individual tally field also includes the entire box for the associated count.  When performing OCR,
it may be a requirement to either focus on `count` or ensure that the `count` field is erased prior to
performing OCR on the `tally` field.

The table below describes the named fields available from the `load_named_fields` call.
| Property Name | Type |
| :--- | :--- |
{{ table_rows.strip() }}