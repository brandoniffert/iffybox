import os
import subprocess


class Speaker:
    def say(self, message, voice='Alex'):
        subprocess.check_call(['/usr/local/Cellar/switchaudio-osx/1.0.0/bin/SwitchAudioSource',
                               '-s', 'Built-in Output'], stdout=open(os.devnull, 'wb'))
        subprocess.check_call(['say', '-v', voice, message])
