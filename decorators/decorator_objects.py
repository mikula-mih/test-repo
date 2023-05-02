
""" Decorator objects """

RETRIES_LIMIT = 3

class WithRetry:

    def __init__(self, retires_limit=RETRIES_LIMIT, allowed_exceptions=None):
        self.retires_limit = retires_limit
        self.allowed_exceptions = allowed_exceptions or (ControlledException,)

    def __call__(self, operation):

        @wraps(operation)
        def wrapped(*args, **kwargs):
            last_raised = None

            for _ in range(self.retries_limit):
                try:
                    return operation(*args, **kwargs)
                except self.allowed_exceptions as e:
                    logger.info("retrying %s due to %s", operation, e)
                    last_raised = e
            raise last_raised

        return wrapped

@WithRetry(retries_limit=5)
def run_with_custom_retries_limit(task):
    return task.run()
