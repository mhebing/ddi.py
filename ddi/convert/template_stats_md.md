# Codebook

{% for var in stat %}
## Variable {{ loop.index }}: {{var["variable"]}} – {{var["label"]}}
    :---- VARIABLE ----:
    name: {{var["variable"]}}
    label: {{var["label"]}}
    scale: {{ var["scale"] }}
    uni:
    {% if var["scale"] == "cat" %}
        values: {{var["uni"]["values"]}}
        labels: {{var["uni"]["labels"]}}

        frequencies: {{var["uni"]["frequencies"]}}
        missings: {{var["uni"]["missings"]}}
        statistics:
        {% for key in var["statistics"] %}
            {{key}} = {{var["statistics"][key]}}
        {% endfor %}
    {% endif %}
    bi:
    :------------------:
    
{% endfor %}
