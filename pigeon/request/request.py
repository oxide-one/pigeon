from pigeon.util import make_ordinal
from pigeon.task import Task


class Request():
    '''
    A Request. A request has rows, and tasks. The rows are first determined
    before the tasks are initalized.
    '''

    def __init__(self, pigeon, request_index, request):
        # Set the name of the request
        self.name = request["name"]

        # Create the logger
        logger = pigeon.logger

        # Log the entire request
        logger.info("Creating a new request: '{}'".format(self.name))

        # Set the number of rows
        self.rows = request["rows"]

        # Set the tasks
        self.tasks = []

        # Set the request index
        self.index = request_index

        # Set the logger
        self.logger = logger

        # Iterate over the tasks in the request and initalize each task
        tasks = request["tasks"]
        self.tasks = []
        for task_index, task in enumerate(tasks):
            new_task = Task(logger, task_index, task)
            self.tasks.append(new_task)

    def execute(self, pigeon):
        '''
        Iterates over each task in the request and runs it.
        ## Required variables
        request_vars    - The individual variables for the request
        requests_vars   - The request variables for ALL requests

        Within the request space, only the 'request_vars' are allowed to be edited.
        '''
        logger = pigeon.logger

        # Iterate over each task in the list of tasks
        for task in self.tasks:
            logger.info("Executing task '{}'".format(task.task_name))
            task.execute(pigeon.data_space)
