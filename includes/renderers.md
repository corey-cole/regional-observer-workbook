{% macro render_field_table(data, parent='') -%}
  {%- for key, value in data.items() -%}
    {%- set current_path = (parent ~ '.' ~ key) if parent else key -%}
    
    {%- if value is mapping and 'type' not in value -%}
      {{- render_field_table(value, current_path) -}}
    {%- else -%}
| `{{ current_path }}` | {{ value.type if value is mapping else 'text' }} |{{ "\n" }}
    {%- endif -%}
  {%- endfor -%}
{%- endmacro %}