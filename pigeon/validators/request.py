import sys


def validate_request(logger, request: dict):
    required_root_options = ["name", "rows"]
    # Iterate over the required root options
    logger.debug("Validating root options within the request")
    for root in required_root_options:

        # Check if the required options are part of the play.
        if root not in request:
            logger.critical("The request is missing '{}'".format(root))
            sys.exit(1)
        else:
            logger.debug("The request has '{}'".format(root))

    logger.debug("Checks for required variables have passed")

    # Check that the rows is of type int
    try:
        int(request["rows"])
    except ValueError:
        logger.critical("Rows is not an integer")
        sys.exit(1)

    # Check that tasks and generators are lists
    if "tasks" in request:
        logger.debug("Found {} tasks in the request\n{}".format(len(request['tasks']), request['tasks']))
        if type(request["tasks"]) is not list:
            logger.error("'tasks:' should be a list")
            sys.exit(1)
