#!python
from queue import LinkedQueue
from collections import deque

class BinaryTreeNode(object):

    def __init__(self, data):
        """Initialize this binary tree node with the given data."""
        self.data = data
        self.left = None
        self.right = None

    def __repr__(self):
        """Return a string representation of this binary tree node."""
        return 'BinaryTreeNode({!r})'.format(self.data)

    def is_leaf(self):
        """Return True if this node is a leaf (has no children)."""
        # Check if both left child and right child have no value
        return self.left is None and self.right is None

    def is_branch(self):
        """Return True if this node is a branch (has at least one child)."""
        # Check if either left child or right child has a value
        return self.left is not None or self.right is not None

    def height(self):
        """Return the height of this node (the number of edges on the longest
        downward path from this node to a descendant leaf node).
        Best and worst case running time: ??? under what conditions?"""

        # Base case
        if self.is_leaf():
            return 0

        # Check if left child has a value and if so calculate its height
        left_height = 0 if self.left is None else self.left.height()

        # Check if right child has a value and if so calculate its height
        right_height = 0 if self.right is None else self.right.height()

        # Return one more than the greater of the left height and right height
        return max(left_height, right_height) + 1


class BinarySearchTree(object):

    def __init__(self, items=None):
        """Initialize this binary search tree and insert the given items."""
        self.root = None
        self.size = 0
        if items is not None:
            for item in items:
                self.insert(item)

    def __repr__(self):
        """Return a string representation of this binary search tree."""
        return 'BinarySearchTree({} nodes)'.format(self.size)

    def is_empty(self):
        """Return True if this binary search tree is empty (has no nodes)."""
        return self.root is None

    def height(self):
        """Return the height of this tree (the number of edges on the longest
        downward path from this tree's root node to a descendant leaf node).
        Best case running time: O(1)
        Worst case running time: O(log(n))"""
        # Check if root node has a value and if so calculate its height
        return self.root.height()

    def contains(self, item):
        """Return True if this binary search tree contains the given item.
        Best case running time: O(1)
        Worst case running time: O(log(n))"""
        # Find a node with the given item, if any
        # node = self._find_node(item)
        node = self._find_node_recursive(item, self.root)
        # Return True if a node was found, or False
        return node is not None

    def search(self, item):
        """Return an item in this binary search tree matching the given item,
        or None if the given item is not found.
        Best case running time: O(1)
        Worst case running time: O(log(n))"""
        # Find a node with the given item, if any
        # node = self._find_node(item)
        node = self._find_node_recursive(item, self.root)
        # Return the node's data if found, or None
        return node.data if node is not None else None

    def insert(self, item):
        """Insert the given item in order into this binary search tree.
        Best case running time: O(1) when tree is empty or unbalanced
        Worst case running time: O(log(n)) average case"""

        # Create child node
        new_child = BinaryTreeNode(item)

        # Handle the case where the tree is empty
        if self.is_empty():
            self.root = new_child
            self.size += 1
            return

        # Find the parent node of where the given item should be inserted
        parent = self._find_parent_node_recursive(item, self.root)

        # Check if the given item should be inserted left or right of parent node
        if item < parent.data:
            parent.left = new_child
        elif item > parent.data:
            parent.right = new_child

        # Increase the tree size
        self.size += 1

    def _find_node(self, item):
        """Return the node containing the given item in this binary search tree,
        or None if the given item is not found.
        Best case running time: O(1) when item is root node
        Worst case running time: O(log(n)) average case"""
        # Start with the root node
        node = self.root
        # Loop until we descend past the closest leaf node
        while node is not None:
            # Check if the given item matches the node's data
            if item == node.data:
                # Return the found node
                return node
            # Check if the given item is less than the node's data
            elif item < node.data:
                # Descend to the node's left child
                node = node.left
            # Check if the given item is greater than the node's data
            elif item > node.data:
                # Descend to the node's right child
                node = node.right
        # Not found
        return None

    def _find_node_recursive(self, item, node):
        """Return the node containing the given item in this binary search tree,
        or None if the given item is not found."""
        # Check if current node contains what we are looking for
        if node.data == item:
            return node

        # If current node is a leaf and we haven't found the item, return None
        if node.is_leaf() or node is None:
            return None

        if item < node.data:
            return self._find_node_recursive(item, node.left)
        elif item > node.data:
            return self._find_node_recursive(item, node.right)

    def _find_parent_node(self, item):
        """Return the parent node of the node containing the given item
        (or the parent node of where the given item would be if inserted)
        in this tree, or None if this tree is empty or has only a root node.
        TODO: Best case running time: ??? under what conditions?
        TODO: Worst case running time: ??? under what conditions?"""
        # Start with the root node and keep track of its parent
        node = self.root
        parent = None
        # Loop until we descend past the closest leaf node
        while node is not None:
            # Check if the given item matches the node's data
            if item == node.data:
                # Return the parent of the found node
                return parent
            # Check if the given item is less than the node's data
            elif item < node.data:
                # Update the parent and descend to the node's left child
                parent = node
                node = node.left
            # Check if the given item is greater than the node's data
            elif item > node.data:
                # Update the parent and descend to the node's right child
                parent = node
                node = node.right
        # Not found
        return parent

    def _find_parent_node_recursive(self, item, node, parent=None):
        """Return the parent node of the node containing the given item
        (or the parent node of where the given item would be if inserted)
        in this tree, or None if this tree is empty or has only a root node."""
        
        # If current node is a leaf and we haven't found the item, return None
        if node is None:
            return None

        if node.data == item:
            return parent
        # Check if we should descend to the left
        elif item < node.data and node.left is not None:
            parent = node
            node = node.left
            return self._find_parent_node_recursive(item, node, parent)
        # Check if we should descend to the right
        elif item > node.data and node.right is not None:
            return self._find_parent_node_recursive(item, node.right, node)
        # The item does not exist, but this would be it's parent
        else:
            return node

    # This space intentionally left blank (please do not delete this comment)

    def items_in_order(self):
        """Return an in-order list of all items in this binary search tree."""
        items = []
        if not self.is_empty():
            # Traverse tree in-order from root, appending each node's item
            self._traverse_in_order_recursive(self.root, items.append)
            # self._traverse_in_order_iterative(self.root, items.append)
        # Return in-order list of all items in tree
        return items

    def _traverse_in_order_recursive(self, node, visit):
        """Traverse this binary tree with recursive in-order traversal (DFS).
        Start at the given node and visit each node with the given function.
        Running time: O(n), visiting every node in tree
        Memory usage: O(height), this function will have at most height functions
        working to traverse the tree."""
        # Traverse left subtree, if it exists
        if node.left is not None:
            self._traverse_in_order_recursive(node.left, visit)
        # Visit this node's data with given function
        visit(node.data)
        # Traverse right subtree, if it exists
        if node.right is not None:
            self._traverse_in_order_recursive(node.right, visit)
        

    def _traverse_in_order_iterative(self, node, visit):
        """Traverse this binary tree with iterative in-order traversal (DFS).
        Start at the given node and visit each node with the given function.
        TODO: Running time: ??? Why and under what conditions?
        TODO: Memory usage: ??? Why and under what conditions?"""
        # Traverse in-order without using recursion (stretch challenge)
        # Create queue and enqueue first node
        stack = deque()
        stack.append(node)
        # Loop through all nodes in order
        while len(stack) > 0:
            node = stack.pop()
            # Enqueue left node if it exists
            if node.left is not None:
                stack.append(node.left)
            # Visit node's data
            visit(node.data)
            # Enqueue right node if it exists
            if node.right is not None:
                stack.append(node.right)


    def items_pre_order(self):
        """Return a pre-order list of all items in this binary search tree."""
        items = []
        if not self.is_empty():
            # Traverse tree pre-order from root, appending each node's item
            self._traverse_pre_order_recursive(self.root, items.append)
        # Return pre-order list of all items in tree
        return items

    def _traverse_pre_order_recursive(self, node, visit):
        """Traverse this binary tree with recursive pre-order traversal (DFS).
        Start at the given node and visit each node with the given function.
        TODO: Running time: ??? Why and under what conditions?
        TODO: Memory usage: ??? Why and under what conditions?"""
        # Visit this node's data with given function
        visit(node.data)
        # Traverse left subtree, if it exists
        if node.left is not None:
            self._traverse_pre_order_recursive(node.left, visit)
        # Traverse right subtree, if it exists
        if node.right is not None:
            self._traverse_pre_order_recursive(node.right, visit)
        

    def _traverse_pre_order_iterative(self, node, visit):
        """Traverse this binary tree with iterative pre-order traversal (DFS).
        Start at the given node and visit each node with the given function.
        TODO: Running time: ??? Why and under what conditions?
        TODO: Memory usage: ??? Why and under what conditions?"""
        # TODO: Traverse pre-order without using recursion (stretch challenge)

    def items_post_order(self):
        """Return a post-order list of all items in this binary search tree."""
        items = []
        if not self.is_empty():
            # Traverse tree post-order from root, appending each node's item
            self._traverse_post_order_recursive(self.root, items.append)
        # Return post-order list of all items in tree
        return items

    def _traverse_post_order_recursive(self, node, visit):
        """Traverse this binary tree with recursive post-order traversal (DFS).
        Start at the given node and visit each node with the given function.
        TODO: Running time: ??? Why and under what conditions?
        TODO: Memory usage: ??? Why and under what conditions?"""
        # Traverse left subtree, if it exists
        if node.left is not None:
            self._traverse_post_order_recursive(node.left, visit)
        # Traverse right subtree, if it exists
        if node.right is not None:
            self._traverse_post_order_recursive(node.right, visit)
        # Visit this node's data with given function
        visit(node.data)


    def _traverse_post_order_iterative(self, node, visit):
        """Traverse this binary tree with iterative post-order traversal (DFS).
        Start at the given node and visit each node with the given function.
        TODO: Running time: ??? Why and under what conditions?
        TODO: Memory usage: ??? Why and under what conditions?"""
        # TODO: Traverse post-order without using recursion (stretch challenge)

    def items_level_order(self):
        """Return a level-order list of all items in this binary search tree."""
        items = []
        if not self.is_empty():
            # Traverse tree level-order from root, appending each node's item
            self._traverse_level_order_iterative(self.root, items.append)
        # Return level-order list of all items in tree
        return items

    def _traverse_level_order_iterative(self, start_node, visit):
        """Traverse this binary tree with iterative level-order traversal (BFS).
        Start at the given node and visit each node with the given function.
        TODO: Running time: ??? Why and under what conditions?
        TODO: Memory usage: ??? Why and under what conditions?"""
        # Create queue to store nodes not yet traversed in level-order
        queue = LinkedQueue()
        # Enqueue given starting node
        queue.enqueue(start_node)
        # Loop until queue is empty
        while queue.length() > 0:
            # Dequeue node at front of queue
            node = queue.dequeue()
            # Visit this node's data with given function
            visit(node.data)
            # Enqueue this node's left child, if it exists
            if node.left is not None:
                queue.enqueue(node.left)
            # Enqueue this node's right child, if it exists
            if node.right is not None:
                queue.enqueue(node.right)
            


def test_binary_search_tree():
    # Create a complete binary search tree of 3, 7, or 15 items in level-order
    # items = [2, 1, 3]
    items = [4, 2, 6, 1, 3, 5, 7]
    # items = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
    print('items: {}'.format(items))

    tree = BinarySearchTree()
    print('tree: {}'.format(tree))
    print('root: {}'.format(tree.root))

    print('\nInserting items:')
    for item in items:
        tree.insert(item)
        print('insert({}), size: {}'.format(item, tree.size))
    print('root: {}'.format(tree.root))

    print('\nSearching for items:')
    for item in items:
        result = tree.search(item)
        print('search({}): {}'.format(item, result))
    item = 123
    result = tree.search(item)
    print('search({}): {}'.format(item, result))

    print('\nTraversing items:')
    print('items in-order:    {}'.format(tree.items_in_order()))
    print('items pre-order:   {}'.format(tree.items_pre_order()))
    print('items post-order:  {}'.format(tree.items_post_order()))
    print('items level-order: {}'.format(tree.items_level_order()))


if __name__ == '__main__':
    test_binary_search_tree()
