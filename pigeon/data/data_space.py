class DataSpace():
    """This is the space in which data is created, managed and stored
    If the data does not get send to the dataspace, it does not exist
    to the requests.
    :param logger: The logging instance created when pigeon is run
    :type logger: `logging.Logger`
    """

    def __init__(self, pigeon):
        logger = pigeon.logger
        logger.debug("Creating the DataSpace")

        # Set the logger
        logger = pigeon.logger
        requests = pigeon.requests
        # Set the request count
        request_count = len(requests)

        self.__request_count__ = request_count
        self.__requests__ = [
                {
                    "name": request.name,
                    "rows": request.rows,
                    "row_vars": [{"row": row} for row in range(request.rows)]
                } for request in requests
            ]

    def prepare_request(self, request_number):
        '''
        Create the data relevant to the request, and set the current row and index.
        '''
        self.__current_request__ = request_number
        self.current_row = 0

    def get_rows(self):
        '''
        Return the number of rows in the current request
        '''
        return len(
            self.__requests__[self.__current_request__]['row_vars']
            )

    def pull(self):
        '''
        Return all data relevant to the specific row
        '''
        # Expand the current RequestData object, and provide
        return {
            "request_vars": self.__requests__,
            **self.__requests__[self.__current_request__],
            **self.__requests__[self.__current_request__]['row_vars'][self.current_row],
            }

    def update_row(self, variable, data):
        self.__requests__[self.__current_request__]['row_vars'][self.current_row][variable] = data
