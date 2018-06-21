import networkx

from claripy.utils.orderedset import OrderedSet

from ..misc.ux import deprecated
from ..errors import QrtzForwardAnalysisError
from ..error import QrtzSkipJobNotice, QrtzDelayJobNotice, QrtzJobMergingFailureNotice, QrtzJobWideningFailureNotice
from .cfg.cfg_utils import CFGUtils


'''
:TODO: A class that takes a node in the graph and returns its successors.
'''
