import sys

def main(foo, bar, **cmd_line_args):
    print('Called myscript with:')
    print('foo = {}'.format(foo))
    print('bar = {}'.format(bar))
    for k, v in cmd_line_args.items():
        print('keyword argument: {} = {}'.format(k, v))

if __name__=='__main__':
    main(sys.argv[1], # foo
         sys.argv[2], # bar
         **dict(arg.split('=') for arg in sys.argv[3:])) # kwargs

# Example use:
# $ python myscript.py foo bar hello=world 'with spaces'='a value'
# Called myscript with:
# foo = foo
# bar = bar
# keyword argument: hello = world
# keyword argument: with spaces = a value