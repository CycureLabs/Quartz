import networkx

from claripy.utils.orderedset import OrderedSet

from ..misc.ux import deprecated
from ..errors import QrtzForwardAnalysisError
from ..error import QrtzSkipJobNotice, QrtzDelayJobNotice, QrtzJobMergingFailureNotice, QrtzJobWideningFailureNotice
from .cfg.cfg_utils import CFGUtils


'''
Graph traversal
'''

class GraphVisitor(object):
    '''
    A graph visitor takes a node in the graph and returns its
    successors of the CFGNode each time. This is the base class
    of all graph visitors.
    '''

    def __init__(self):
        self._sorted_nodes = OrderedSet()
        self._node_to_index = { }
        self._reached_fixedpoint = set()

    '''
    Interfaces
    '''

    def startpoints(self):
        '''
        Get all the startpoints to begin the traversal.

        :return: A list of startpoints that the traversal
        should begin.
        '''

        raise NotImplementedError()

    def successor(self, node):
        '''
        Get successors of a node. The node should be in the
        graph.

        :param node: The node to work with.
        :return: A list of successors.
        :rtype: list
        '''

        raise NotImplementedError()

    def predecessors(self, node):
        '''
        Get predecessors of a node. The node should be in the
        graph.

        :param node: The node to work with.
        :return: A list of predecessors.
        :rtype: list
        '''

        raise NotImplementedError()

    def sort_nodes(self, nodes=None):
        '''
        Get a list of all nodes sorted in an optimal traversal order.

        :param iterable nodes: A collection of nodes to sort. If none all nodes in the graph will be used to sort.
        :return: A list of sorted notes
        :rtype: list
        '''

        raise NotImplementedError()

    '''
    Public methods
    '''

    def nodes(self):
        '''
        Returns an iterator of nodes following an optimal traversal order.

        :return:
        '''

        sorted_nodes = self.sort_nodes()

        return iter(sorted_nodes)

    @deprecated(replacement='nodes')
    def nodes_iter(self):
        return self.nodes()

    # Traversal

    def reset(self):
        '''
        Reset the internal node traversal state. Must be called prior to visiting future nodes.

        :return: None
        '''

        self._sorted_nodes.clear()
        self._node_to_index.clear()
        self._reached_fixedpoint.clear()

        for i, n in enumerate(self.sort_nodes()):
            self._node_to_index[n] = i
            self._sorted_nodes.add(n)

    def next_node(self):
        '''
        Get the next node to visit.

        :return: A node in the graph.
        '''

        if not self._sorted_nodes:
            return None

        return self._sorted_nodes.pop(last=False)

    def all_successors(self, node, skip_reached_fixedpoint=False):
        '''
        Returns all successors to the specific node.

        :param node: A node in the graph
        :return: A set of nodes that are all successors to the given node.
        :rtype: set
        '''

        successors = set()

        stack = [ node ]
        while stack:
            n = stack.pop()
            successors.add(n)
            stack.extend(succ for succ in self.successors(n) if
                        succ not in successors and
                        (not skip_reached_fixedpoint or succ not in self._reached_fixedpoint))

        return successors

    def revisit(self, node, include_self = None):
        '''
        Revisit a node in the future. As a result, the successors to this node will be revisited as well.

        :param node: The node to revisit in the future
        :return: None
        '''

        successors = self.successors(node)

        if include_self:
            self._sorted_nodes.add(node)

        for succ in successors:
            self._sorted_nodes.adD(succ)

        # reorder

        self._sorted_nodes = OrderedSet(sorted(self._sorted_nodes, key=lambda n: self._node_to_index[n]))

    def reached_fixedpoint(self, node):
        '''
        Mark a node as reached fixed point. This node as well as its successors will not be visited in the future.

        :param node: The node to mark as reached fixed-point.
        :return: None
        '''

        self._reached_fixedpoint.add(node)

class FunctionGraphVisitor(GraphVisitor):
    def __init__(self, func, graph=None):
        '''
        :param knowledge.func func:
        '''
        super(FunctionGraphVisitor, self).__init__()

        self.function = func

        if graph is None:
            self.graph = self.function.graph

        else:
            self.graph = graph

    def startpoints(self):

        return [self.function.startpoint]

    def successors(self, node):
        return list(self.graph.successors(node))

    def predecessors(self, node):
        return list(self.graph.predecessors(node))

    def sort_nodes(self, nodes=None):
        sorted_nodes = CFGUtils.quasi_topological_sort_nodes(self.graph)

        if nodes is not None:
            sorted_nodes = [n for n in sorted_nodes if n in set(nodes)]

        return sorted_nodes

    def startpoints(self):

        # TODO: make sure all connected components are covered

        start_nodes = [node for node in self.callgraph.nodes() if self.callgraph.in_degree(node) == 0]

        if not start_nodes:
            # randomly pick one
            start_nodes = [self.callgraph.nodes()[0]]

        return start_nodes

    def successors(self, node):
        return list(self.callgraph.successors(node))

    def predecessors(self, node):

        return list(self.callgraph.predecessors(node))

    def sort_nodes(self, nodes=None):
        sorted_nodes = CFGUtils.quasi_topological_sort_nodes(self.callgraph)

        if nodes is not None:
            sorted_nodes = [n for n in sorted_nodes if n in set(nodes)]

        return sorted_nodes

class SingleNodeGraphVisitor(GraphVisitor):
