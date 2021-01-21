import sys


class Module:
    '''
    The parent module to all other tasks.
    This will handle updating the default options dictionary.
    The __init__ class cannot be used by the subclasses, otherwise this stuff will not work.
    '''
    # Strict options boolean. This controls whether to throw an error if an unrecognised option is given to the module.
    strict_options = False

    def __init__(self, logger, *args, **kwargs):
        '''
        the init
        '''
        self._update_options(logger, *args, **kwargs)
        self._init_()
        logger.debug("hello")

    def _update_options(self, logger, *args, **kwargs):
        if self.strict_options:
            for key, value in kwargs.items():
                if key not in self.options:
                    logger.critical("unrecognised option {} given to module {}".format(key, self.__class__.__name__))
                    sys.exit(1)
        try:
            self.options.update(dict((key.lower(), value) for key, value in kwargs.items()))
        except AttributeError:
            self.options = kwargs
            logger.debug("The {} module does not take options".format(self.__class__.__name__))

    def pre_exec(self, *args):
        '''
        The pre_exec function, called from within pigeon
        '''
