import sys
from pigeon.validators import validate_request
from pigeon.util import make_ordinal


def validate_requests(pigeon):
    '''
    Iterate over each request and perform validations for the requests
    '''
    # Create the logger from pigeon
    logger = pigeon.logger

    # Grab the YAML
    requests = pigeon.requests_yaml
    # Required 'root' options, such as name etc..
    if type(requests) is not list:
        logger.critical("The root of the YAML must be a list.")
        sys.exit(1)

    # Enumerate the list and validate the yaml for each request
    for idx, request in enumerate(requests):
        # Create a variable specifying which 'ist' the request is, i.e. 1st 2nd
        ist = make_ordinal(idx + 1)
        logger.debug("Validating YAML for the the {} request".format(ist))
        validate_request(logger, request)
        logger.debug("Basic validation has passed for the {} request".format(ist))

    # Log that validation passed
    logger.info("Request Validation passed")
