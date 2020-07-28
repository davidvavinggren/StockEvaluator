#!/usr/bin/env python3
"""Klass av nyckeltal.

Filen ska kunna användas som hjälp för att importera nyckeltal, kan eventuellt
läggas till en senare fil som en enda klass.
"""

#osäker om klasser eller dictionaries är lämpligste sättet att lagra datan

class Nyckeltal(object):
    """Fäst nyckeltal till ett bolag som representerar klassen"""

    def __init__(self, name, price, earnings, amount_of_stocks, earning_growth):
        """Tar in bolagsdata"""
        self.name = name
        self.pe = (price*amount_of_stocks)/earnings
        self.peg = self.pe/earning_growth
