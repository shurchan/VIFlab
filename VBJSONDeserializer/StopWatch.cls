BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "StopWatch"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Private mlngStart As Long
Private Declare Function GetTickCount Lib "kernel32" () As Long

Public Sub StartTimer()
    mlngStart = GetTickCount
End Sub

Public Function EndTimer() As Long
    EndTimer = (GetTickCount - mlngStart)
End Function