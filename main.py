class Vertex:
    def __init__(self, key, value, parent):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent

    def info(self):
        if self.parent is None:
            return f"[{self.key} {self.value}]"
        else:
            return f"[{self.key} {self.value} {self.parent.key}]"

    def is_leaf(self):
        return self.left is None and self.right is None

    def has_parent(self):
        return self.parent is not None


class DBT:
    def __init__(self):
        self.root = None
        self.height = 0

    def add(self, key, value):
        if self.root is None:
            self.root = Vertex(key, value, None)
            self.height += 1
        else:
            current_vertex = self.root
            height = 1
            while True:
                if key < current_vertex.key:
                    if current_vertex.left is None:
                        current_vertex.left = Vertex(key, value, current_vertex)
                        height += 1
                        if height > self.height:
                            self.height = height
                        break
                    else:
                        current_vertex = current_vertex.left
                        height += 1
                elif key > current_vertex.key:
                    if current_vertex.right is None:
                        current_vertex.right = Vertex(key, value, current_vertex)
                        height += 1
                        if height > self.height:
                            self.height = height
                        break
                    else:
                        current_vertex = current_vertex.right
                        height += 1

    def set(self, key, value):
        current_vertex = self.root
        while True:
            if current_vertex is None:
                print("error")
                break
            if key == current_vertex.key:
                current_vertex.value = value
                break
            elif key < current_vertex.key:
                current_vertex = current_vertex.left
            elif key > current_vertex.key:
                current_vertex = current_vertex.right

    def print_vertex_by_code(self, vertex_code):
        current_vertex = self.root
        while len(vertex_code) > 0:
            current_step = vertex_code[0]
            if current_step == '0':
                current_vertex = current_vertex.left
            elif current_step == '1':
                current_vertex = current_vertex.right
            if current_vertex is None:
                return '_'
            vertex_code = vertex_code[1:]
        return f'[{current_vertex.key} {current_vertex.value} {current_vertex.parent.key}]'

    def print(self):
        level = 2
        print(f'[{self.root.key} {self.root.value}]')
        while level <= self.height:
            vertex_amount_on_level = (2 ** (level - 1))
            for level_count in range(vertex_amount_on_level):
                current_code = f'{level_count:b}'.zfill(level - 1)
                print(self.print_vertex_by_code(current_code), end=' ')
            print()
            level += 1

    def search(self, key):
        current_vertex = self.root
        while True:
            if current_vertex is None:
                print('0')
                break
            if key == current_vertex.key:
                print(f'1 {current_vertex.value}')
                break
            elif key < current_vertex.key:
                current_vertex = current_vertex.left
            elif key > current_vertex.key:
                current_vertex = current_vertex.right

    def min(self, root):
        current_vertex = root
        if current_vertex is not None:
            while current_vertex.left is not None:
                current_vertex = current_vertex.left
            print(f'{current_vertex.key} {current_vertex.value}')
            return current_vertex
        else:
            print("error")

    def max(self, root):
        current_vertex = root
        if current_vertex is not None:
            while current_vertex.right is not None:
                current_vertex = current_vertex.right
            print(f'{current_vertex.key} {current_vertex.value}')
            return current_vertex
        else:
            print("error")

    def delete(self, key):
        current_vertex = self.root
        while True:
            if current_vertex is None:
                print("error")
                break
            if key == current_vertex.key:
                if current_vertex.is_leaf():  # vertex is a leaf
                    if current_vertex.parent.left == current_vertex:
                        current_vertex.parent.left = None
                    else:
                        current_vertex.parent.right = None
                elif current_vertex.left is None:  # vertex has only right child
                    if current_vertex.parent.left == current_vertex:
                        current_vertex.parent.left = current_vertex.right
                    else:
                        current_vertex.parent.right = current_vertex.right
                    current_vertex.right.parent = current_vertex.parent
                elif current_vertex.right is None:  # vertex has only left child
                    if current_vertex.parent.left == current_vertex:
                        current_vertex.parent.left = current_vertex.left
                    else:
                        current_vertex.parent.right = current_vertex.left
                        current_vertex.left.parent = current_vertex.parent
                    current_vertex.left.parent = current_vertex.parent
                else:  # vertex has two children
                    swap_vertex = self.max(current_vertex.left)  # max from left subtree
                    if swap_vertex.is_leaf():
                        if swap_vertex == current_vertex.left:
                            swap_vertex.right = current_vertex.right  # link between cur_ right child and swap_
                            swap_vertex.right.parent = swap_vertex
                        else:
                            swap_vertex.parent.right = None  # deleting link between swap_ parent and swap_

                            swap_vertex.right = current_vertex.right  # making links between cur_ children and swap_
                            swap_vertex.right.parent = swap_vertex
                            swap_vertex.right = current_vertex.right
                            swap_vertex.right.parent = swap_vertex

                            swap_vertex.left = current_vertex.left  # making links between cur_ children and swap_
                            swap_vertex.left.parent = swap_vertex
                            swap_vertex.left = current_vertex.left
                            swap_vertex.left.parent = swap_vertex

                        if current_vertex != self.root:
                            if current_vertex.parent.left == current_vertex:  # link between cur_ parent and swap_
                                current_vertex.parent.left = swap_vertex
                            elif current_vertex.parent.right == current_vertex:
                                current_vertex.parent.right = swap_vertex
                            swap_vertex.parent = current_vertex.parent
                        else:
                            swap_vertex.parent = None
                            self.root = swap_vertex



                break
            elif key < current_vertex.key:
                current_vertex = current_vertex.left
            else:
                current_vertex = current_vertex.right


test_tree = DBT()
test_tree.add(8, 10)
test_tree.add(4, 14)
test_tree.add(7, 15)
test_tree.add(9, 11)
test_tree.add(3, 13)
test_tree.add(5, 16)
test_tree.add(88, 1)
test_tree.add(11, 2)
test_tree.add(100, 18)

print("Tree without changes:")
test_tree.print()

print("Deleting with key 100(leaf):")  # WORKING
test_tree.delete(100)
test_tree.print()

print("Deleting with key 7(one child):")  # WORKING
test_tree.delete(7)
test_tree.print()

print("Deleting with key 4(two children, 'max' is a left child of 4)")  # WORKING???
test_tree.delete(4)
test_tree.print()

print("Adding two new vertex")
test_tree.add(1, 14)
test_tree.add(2, 118)
test_tree.print()

print("Deleting with key 3(two children, 'max' is not a left child of 4)")  # WORKING???
test_tree.delete(3)
test_tree.print()
