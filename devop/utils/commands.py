import subprocess


def getstatusoutput(cmd):
    cmd = cmd.split()
    try:
        out_bytes = subprocess.check_output(cmd)
        code = 0
    except subprocess.CalledProcessError as e:
        out_bytes = e.output
        code = e.returncode
    return (code, out_bytes)
