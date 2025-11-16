# orders/templatetags/form_extras.py
from django import template

register = template.Library()

def _merge_classes(original, extra):
    original = (original or "").strip()
    extra = (extra or "").strip()
    if not original:
        return extra
    if not extra:
        return original
    merged = (original + " " + extra).split()
    seen = []
    for c in merged:
        if c not in seen:
            seen.append(c)
    return " ".join(seen)

@register.filter(name="add_class")
def add_class(field, css_classes):
    """
    Uso en template: {{ form.campo|add_class:"form-control is-invalid" }}
    No cambia el aspecto por sí mismo; solo agrega clases al widget.
    """
    attrs = field.field.widget.attrs.copy()
    attrs["class"] = _merge_classes(attrs.get("class", ""), css_classes)
    return field.as_widget(attrs=attrs)

@register.filter(name="add_attr")
def add_attr(field, arg):
    """
    Uso: {{ form.campo|add_attr:"placeholder:Tu nombre" }}
    """
    try:
        name, val = [x.strip() for x in arg.split(":", 1)]
    except ValueError:
        return field
    attrs = field.field.widget.attrs.copy()
    attrs[name] = val
    return field.as_widget(attrs=attrs)
