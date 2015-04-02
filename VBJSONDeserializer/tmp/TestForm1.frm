VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} TestForm1 
   Caption         =   "UserForm1"
   ClientHeight    =   5060
   ClientLeft      =   0
   ClientTop       =   -1320
   ClientWidth     =   7060
   OleObjectBlob   =   "TestForm1.frx":0000
   StartUpPosition =   1  'CenterOwner
   Begin VB.CheckBox CheckShowNames 
      Caption         =   "Show Names"
      Height          =   255
      Left            =   9600
      TabIndex        =   9
      Top             =   1440
      Width           =   1815
   End

End
Attribute VB_Name = "TestForm1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub TestButton1_Click()
    
    Dim MyNummber As Integer
    
    MyNumber = 10
    
    If MyNumber = 10 Then
    
    MsgBox "Number = 10"
    
    End If
End Sub

