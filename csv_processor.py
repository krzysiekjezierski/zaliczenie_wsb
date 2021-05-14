from operator import itemgetter
from pprint import pprint


class CSVProcessor:
    def __init__(self, csv: str=None, types=None, sep=','):
        if csv is None:
            return

        split = [line.split(sep) for line in csv.splitlines()]
        self.header = split[0]
        self.csv = ([[type_(value) for (type_, value) in zip(types, values)] for values in split[1:]]
                    if types is not None else split[1:])
        self.types = types
        self.sep = sep

    def sort(self, key=None):
        if key is None:
            key = 0

        self.csv = sorted(self.csv, key=itemgetter(key))

    def top(self, count):
        return self.csv[:count]

    def tail(self, count):
        return self.csv[-count:]

    def get_column(self, column):
        return [row[column] for row in self.csv]

    def get_columns(self, columns):
        return [[row[column] for column in columns]
                for row in self.csv]

    def drop_column(self, column):
        del self.header[column]
        for row in self.csv:
            del row[column]

    def drop_columns(self, columns):
        c = set(range(len(self.header))) - set(columns)
        self.header = [self.header[i] for i in range(len(self.header)) if i in c]
        self.csv = self.get_columns(c)

    def get_rows_by_column_value(self, column, value):
        return [row for row in self.csv if row[column] == value]

    def __str__(self):
        s = self.sep.join(str(cell) for cell in self.header) + "\n"
        for row in self.csv:
            s += self.sep.join([str(cell) for cell in row]) + "\n"
        return s

    def __getitem__(self, n):
        return self.csv[n]

    def __eq__(self, other: "CSVProcessor"):
        return str(self) == str(other)

    @classmethod
    def from_file(cls, path):
        with open(path, "r", encoding="utf-8") as f:
            csv = "".join(f.readlines())
        return CSVProcessor(csv=csv)


if __name__ == "__main":
    csv_processor = CSVProcessor.from_file("ford_escort.csv")
    csv_processor.sort(key=2)
    csv_processor.drop_column(1)
    pprint(csv_processor.bottom(10))
    print(str(csv_processor))
