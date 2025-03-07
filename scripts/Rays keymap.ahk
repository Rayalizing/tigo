;=====================================================================o
;                       CapsLock Initializer
;---------------------------------------------------------------------o
SetCapsLockState, AlwaysOff
;-----------------------------------o---------------------------------o


;=====================================================================o
;                    CapsLock Direction Navigator
;-----------------------------------o---------------------------------o
;                      CapsLock + a |  Left  (附：再加上Ctrl后变Home)
;                      CapsLock + s |  Down
;                      CapsLock + w |  Up
;                      CapsLock + d |  Right (附：再加上Ctrl后变End)
;                      Ctrl, Alt Compatible
;-----------------------------------o---------------------------------o
CapsLock & a::
if GetKeyState("control") = 0
{
    if GetKeyState("alt") = 0
  Send, {Left}
    else
  Send, +{Left}
    return
}
else{
    if GetKeyState("alt") = 0
  Send, {Home}
    else
  Send, +^{Left}
    return
}
return
;-----------------------------------o
CapsLock & s::
if GetKeyState("control") = 0
{
    if GetKeyState("alt") = 0
  Send, {Down}
    else
  Send, +{Down}
    return
}
else{
    if GetKeyState("alt") = 0
  Send, ^{Down}
    else
  Send, +^{Down}
    return
}
return
;-----------------------------------o
CapsLock & w::
if GetKeyState("control") = 0
{
    if GetKeyState("alt") = 0
  Send, {Up}
    else
  Send, +{Up}
    return
}
else{
    if GetKeyState("alt") = 0
  Send, ^{Up}
    else
  Send, +^{Up}
    return
}
return
;-----------------------------------o
CapsLock & d::
if GetKeyState("control") = 0
{
    if GetKeyState("alt") = 0
  Send, {Right}
    else
  Send, +{Right}
    return
}
else{
    if GetKeyState("alt") = 0
  Send, {End}
    else
  Send, +^{Right}
    return
}
return




;=====================================================================o
;                      CapsLock Page Navigator
;-----------------------------------o---------------------------------o
;                      CapsLock + r |  PageUp
;                      CapsLock + f |  PageDown
;                      Ctrl, Alt Compatible
;-----------------------------------o---------------------------------o
CapsLock & r::
if GetKeyState("control") = 0
{
    if GetKeyState("alt") = 0
  Send, {PgUp}
    else
  Send, +{PgUp}
    return
}
else{
    if GetKeyState("alt") = 0
  Send, ^{PgUp}
    else
  Send, +^{PgUp}
    return
}
return
;-----------------------------------o
CapsLock & f::
if GetKeyState("control") = 0
{
    if GetKeyState("alt") = 0
  Send, {PgDn}
    else
  Send, +{PgDn}
    return
}
else{
    if GetKeyState("alt") = 0
  Send, ^{PgDn}
    else
  Send, +^{PgDn}
    return
}
return


;=====================================================================o
;                              DIY Area
;-----------------------------------o---------------------------------o
CapsLock & q:: Send, !{Left}    ;CapsLock + q = Alt + Left       后退
CapsLock & e:: Send, !{Right}   ;CapsLock + e = Alt + Right      前进

LCtrl & Backspace:: Send, {Delete}
Ctrl & Left:: Send, {Home}
Ctrl & Right:: Send, {End}

CapsLock & c:: Send, !c             ;用于唤醒CopyQ剪贴板
CapsLock & x:: Send, !x             ;用于划词翻译
CapsLock & z:: Send, !z             ;用于输入翻译
CapsLock & Space:: Send, !v         ;用于截图翻译

LWin & c:: Send, ^c
LWin & e:: Send, #{Tab}
LWin & q:: Send, #^{Left}
LWin & r:: Send, #^{Right}


;=====================================================================o
;                            打字手感设置
;-----------------------------------o---------------------------------o
;numpad设置（为了在数字键盘上用九键打字）：
SetNumLockState, AlwaysOn      ;NumLock Initializer:
NumLock:: Send, 0              ;将numlock改为数字0
NumpadSub:: Send, {BackSpace}  ;将数字键盘的减号改为退格键
NumpadAdd:: Send, {Space}      ;将数字键盘的+改为空格键
Numpad0:: Send, {;}            ;将数字键盘的0改为分号
;-----------------------------------o
CapsLock:: Send, {'}      ;CapsLock 单击设为单引号(不会影响其组合键的使用)
;-----------------------------------o---------------------------------o