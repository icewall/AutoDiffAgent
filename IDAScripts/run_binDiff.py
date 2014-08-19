from idaapi import *
from idautils import *

import subprocess
import time

if __name__ == '__main__':
    autoWait()
    subprocess.Popen([r"c:\Program Files (x86)\AutoIt3\AutoIt3_x64.exe", r"t:\projects\Cisco\Code\AutoDiff\AutoDiff\agent\Au3\bindiffer.au3"])
    plugin = load_plugin(r"d:\IDA_6.6\plugins\zynamics_bindiff_4_0.plw")
    print run_plugin(plugin, 0)
