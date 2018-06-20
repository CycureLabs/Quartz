import os
import logging
from pwn import *
import subprocess


# This file generates a class Preprocess which return some binary info
# and generates the executable to be exploited, and it's bytecode to
# analyze.
# It compiles the given source code using two compilers, GCC compiler
# as mentioned in AEG Documentation to create binary we need to
# exploit and secondly using LLVM to generate bytecodes for further
# analysis.

__author__ = 'Rajesh'

l = logging.getLogger("Quartz.preprocess")

class Preprocess(object):
    LEAKS = ['puts', 'printf']

    def __init__(self, source):
        self.source = source
        self.result = None
        self.results = []
        #self.binary = ''

    def _compile_gcc(self):
        # This function would simply generate an executable binary
        # using gcc compiler, to exploit
        #files = os.listdir(self.path)
        l.debug("Generating executable binary using GCC Compiler.")
        gcc_command = 'gcc ' + self.source + '-o gcc_binary -fno-stack-protector'
        #for f in files:
            # Tried an inefficient way, but gets the work done.
            # Hopefully would find a better way
         #   command += self.path + '/' + str(f) + ' '

        # Here trying to be simple by disabling stack protection,
        # In future if possible will remove this.
        #command += '-o gcc_binary -fno-stack-protector'

        os.system(gcc_command)
        #self.binary = self.path + '/gcc_binary'

    def _generate_bytecodes(self):
        l.debug("Generating bytecode using LLVM-GCC Compiler.")
        llvm_command = 'llvmgcc '+self.source+' -c -o llvm_bytecode'
        os.system(llvm_command)

    def _get_binary_info(self):

        # This function will get some binary info using
        # pwntools ELF module and ldd commands output.

        elf = ELF(self.path + '/gcc_binary')
        self.result['elf'] = {
            'RELRO': elf.relro,
            'Canary': elf.canary,
            'NX' : elf.nx,
            'PIE': elf.pie,
        }

        ldd_output = subprocess.getoutput('ldd %s' % self.binary).split('\n')
        lib = filter(lambda lib: 'libc.so.6' in lib, ldd_output)[0]

        # I am not that good in using re module in python, this might not give
        # expected results, might need to rework on this part.
        self.result['elf']['libc'] = re.findall('=> (*.) \(', lib)[0]

        self.result['elf']['leak_symbol'] = []
        for leak in Preprocess.LEAKS:
            if leak in elf.symbols:
                self.result['elf']['leak_symbol'].append(leak)

    def preprocess(self):
        self._get_binary_info()
        l.debug("Preprocessing...")
        self.results.append(self.result)
        return self.result
