#!/usr/bin/env python
import argparse
import os
import re
import readline
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Determine dependencies for a LaTeX/PDF/pmd document project.')
    parser.add_argument('dep', type=str, help='The target dependent file we are searching for dependencies.')

    args = parser.parse_args()
    
    pfigs = re.compile('^.*(figures/.*\.png).*$')
    pbibs = re.compile('^.*bibliography\{(.*)\}.*$')

    for line in sys.stdin.readlines():
        # search for included figure dependencies
        m = pfigs.match(line)
        if m:
            print("%s: %s" % (args.dep, m.group(1)) )

        # search for bibliography dependencies
        m = pbibs.match(line)
        if m:
            # can be a comma separated list
            bib_names = m.group(1).split(',')
            for bib_name in bib_names:
                bib_name = bib_name.strip()
                _, bib_ext = os.path.splitext(bib_name)
                if bib_ext != '.bib':
                    bib_name += '.bib'
                print("%s: %s" % (args.dep, bib_name) )
        
