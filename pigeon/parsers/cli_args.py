import argparse
from pigeon import __version__


def parse_cli_args():
    '''
    Parses the command line arguments and returns them as a dict of arguments.
    '''
    program_description = """
    Pigeon. The python based data generator.
    """
    # Create an argument parser instance
    parser = argparse.ArgumentParser(
        description=program_description, prog='Pigeon')

    # Add an argument to handle requests
    parser.add_argument(
        'request',
        metavar="request",
        help="A YAML file that contains the request.",
        type=argparse.FileType('r')
        )

    # Verbosity flag
    parser.add_argument(
        '-v',
        '--verbose',
        help="The logging verbosity",
        action='count',
        default=0
        )

    # Version flag
    parser.add_argument(
        '-V',
        '--version',
        help="Print the version of the program and exit",
        action='version',
        version='%(prog)s {}'.format(__version__),
        )
    # Parse the args and return
    return parser.parse_args()
