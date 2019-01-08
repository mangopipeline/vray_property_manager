'''
Created on Jan 7, 2019

@author: carlos
'''
import unittest
from tps.qt_helpers.tree_model_helper import Node


class TestTreeNode(unittest.TestCase):
    def test_treenode_create(self):
        node_a = Node('Node A')
        node_b = Node('Node B')
        node_b.parent = node_a

        self.assertTrue(node_b.parent == node_a)
        self.assertListEqual(node_a.children, [node_b])

        node_c = Node('Node C')
        node_c.parent = node_a

        self.assertListEqual(node_a.children, [node_b, node_c])


if __name__ == '__main__':
    unittest.main()
