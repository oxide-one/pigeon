from importlib import import_module
from pigeon.module import Module
import sys
import traceback
from os.path import dirname, abspath, join


### NOTES
"""
I need to try to add functionality that allows for imports from a folder
that the user can specify. I do not want to end up with the same issue
that ansible has, in which the tree has too many modules in the main
repo. As the project is small at the moment, I can afford this lazyness
but this is something I absolutely should keep in mind :)

If you read this, get in contact. okami <AT> oxide.one
"""


def attempt_import(logger, module_name):
    package_dirs = [
     "pigeon.modules.builtin",
     "pigeon.modules"
    ]

    # Iterate over the package dirs to find the module.
    for package_dir in package_dirs:
        try:
            logger.debug("Attempting import from {}".format(package_dir))
            task_module = import_module('.' + module_name, package=package_dir)
            logger.debug("Module {} found in {}".format(module_name, package_dir))
        except ModuleNotFoundError as err:
            logger.debug(err)
            pass

    # If the module is not found by this point, attempting to access the module saved
    # At 'task_module' will raise a UnboundLocalError, which allows for us to
    # Determine if it's been found or not.
    try:
        task_module
    except UnboundLocalError:
        logger.critical('The {} module could not be found!'.format(module_name))
        sys.exit(1)

    return task_module


def import_pigeon_module(logger, module_name, *args, **kwargs):
    '''
    Handles the importing of modules
    '''
    # Attempt to import the module. Returns a module
    task_module = attempt_import(logger, module_name)
    try:
        # Attempt to get the class from the module. This follows a schema of
        # module_name.module_name
        # So set_fact is really set_fact.set_fact
        task_module_class = getattr(task_module, module_name)
        # Initalize the class using the arguments passed to the module
        task_module_instance = task_module_class(logger, *args, **kwargs)
    except AttributeError:
        logger.critical('There is an error in the {} module!'.format(module_name))
        err_traceback = traceback.format_exc()
        logger.debug(err_traceback)
        sys.exit(1)

    except AssertionError:
        logger.critical('The {} module does not exist!'.format(module_name))
        err_traceback = traceback.format_exc()
        logger.debug(err_traceback)
        sys.exit(1)

    else:
        if not issubclass(task_module_class, Module):
            logger.critical("The {} module is not subclassed properly!".format(task_module_class))
            sys.exit(1)
    return task_module_instance
