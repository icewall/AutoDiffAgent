#include <MsgBoxConstants.au3>
$old_db = "t:\tmp\gdi32\old\SP3QFE\gdi32.idb"
$bd_db = "t:\tmp\gdi32\gdi32_vs_gdi32.BinDiff"
$exit_script = "t:\projects\Cisco\Code\AutoDiff\AutoDiff\agent\IDAScripts\exit.py"

WinWait("zynamics BinDiff 4.0.0")
WinActivate("zynamics BinDiff 4.0.0")
send("{ENTER}")
WinWait("Select Database")
sleep(1000)
send($old_db)
send("{ENTER}")
WinWaitClose("zynamics BinDiff 4.0.0")
send("{CTRLDOWN}")
send("6")
send("{CTRLUP}")
WinWait("zynamics BinDiff 4.0.0")
send("{DOWN}")
send("{DOWN}")
send("{DOWN}")
send("{DOWN}")
send("{ENTER}")
WinWait("Save Results As")
sleep(1000)
send($bd_db)
send("{ENTER}")
sleep(2000)
WinWaitActive("zynamics BinDiff 4.0.0")
send("{DOWN}")
send("{DOWN}")
send("{ENTER}")
send("{ALTDOWN}")
send("{F7}")
send("{ALTUP}")
sleep(1000)
send($exit_script)
send("{ENTER}")
sleep(1000)