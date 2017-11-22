import re

class Listing():
    NON_NUMERIC = re.compile("[^0-9]")
    """Strip non numeric characters from price"""

    def __init__(self):
        self.post_id = ''
        self.make = ''
        self.model = ''
        self.series = ''
        self.price = ''

    @classmethod
    def create(cls, post_id, make, model, series, price):
        """Factory for class. Assumes parameters are list of size 0 or 1."""
        ret = cls()

        if post_id:
            ret.post_id = post_id[0]
        if make:
            ret.make = make[0]
        if model:
            ret.model = model[0]
        if series:
            ret.series = series[0]
        if price:
            ret.price = re.sub(Listing.NON_NUMERIC, '', price[0])

        return ret

    def __str__(self):
        return "{0},{1},{2},{3},{4}".format(
            self.post_id, self.make, self.model, self.series, self.price)
