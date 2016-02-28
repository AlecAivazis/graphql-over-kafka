# {% for service in services %}{{service.title()}} {% endfor %}Connection

A service that manages the relationship between {% for service in services %}{% if loop.last %} and {%endif%}{{service}}s{% if not loop.last and loop|length > 2 %},{%endif%}{% endfor %}
