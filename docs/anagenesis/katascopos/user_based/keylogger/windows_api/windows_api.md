# Nomenclature
*for the nomenclature see [Nomenclature](../../../../nomenclature.md)*

| Kinds       | Names        |
|-------------|--------------|
| **Kingdom** | *Anagenesis* |
| **Class**   | *Katascopos* |
| **Order**   | *User Based* |
| **Family**  | *Keylogger*  |
| **Species** | [*API keylogger*](https://en.wikipedia.org/wiki/Keystroke_logging#Software-based_keyloggers) |

# Technical Specifications
**Current version**: 0.2

**Efficency**: **Low**

# Behavior
## v.0.2
### NEW FEATURE
Now regist also mouse clicks.

## v.0.1
This keylogger, when launched, starts an hidden windows that quietly regist every keystrokes pressed and save them on a log file.


# To Do
*for more informations see [*To-Do*](../../../../../to-do.md)*
## keylogger.cpp
* [X] add mouse events
* [ ] write datetime
* [ ] send HTTPS POST request
* [ ] starts when user log on

## Tools
### analyzer.py
* [x] encrypt option
* [x] command line control (pause and continue)
* [ ] check file extension
* [ ] modes (MySQL, file txt, ...)
* [ ] progesses bar
* [ ] tidy code
* [ ] refine username recognition
