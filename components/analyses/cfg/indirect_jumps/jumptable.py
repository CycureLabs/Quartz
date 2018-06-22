import logging
from collection import defaultdict

import pyvex


from ....errors import QrtzError, SimError
from .... import sim_options as o
from .resolver import IndirectJumpResolver

from ....blade import Blade
from ....annocfg import AnnotatedCFG
from .... import BP, BP_BEFORE
from ....surveyors import Slicecutor

l = logging.getLogger("Quartz.components.analyses.indirect_jumps.jumptable")

class UninitReadMeta(object):
    uninit_read_base = 0xc000000

class JumpTableResolver(IndirectJumpResolver):

    def __init__(self, project):
        super(JumpTableResolver, self).__init__(project, timeless=False)

        self._bss_regions = None

        self._max_targets = None

        self._find_bss_region()


