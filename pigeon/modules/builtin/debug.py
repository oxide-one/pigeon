from pigeon.module import Module
from jinja2 import Template
import pprint

class debug(Module):
    options = {
    "msg": "hello world"
    }

    def _init_(self):
        self.template_raw = self.options["msg"]
        self.template = Template(self.template_raw)
        self.printer = pprint.PrettyPrinter()

    def execute(self, logger, row, variables, opt=None):
        rendered_message = self.template.render(variables)
        self.printer.pprint(rendered_message)
        return {
         "msg": rendered_message,
         "template": self.template_raw
        }
