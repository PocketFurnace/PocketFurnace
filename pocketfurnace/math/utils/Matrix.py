from copy import deepcopy


class Matrix:
    matrix = {}
    rows = 0
    columns = 0

    def offset_exists(self, offset):
        if int(offset) in self.matrix:
            return True
        else:
            return False

    def offset_get(self, offset):
        return self.matrix[int(offset)]

    def offset_set(self, offset, value):
        self.matrix[int(offset)] = value

    def offset_unset(self, offset):
        self.matrix[int(offset)].pop()

    def __init__(self, rows, columns, set={}):
        self.rows = max(1, int(rows))
        self.columns = max(1, int(columns))
        self.set(set)

    def set(self, m):
        for r in range(0, self.rows):
            self.matrix[r] = {}
            for c in range(0, self.columns):
                self.matrix[r][c] = m[r][c] or 0

    def get_rows(self) -> int:
        return self.rows

    def get_columns(self):
        return self.columns

    def set_element(self, row, column, value) -> bool:
        if row > self.rows or row < 0 or column > self.columns or column < 0:
            return False
        self.matrix[int(row)][int(column)] = value
        return True

    def get_element(self, row, column):
        if row > self.rows or row < 0 or column > self.columns or column < 0:
            return False
        return self.matrix[int(row)][int(column)]

    def is_square(self) -> bool:
        if self.rows == self.columns:
            return True
        else:
            return False

    def add(self, matrix):
        if self.rows != matrix.get_rows() or self.columns != matrix.get_columns():
            return False
        result = Matrix(self.rows, self.columns)
        for r in range(0, self.rows):
            for c in range(0, self.columns):
                result.set_element(r, c, self.matrix[r][c] + matrix.get_element(r, c))
        return result

    def subtract(self, matrix):
        if self.rows != matrix.get_rows() or self.columns != matrix.get_columns():
            return False
        result = deepcopy(self)
        for r in range(0, self.rows):
            for c in range(0, self.columns):
                result.set_element(r, c, self.matrix[r][c] - matrix.get_element(r, c))
        return result

    def multiply_scalar(self, number):
        result = deepcopy(self)
        for r in range(0, self.rows):
            for c in range(0, self.columns):
                result.set_element(r, c, self.matrix[r][c] * number)
        return result

    def divide_scalar(self, number):
        result = deepcopy(self)
        for r in range(0, self.rows):
            for c in range(0, self.columns):
                result.set_element(r, c, self.matrix[r][c] / number)

    def transpose(self):
        result = Matrix(self.rows, self.columns)
        for r in range(0, self.rows):
            for c in range(0, self.columns):
                result.set_element(r, c, self.matrix[r][c])
        return result

    def product(self, matrix):
        if self.columns != matrix.get_rows():
            return False
        c = matrix.get_columns()
        result = Matrix(self.rows, c)
        for i in range(0, self.rows):
            for j in range(0, c):
                sum = 0
                for k in range(0, self.columns):
                    sum += self.matrix[i][k] * matrix.get_element(k, j)
                result.set_element(i, j, sum)
        return result

    def determinant(self):
        if not self.is_square():
            return False

        if self.rows == 1:
            return self.matrix[0][0]
        if self.rows == 2:
            return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]
        if self.rows == 3:
            return self.matrix[0][0] * self.matrix[1][1] * self.matrix[2][2] + self.matrix[0][1] * self.matrix[1][2] * \
                   self.matrix[2][0] + self.matrix[0][2] * self.matrix[1][0] * self.matrix[2][1] - self.matrix[2][0] * \
                   self.matrix[1][1] * self.matrix[0][2] - self.matrix[2][1] * self.matrix[1][2] * self.matrix[0][0] - \
                   self.matrix[2][2] * self.matrix[1][0] * self.matrix[0][1]
        return False

    def to_string(self):
        s = ""
        for r in range(0, self.rows):
            s += ",".join(self.matrix[r]) + ";"
        return "Matrix("+str(self.rows)+"x"+str(self.columns)+":"+s[0:-1]+")"
