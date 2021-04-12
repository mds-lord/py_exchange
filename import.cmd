e:
rem set PATH=%PATH%;c:\users\dmarkov\appdata\local\packages\pythonsoftwarefoundation.python.3.9_qbz5n2kfra8p0\localcache\local-packages\python39\site-packages
rem echo %PATH%
cd e:\work\py_exchange
pip install -r .\requirements.txt > 1.txt 2>&1
python e:\work\py_exchange\import.py >> 1.txt 2>&1
rem c:\windows\py.exe e:\work\py_exchange\import.py >> 1.txt 2>&1
exit