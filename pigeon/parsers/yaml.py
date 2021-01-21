import yaml
import sys


def parse_yaml(pigeon, request_file) -> list:
    '''
    Parses the request YAML, and returns it as a dictionary
    '''
    logger = pigeon.logger
    try:
        request_yaml = yaml.safe_load(request_file)
    except yaml.YAMLError as exc:
        logger.critical("There is an error in your yaml. \n {}".format(exc))
        sys.exit(1)

    logger.debug(
        "Request YAML as interpreted by pyyaml \n {}".format(request_yaml))
    return request_yaml
