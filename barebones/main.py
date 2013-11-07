#!/usr/bin/env python3

import barebones
import sys

for filename in sys.argv[1:]:
    barebones.Interpreter(filename).run()
