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
        {{var["statistics"] }}
        '''
        {% for key, value in var["stat_dict"] %}
            {{key}}: {{value}}
        {% endfor %}
        '''
    {% endif %}
    bi:
    :------------------:
    
{% endfor %}
