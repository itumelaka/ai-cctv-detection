Set WshShell = CreateObject("WScript.Shell")

scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
batPath = scriptDir & "\run_monitor_person_all_once.bat"

WshShell.Run """" & batPath & """", 0, True
