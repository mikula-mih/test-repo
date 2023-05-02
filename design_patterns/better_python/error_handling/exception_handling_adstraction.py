
""" Handle exceptions at the right level of abstraction """

# the exception the funciton is handling or raising has to be consistent with
# the logic encapsulated on it;

class DataTransport:
    """An example of an object handling exceptions of different levels."""

    retry_threshold: int = 5
    retry_n_times: int = 3

    def __init__(self, connector):
        self._connector = connector
        self.connection = None

    def delicer_event(self, event):
        try:
            self.connect()
            data = event.decode()
            self.send(data)
        except ConnectionError as e:
            logger.info("connection error detected: %s", e)
            raise
        except ValueError as e:
            logger.error("%r contains incorrect data: %s", event, e)
            raise

    def connect(self):
        for _ in range(self.retry_n_times):
            try:
                self.connection = self._connector.connect()
            except ConnectionError as e:
                logger.info(
                    "%s: attempting new connection in %is",
                    e,
                    self.retry_threshold,
                )
                time.sleep(self.retry_threshold)
            else:
                return self.connection
        raise ConnectionError(
            f"Couldn't connect after {self.retry_n_times} times"
        )

    def send(self, data):
        return self.connection.send(data)


# for the exception on the `ValueError` event, we could separate it with
# a new object and do composition, but for this limited case it would be overkill
#
# The `ConnectionError` should be handled inside the connect method. This
# will allow a clear separation of behavior.
# Conversely, `ValueError` belongs to the decode method of the event.
# With this new implementation, this method does not need to catch
# any exception—the exceptions it was worrying about before are either handled
# by internal methods or deliberately left to be raised.

    def connect_with_retry(connector, retry_n_times, retry_threshold=5):
        """Tries to establish the connection of <connector> retrying
        <retry_n_times>.
        If it can connect, returns the connection object.
        If it's not possible after the retries, raises ConnectionError

        :param connector: An object with a `.connect()` method.
        :param retry_n_times int: The number of times to try to call
                                    ``connector.connect()``.
        :param retry_threshold int: The time lapse between retry calls.
        """
        for _ in range(retry_n_times):
            try:
                return connector.connect()
            except ConnectionError as e:
                logger.info(
                    "%s: attempting new connection in %is", e, retry_threshold
                )

    def deliver_event(self, event):
        self.connection = connect_with_retry(
            self._connector, self.retry_n_times, self.retry_threshold
        )
        self.send(event)

    def send(self, event):
        try:
            return self.connection.send(event.decode())
        except ValueError as e:
            logger.error("%r contains incorrect data: %s", event, e)
            raise


""" Do not expose tracebacks """
# This is a security consideration
""" Avoid empty except blocks """
# the most diabolical Python anti-pattern (REAL 01)
# an empty `except` block that silently passes without doing anything
""" Include the original exception """
# In Python 3 (PEP-3134), we can now use the raise <e> from <original_exception>
# syntax

class InternalDataError(Exception):
    """An exception with the data of our domain problem."""

def process(data_dictionary, record_id):
    try:
        return data_dictionary[record_id]
    except KeyError as e:
        # Always use the `raise <e> from <o>` syntax
        # when changing the type of the exception
        raise InternalDataError("Record not present") from e
