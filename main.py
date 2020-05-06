from Scanner import Scanner
from Parser import Parser
from pathlib import Path

import sys

def main():
    fileArg = sys.argv[1]
    path = Path('.')
    filePath = path / fileArg

    with open(filePath) as f:
        content = f.read()
        try:
            parser = Parser(content)
            parser.parse()
        except:
            print('error')

if __name__ == '__main__':
    main()