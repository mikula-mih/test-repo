import numpy as np

class Player:
    def __init__(self, name, position, fatigue=0):
        self.name = name
        self.position = position
        self.fatigue = fatigue

    def draw(self):
        print(f"drawing {self.name} to screen at {self.position}")

    def move(self, delta):
        self.position += delta
        self.fatigue += 1

    def rest(self):
        self.fatigue = 0


class PlayerMethodChaining:
    def __init__(self, name, position, fatigue=0):
        self.name = name
        self.position = position
        self.fatigue = fatigue

    def draw(self):
        print(f"drawing {self.name} to screen at {self.position}")
        return self

    def move(self, delta):
        self.position += delta
        self.fatigue += 1
        return self

    def rest(self):
        self.fatigue = 0
        return self


def main():
    james = Player("James", np.array([0.0, 0.0]))
    mark = PlayerMethodChaining("Mark", np.array([0.0, 0.0]))
    UP = np.array([0.0, 1.0])
    RIGHT = np.array([1.0, 0.0])

    james.move(UP)
    james.move(RIGHT)
    james.move(UP)
    james.rest()
    james.draw()

    # mark.move(UP).move(RIGHT).move(UP).rest().draw()
    #
    mark.move(UP) \
        .move(RIGHT) \
        .move(UP) \
        .rest() \
        .draw()
    #
    (
        mark.move(UP)
            .move(RIGHT)
            .move(UP)
            .rest()
            .draw()
    )

# EXAMPLE 2
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Vector:
    x: float
    y: float
    z: float

    def normalized(self):
        x, y, z = self.x, self.y, self.z
        norm = np.sqrt(x * x + y * y + z * z)
        return type(self)(x / norm, y / norm, z / norm)

    def reflected(self):
        return type(self)(-self.x, -self.y, -self.z)


def main_Vector():
    p = Vector(1., 2., 3.)
    q = p.reflected().normalized()
    print(p)
    print(q)

# EXAMPLE 3
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship("Address",
                             back_populates="user",
                             cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="assresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


def demo_method_chaining(session):
    stmt = (
        select(Address)
            .join(Address.user)
            .where(User.name == "sandy")
            .where(Address.email_address == "sandy@sqlalchemy.org")
    )

    print(type(stmt))
    print()
    print(stmt)

# DataScience EXAMPLE
import pandas as pd
from pandas import DataFrame

company_sales = {
    'SalesMonth': ['Jan', 'Feb', 'Mar', 'Apr'],
    'Company1': [150.0, 200.0, 300.0, 400.0],
    'Company2': [180.0, 250.0, np.nan, 500.0],
    'Company3': [400.0, 500.0, 600.0, 675.0]
}

def pandas_way():
    df = pd.DataFrame.from_dict(company_sales)
    del df['Company1']
    df = df.dropna(subset=['Company2', 'Company3'])
    df = df.rename(
        {
            'Company2': 'Amazon',
            'Company3': 'Facebook',
        },
        axis=1,
    )
    df['Google'] = [450.0, 550.0, 800.0]
    print()
    print(df)


# pip install pyjanitor
def pyjanitor_way():
    df = (
        pd.DataFrame.from_dict(company_sales)
            .remove_columns(["Company1"])
            .dropna(subset=["Company2", "Company3"])
            .rename_column("Company2", "Amazon")
            .rename_column("Company3", "Facebook")
            .add_column("Google", [450.0, 550.0, 800.0])
    )

    print()
    print(df)


if __name__ == '__main__':
    main()
    main_Vector()
    demo_method_chaining()
    pandas_way()
    pyjanitor_way()
