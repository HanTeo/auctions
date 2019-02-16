import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src')


def get_stdout(capsys):
    out, err = capsys.readouterr()
    out = [o for o in out.split('\n') if o != '']
    err = [o for o in err.split('\n') if o != '']
    return out, err
