import subprocess


def say(message):
    subprocess.check_call(['espeak', '-s', '140', "{}".format(message)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
