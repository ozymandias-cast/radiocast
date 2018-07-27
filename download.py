import podb
import debug_output
import requests

class download:
    def __init__(self,p,o):
        self.o = o
        self.p = p
        return None

    def now(self):
        rows = self.p.missing_episodes()
        for row in rows:
            pod = self.p.decode_episode(row)
            self.o.output(1,"Downloading episode %s %s %s" % (str(pod.p_title), str(pod.e_title), str(pod.file)),None)
            r = requests.get(pod.file, allow_redirects=True)
            pod.mp3 = r.content
            self.p.write_mp3(pod)


