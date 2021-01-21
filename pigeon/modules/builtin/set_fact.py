from pigeon.module import Module
from jinja2 import Template


class set_fact(Module):
    strict_options = False

    def _init_(self):
        '''
        Self.options is automatically populated by pigeon
        '''
        self.facts = [
            {
                'fact': fact,
                'template': Template(template)
            }
            for fact, template in self.options.items()
        ]

    def execute(self, logger, row, vars, data_space):
        self.data = []
        for index, fact_data in enumerate(self.facts):
            fact = fact_data['fact']
            template = fact_data['template']
            rendered_template = template.render(**vars)
            data_space.update_row(fact, rendered_template)
            self.data.append(rendered_template)
        return self.data
