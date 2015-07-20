import subprocess


def say(message):
    subprocess.check_call(['espeak', "{}".format(message)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
