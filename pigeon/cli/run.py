import pigeon.parsers as parsers
from pigeon import Pigeon


def run():
    '''
    The entrypoint to pigeon. The run function will load the yaml and parse it into requests.
    '''
    # Parse the command line arguments and store it in the 'args' variable
    args = parsers.parse_cli_args()

    # Create pigeon and initalize the logger
    pigeon = Pigeon(args)

    # Execute the requests
    pigeon.execute()
