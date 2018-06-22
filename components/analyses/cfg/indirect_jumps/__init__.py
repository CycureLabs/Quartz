'''
Code from angr framework for python
https://github.com/angr/angr

Modified some code for Quartz.
'''

from .mips_elf_fast import MipsElfFastResolver
from .x86_elf_pic_plt import X86ElfPicPltResolver
from .jumptable import JumpTableResolver
from .x86_pe_iat import X86PeIatResolver
