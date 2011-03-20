#/bin/bash
# 
#  compile_frag.sh
#  fastFrag
#  
#  Created by gregory tomlinson on 2011-03-19.
#  Copyright 2011 the public domain. All rights reserved.
# 
# just a one liner to compile, based on the location of the closure jar from my machine
java -jar ../../website/tools/closure_compiler.jar --js=../js/fastFrag.js --js_output_file=../js/fastFrag.min.js