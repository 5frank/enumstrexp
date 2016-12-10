menumstr - make enum strings automagically. Work in progress.

Features
========
- alter the string representation. remove a common prefix, change to lower case etc.
- enums used as bitflags (compiler error if enum with multiple bits set)
- separate enum definition and their string representation.
useful if you have 6000 error codes defined as enums in a Arduino/MCU
and the string table doesnt fit.
- handle duplicate enum members
