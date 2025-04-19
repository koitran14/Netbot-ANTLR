#!/bin/bash
java -jar lib/antlr4-4.9.2-complete.jar -Dlanguage=Python3 -visitor -o src/generated src/grammar/Command.g4