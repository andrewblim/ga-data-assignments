
import sys

def run_code_block(name):
    args = sys.argv[1:]
    if str(name) in args or 'all' in args: return True
    else: return False