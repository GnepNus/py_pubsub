call C:\dev\ros2_foxy\local_setup.bat
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64
@REM 自定义的接口的环境
call D:\dev\ros2_cpp_ws\install\local_setup.bat
set PYTHONPATH=D:\dev\ros2_ws\src\py_pubsub;%PYTHONPATH%
python D:\dev\ros2_ws\src\py_pubsub\py_pubsub\publisher.py