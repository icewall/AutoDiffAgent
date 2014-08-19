$old_db = "t:\projects\Cisco\Code\AutoDiff\samples\GDI\old\gdi32.idb"
$bd_db = "t:\projects\Cisco\Code\AutoDiff\samples\GDI\gdi32_vs_gdi32.BinDiff"
$exit_script = "t:\projects\Cisco\Code\AutoDiff\AutoDiff\agent\IDAScripts\exit.py"

WinWait("zynamics BinDiff 4.0.0")
send("{ENTER}")
ConsoleWrite("Waiting for database window")
WinWait("Select Database")
sleep(1000)
send($old_db)
