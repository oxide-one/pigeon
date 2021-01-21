from pigeon.logging import create_logger
from pigeon.parsers import parse_yaml
from pigeon.validators import validate_requests
from pigeon.request import Request
from pigeon.data import DataSpace


class Pigeon:
    def __init__(self, args):
        '''Create an Instance of Pigeon and perform the following.
        1. Create a logging instance
        2. Parse the YAML
        3. Validate the YAML
        4. Initalize the requests
        '''
        # Create a logging instance
        self.logger = create_logger(args.verbose)

        # Parse the YAML, and store it
        self.logger.info("Parsing YAML")
        self.requests_yaml = parse_yaml(self, args.request)
        self.requests_file = args.request

        # Validate the YAML and exit upon error
        self.logger.info("Validting requests")
        validate_requests(self)

        # Create the Requests
        self.requests = [
            Request(self, request_index, request) for request_index, request in enumerate(self.requests_yaml)
        ]

        # Create the dataspace
        self.data_space = DataSpace(self)

    def execute(self):
        for idx, request in enumerate(self.requests):
            self.data_space.prepare_request(idx)
            request.execute(self)
