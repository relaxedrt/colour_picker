@echo off

:start
cls

set python_ver=36

cd \
cd \python%python_ver%\Scripts\
pip install opencv-python
pip install pyserial
pip install logging

pause
exit