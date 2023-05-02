
# `decorator` was introduced in PEP-318
# as a mechanism to simplify the way functions and methods are defined when
# they have to be modified after their original definition;

def original(...): # wrapped object
    ...
original = modifier(original)
# the same as
@modifier
def original(...):
    ...

""" Passing arguments to decorators """
""" Decorators with nested functions """
# @retry(arg1, arg2,... )
# <original_function> = retry(arg1, arg2, ....)(<original_function>)
RETRIES_LIMIT = 3

def with_retry(retries_limit=RETRIES_LIMIT, allowed_exceptions=None):
    allowed_exceptions = allowed_exceptions or (ControlledException,)

    def retry(operation):

        @wraps(operation)
        def wrapped(*args, **kwargs):
            last_raised = None
            for _ in range(retries_limit):
                try:
                    return operation(*args, **kwargs)
                except allowed_exceptions as e:
                    logger.info("retrying %s due to %s", operation, e)
                    last_raised = e
            raise last_raised

        return wrapped

    return retry

# examples: of how this decorator can be applied to funtions, showing the
#   different options it accepts:
@with_retry()
def run_operation(task):
    return task.run()

@with__retry(retries_limit=5)
def run_with_custom_retries_limit(task):
    return task.run()

@with_retry(allowed_exceptions=(AttributeError,))
def run_with_custom_exceptions(task):
    return task.run()

@with_retry(
    retries_limit=4, allowed_exceptions=(ZeroDivisionError, AttributeError)
)
def run_with_custom_parameters(task):
    return task.run()
