from matrix import matrix_mult as mmult
from matrix import *

class Stack:
    def __init__(self):
        self.stack = []
        I = new_matrix()
        ident(I)
        self.stack.append(I)

    def push():
        clone = [row[:] for row in self.peek()[:]]
        self.stack.append(clone)

    def pop():
        if len(stack) > 1:
            self.stack.pop()

    def peek():
        return self.stack[-1]

    def mult(matrix):
        mmult(matrix, self.peek())

    def transform_points(points):
        mmult(self.peek(), points)
