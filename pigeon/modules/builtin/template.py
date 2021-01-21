import datetime
from pigeon.module import Module
from jinja2 import Template, Environment, FileSystemLoader
from pathlib import Path


class template(Module):
    strict_options = False
    options = {
        "src": "template.j2",
        "dest": "output",
    }

    def _init_(self):
        '''
        Self.options is automatically populated by pigeon
        '''
        self.env = Environment(
            loader=FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.env.globals['date'] = datetime.date.today()

    def execute(self, logger, row, variables, data_space):
        '''
        Render the source and destination variables before
        loading the template, and executing the action
        '''
        source = Template(self.options['src']).render(variables)
        destination = Template(self.options['dest']).render(variables)
        template = self.env.get_template(source)
        output = template.render(variables)
        path = Path(destination)
        with open(path, 'w+', encoding='UTF-8') as file:
            file.write(output)
        return output
