
# the `Template` pattern (sometimes called the `Template method`) is useful for
# removing duplicate code; it's intended to support the
# `Don't Repeat Yourself principle`
""" the `Template` pattern """
# It is designed for situations where we have several different tasks to
# accomplish that have some, but not all, steps in common. The common steps are
# implemented in a base class, and the distinct steps are overridden in
# subclasses to provide custom behavior. In some ways, it's like
# the Strategy pattern, except similar sections of the algorithms are
# shared using a base class.
import sqlite3

def test_setup(db_name: str = "sales.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_name)

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS Sales (
            salesperson text,
            amt currency,
            year integer,
            model text,
            new boolean
        )
        """
    )

    conn.execute(
        """
        DELETE FROM Sales
        """
    )

    conn.execute(
        """
        INSERT INTO Sales
        VALUES('Tim', 16000, 2010, 'Honda Fit', 'true')
        """
    )
    conn.execute(
        """
        INSERT INTO Sales
        VALUES('Tim', 9000, 2006, 'Ford Focus', 'false')
        """
    )
    conn.execute(
        """
        INSERT INTO Sales
        VALUES('Hannah', 8000, 2004, 'Dodge Neon', 'false')
        """
    )
    conn.execute(
        """
        INSERT INTO Sales
        VALUES('Hannah', 28000, 2009, 'Ford Mustang', 'true')
        """
    )
    conn.execute(
        """
        INSERT INTO Sales
        VALUES('Hannah', 50000, 2010, 'Lincoln Navigator', 'true')
        """
    )
    conn.execute(
        """
        INSERT INTO Sales
        VALUES('Jason', 20000, 2008, 'Toyota Prius', 'false')
        """
    )
    conn.commit()
    return conn
#
class QueryTemplate:
    def __init__(self, db_name: str = "sales.db") -> None:

    def connect(self) -> None:
        pass

    def construct_query(self) -> None:
        pass

    def do_query(self) -> None:
        pass

    def output_context(self) -> ContextManager[TextIO]:
        pass

    def output_results(self) -> None:
        pass

    def process_format(self) -> None:
        self.connect()
        self.construct_query()
        self.do_query()
        self.format_results()
        self.output_results()
#
class QueryTemplate:
    def __init__(self, db_name: str = "sales.db") -> None:
        self.db_name = db_name
        self.conn: sqlite3.Connection
        self.results: list[tuple[str, ...]]
        self.query: str
        self.header: list[str]

    def connect(self) -> None:
        self.conn = sqlite3.connect(self.db_name)

    def construct_query(self) -> None:
        raise NotImplementedError("construct_query not implemented")

    def do_query(self) -> None:
        results = self.conn.execute(self.query)
        self.results = results.fetchall()

    def output_context(self) -> ContextManager[TextIO]:
        self.target_file = sys.stdout
        return cast(ContextManager[TextIO], contextlib.nullcontext())

    def output_results(self) -> None:
        writer = csv.writer(self.target_file)
        writer.writerow(self.header)
        writer.writerows(self.results)

    def process_format(self) -> None:
        self.connect()
        self.construct_query()
        self.do_query()
        with self.output_context():
            self.output_results()
#
import datetime

class NewVehiclesQuery(QueryTemplate):
    def construct_query(self) -> None:
        self.query = "select * from Sales where new='true'"
        self.header = ["salesperson", "amt", "year", "model", "new"]

class SalesGrossQuery(QueryTemplate):
    def construct_query(self) -> None:
        self.query = (
            "select salesperson, sum(amt) "
            " from Sales group by salesperson"
        )
        self.header = ["salesperson", "total sales"]

    def output_context(self) -> ContextManager[TextIO]:
        today = datetime.date.today()
        filepath = Path(f"gross_sales_{today:%Y%m%d}.csv")
        self.target_file = filepath.open("w")
        return self.target_file
#
