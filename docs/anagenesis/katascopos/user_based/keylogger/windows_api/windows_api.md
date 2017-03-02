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
**Current version**: 0.3

**Efficency**: **Low**

# Behavior
## v.0.3
* **NF** Now write also datetime in log file

## v.0.2
* **NF** Now regist also mouse clicks.

## v.0.1
This keylogger, when launched, starts an hidden windows that quietly regist every keystrokes pressed and save them on a log file.


# To Do
*for more informations see [*To-Do*](../../../../../to-do.md)*
## keylogger.cpp
* [X] add mouse events
* [X] write datetime
* [ ] send HTTPS POST request
* [ ] starts when user log on

## Tools
### analyzer.py
* [x] encrypt option
* [x] command line control (pause and continue)
* [X] tidy code
* [X] refine username recognition
* [ ] modes (MySQL, file txt, ...)
* [ ] check file extension
* [ ] progesses bar
