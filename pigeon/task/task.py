import sys
from jinja2 import Template
from pigeon.util import make_ordinal, make_template
from pigeon.importers import import_pigeon_module
import traceback


class Task:
    '''
    A task within Pigeon. This is a 'wrapper' around a module that handles
    events such as 'when' or 'register'. When initalized, the task class will
    Set the name, determine the module to run and finally run it when run() is
    called.
    '''
    default_task_args = [
        "index",
        "numeric_index",
        "name",
        "when",
        "register"
    ]
    __register__ = False
    __when__ = False

    def __init__(self, logger, task_index, task_args):
        '''
        Initalizes the module and sets the necessary variables, along with determining
        the moudule to be used.
        The task class has the following variables set.
            - task_index
            - task_numeric_index
            - task_name
            - task_vars
            - rows
            - module_name
            - module_args
        '''
        # Set the numeric, and ordinal task index.
        # We can be fairly confident that both of these variables will always exist,
        # so no need to perform a check.
        self.index = task_index
        self.ordinal = make_ordinal(task_index)

        self.logger = logger
        # Set the task name.
        # This is not a required field, so default to the module name if not specified.
        if "name" not in task_args:
            logger.warn("The {} task is not named, defaulting to none.".format(self.ordinal))
            self.task_name = "unnamed"
        else:
            self.task_name = task_args["name"]

        # Set the 'when' option to be used by when() later on in the task exectuion.
        # This is also not a required field, so we need to explicitly check for its existence.
        if "when" in task_args:
            self.__when__ = True
            if type(task_args["when"]) is list:
                self.when_template = [make_template(when_arg) for when_arg in task_args["when"]]
            elif type(task_args["when"]) is str:
                self.when_template = make_template(task_args["when"])
            else:
                logger.critical("Error in the when clause")

        # Set the 'register' option to be used by register() later on in the task execution.
        # This is not a required field, so explicitly check for its existence
        if "register" in task_args:
            self.__register__ = True
            self.register_variable = task_args["register"]

        # Pop the task_args to determine the module name.
        # This is done so that any remaining keys can be figured out.
        for opt in self.default_task_args:
            task_args.pop(opt, None)

        # Exit out if there is more than 1 key left.
        if len(task_args.keys()) != 1:
            logger.error(
                "There's an unrecognized argument, or a formatting error in your {} task".format(self.task_index))
            sys.exit(1)

        # Determine the module name from the remaining keys
        self.module_name = list(task_args.keys())[0]
        logger.debug("Using the module {} for the {} task".format(self.module_name, self.index))

        # Set the module args to be passed through when the module is initalized
        # This can fail if no options have been passed through
        try:
            self.module_args = {**task_args[self.module_name]}
        except TypeError:
            self.module_args = {}

        logger.debug("Module args: {}".format(self.module_args))
        # Import the module for pigeon
        self.module = import_pigeon_module(logger, self.module_name, **self.module_args)

    def when(self, data_space):
        '''
        This handles conditionals for the task. the 'when' option is evaluated
        before the task is run, to determine whether to run the task. The When
        option is a simple true/false check, evaluated with Jinja2.
        '''
        if type(self.when_template) is Template:
            when_result = self.when_template.render(**data_space)
            return eval(when_result)

        elif type(self.when_template) is list:
            result = True
            for when_template in self.when_template:
                when_result = when_template.render(**data_space)
                if eval(when_result):
                    pass
                else:
                    result = False
            return result

    def execute_row(self, row, data_space):
        execute_task = True
        if self.__when__:
            execute_task = self.when(data_space.pull())

        if not execute_task:
            return None

        module_return = self.module.execute(
            self.logger,
            row,
            data_space.pull(),
            data_space
            )

        if self.__register__:
            data_space.update_row(
                self.register_variable,
                module_return
                )

        return module_return

    def execute(self, data_space):
        '''
        Run the task each time for the number of rows there are in the request.
        ## Required variables
        request_vars        - The individual variables for the request
        requests_vars       - The request variables for ALL requests
        '''
        rows = data_space.get_rows()
        logger = self.logger
        task_run = []
        try:
            for row in range(rows):
                data_space.current_row = row
                task_run.append(self.execute_row(row, data_space))
        except Exception:
            logger.critical("Error in the execution of the module!")
            err_traceback = traceback.format_exc()
            logger.debug(err_traceback)
            sys.exit(1)
        logger.debug("Task returned: \n{}".format(task_run))
