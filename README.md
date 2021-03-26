# py_exchange

This simple script scraps hardcoded page of a website for links to .xls files; 
searches them for file named by specific pattern;
downloads it; 
selects only several needed lines;
saves this file with very basic formatting and sends it by email.

It was written to practice scripting with python and to automate simple routine task.

## How to use

This repo consists of two files: *import.py* script itself and simple *import.ini*
The very basic use is to save those files in any folder and run 
```
import.py
```
You, obviously, should have installed python.
If python asks for missing modules - just install them using pip
```
pip install module_name
```
If you have no idea what is pip, you can make yourself aquainted with it here:
https://pypi.org/project/pip/

You need to edit import.ini and replace fictional values of 
_mail_from_, _mail_to_ and _smtp_server_ip_ with real ones.

This is very simple example so smtp server must be without authorization and accepting
mails from _mail_from_ address, or it will reject sending mail

The result of the succesful run is .xlsx file saved in same folder and e-mail containing 
same file in your mailbox (_mail_to_).
For the site, used in this script fresh files appear on workdays, around 13:00 GMT

This repo is absolutely free to use for anyone. You can, with little effort, add smtp 
authorization, select another lines from file and make more fancy formatting by 
studying docs of used modules and editing script.

© Markov Dmitriy, 2021.
