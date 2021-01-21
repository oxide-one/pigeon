from jinja2 import Template


def make_template(template_str):
    if "{{" in template_str and "}}" in template_str:
        print("YES")
    else:
        template_str = "{{" + template_str + "}}"
        template = Template(template_str)
        return Template(template_str)
