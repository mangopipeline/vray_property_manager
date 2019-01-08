import os


class Node(object):
    """
    Convenience class for creating Qt Tree Model Views

    :param str name: name of the node
    :param Node parent: Node parent
    """

    def __init__(self, name, parent=None):
        self.expanded = False
        self.selected = True
        self._name = name
        self._children = []
        self._parent = None
        self._icon = None
        if parent:
            self.parent = parent

    def __repr__(self):
        return "<{0.__class__.__name__} '{0.name}'>".format(self)

    def find_child_by_name(self, name):
        """Get immediate child Node by its full name. This allows for searches
        to find nodes with duplicate base names but different paths.

        :param str name: Fully-qualified child node name
        """
        # ToDo: Handle children with duplicate names
        for child in self.children:
            if child.full_name() == name:
                return child

        return None

    @property
    def name(self):
        """
        The name of the node

        :getter: Get the Node's name
        :setter: Set the Node's name
        :type: string
        """
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, basestring):
            raise TypeError("Node's name must be a string")
        self._name = value

    @property
    def children(self):
        """
        A collection of child Nodes

        :getter: Return the Node's children
        :setter: Replace current children with incoming list
        :type: list
        """
        return self._children[:]

    @children.setter
    def children(self, children):
        if isinstance(children, Node):
            children = [children]
        elif not isinstance(children, (list, tuple)):
            raise TypeError("Expected list or tuple of Nodes, found unexpected '{}'".format(type(children).__name__))
        elif not all(isinstance(c, Node) for c in children):
            bad_types = set(type(c).__name__ for c in children if not isinstance(c, Node))
            raise TypeError("All children must be Nodes, found unexpected type(s) '{}'".format(", ".join(bad_types)))

        for child in self._children[:]:
            child.parent = None

        for child in children:
            child.parent = self

        # Get a copy of the child list, and convert to a list in case its a
        # tuple
        self._children = [child for child in children]

    @children.deleter
    def children(self):
        raise AttributeError("Property '.children' may not be deleted. Please change via target's .parent property")

    @property
    def parent(self):
        """
        Change the current parent relationship of the node

        :getter: Return the current parent node
        :setter: Re-parent the node to a new parent
        :type: Node
        """
        return self._parent

    @parent.setter
    def parent(self, value):
        if value == self:
            raise ValueError('Cannot parent an object to itself')
        if value and value.is_descendant_of(self):
            raise ValueError('Cannot create circular dependency')
        old_parent = self._parent
        if old_parent:
            old_parent.__remove_child(self)

        if value:
            value.__add_child(self)

        self._parent = value
        self.post_parent(value)

    @parent.deleter
    def parent(self):
        self.parent = None

    def full_name(self):
        """Return Node's fully-qualified name"""
        names = [n.name for n in self.list_parents()]
        names.append(self.name)
        return os.path.join(*names)

    def icon(self):
        return self._icon

    def __add_child(self, value):
        if value in self._children:
            return
        self._children.append(value)

    def __remove_child(self, value):
        del self._children[self._children.index(value)]

    def post_parent(self, value):
        """
        Convenience method to control what happens after the node is parented
        """
        # this is here mostly to help integrate with apps that need to run other
        # parenting ops outside of the view
        pass

    def row(self):
        """
        Row index based on parent relationship
        """
        if self.parent:
            return self.parent.children.index(self)
        return None

    def list_all_relatives(self, out=None):
        """
        Recursively list all downstream relationships (children/grandchildren)
        """
        out = out or []
        for child in self._children:
            out.append(child)
            child.list_all_relatives(out=out)
        return out

    def list_parents(self):
        """
        List all upstream relationships (parent/grand parents)
        """
        out = []
        parent = self.parent
        while parent:
            out.append(parent)
            parent = parent.parent
        out.reverse()
        return out

    def is_descendant_of(self, node):
        """Return True if current node is a descendant of another node

        :param Node node: Node to search for
        :return: True if current node is a downstream relative of other
        :rtype: bool
        """
        return self._check_if_upstream(self, node)

    def is_ancestor_of(self, node):
        """Return True if current node is an ancestor of another node

        :param Node node: Node to search from
        :return: True if current node is an upstream relative of other
        :rtype: bool
        """
        return self._check_if_upstream(node, self)

    @staticmethod
    def _check_if_upstream(start, end):
        """Return True if end node is an upstream ancestor of start

        :param Node start: Node to begin search from
        :param Node end: Node to search for upstream
        :return: True if end is upstream of start
        :rtype: bool
        """
        curr_node = start
        while curr_node.parent:
            if curr_node.parent == end:
                return True
            curr_node = curr_node.parent
        return False
