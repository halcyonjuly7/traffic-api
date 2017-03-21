# from sqlalchemy import create_engine, Table, MetaData, text
# import csv
# metadata = MetaData()
# engine = create_engine("postgresql+psycopg2://postgres:Jiujitsu123@45.55.198.11/nearest")
#
# table=Table("zip_codes", metadata, autoload_with=engine)
#
# with open("gps_coordinates.csv") as coords:
#     data = list(csv.DictReader(coords))
#     engine.execute("COPY zip_codes FROM '/tmp/gps_coordinates.csv' DELIMITER ',' CSV HEADER")
#     # engine.execute(table.insert(),  data)

#
# opening = "({["
# closing = ")}]"
#
# wrong= "([]{)}"
# right = ""
#
#
# def check_delimiters(string):
#     stack = []
#     for char in string:
#         if char in opening:
#             stack.append(char)
#         elif char in closing:
#             if not stack:
#                 return False
#             if closing.index(char) != opening.index(stack.pop()):
#                 return False
#     return not stack
#
#
# if __name__ == "__main__":
#     print(check_delimiters(wrong))

class Person:
    def __init__(self, name="Cyon", age=12):
        self._name = name
        self._age = age

    def print_name(self):
        return self._name

import functools

babe = functools.partial(Person, name="Babe")
yolo = babe(age=13)

print(yolo.print_name())