# Codebook

{% for var, json_var in stat %}
## Variable {{ loop.index }}: {{ var["name"] }} - {{ var["label"] }}

:---- VARIABLE ----:
{{ json_var }}
:------------------:
    
{% endfor %}
