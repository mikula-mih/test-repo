
class ItemType:
    def __init__(self, name: str) -> None:
        self.name = name
        self.on_hand = 0

class OutOfStock(Exception):
    pass


class InvalidItemType(Exception):
    pass


class Inventory:
    def __init__(self, stock: list[ItemType]) -> None:
        pass

    def lock(self, item_type: ItemType) -> None:
        """Context Entry.
        Lock the item type so nobody else can manipulate the
        inventory while we're working."""
        pass

    def unlock(self, item_type: ItemType) -> None:
        """Context Exit.
        Unlock the item type."""
        pass

    def purchase(self, item_type: ItemType) -> int:
        """If the item is not locked, raise a
        ValueError because something went wrong.
        If the item_type does not exist,
            raise InvalidItemType.
        If the item is currently out of stock,
            raise OutOfStock.
        If the item is available,
            subtract one item; return the number of items left.
        """
        # Mocked results.
        if item_type.name == "Widget":
            raise OutOfStock(item_type)
        elif item_type.name == "Gadget":
            return 42
        else:
            raise InvalidItemType(item_type)


msg = (
    f"there is {num_left} {item_to_buy.name} left"
    if num_left == 1
    else f"there are {num_left} {item_to_buy.name}s left")
print(msg)
