@ECHO OFF
SETLOCAL
SET BASEDIR=%~dp0

REM Python�̗L�����`�F�b�N����B
python -V
IF NOT ERRORLEVEL 1 GOTO END_PYTHON_CHECK
ECHO Vim�̎����X�V�𗘗p����ɂ�Python���C���X�g�[�����Ă��������B
GOTO END_FAILURE
:END_PYTHON_CHECK

REM �f�B���N�g���\���𒲍�����B
IF EXIST "%BASEDIR%"vim-online-update.py GOTO FOUND_CURR
IF EXIST "%BASEDIR%"online-update\vim-online-update.py GOTO FOUND_BOTTOM
ECHO �X�V�p�X�N���v�g��������܂���B
GOTO END_FAILURE
:FOUND_CURR
SET SCRIPT=%BASEDIR%vim-online-update.py
SET TARGET_DIR=%BASEDIR%var\vim73
GOTO END_DIR_CHECK
:FOUND_BOTTOM
SET SCRIPT=%BASEDIR%online-update\vim-online-update.py
SET TARGET_DIR=%BASEDIR%
SET PYTHONPATH=%BASEDIR%online-update
GOTO END_DIR_CHECK
:END_DIR_CHECK

ECHO Vim�̍X�V���ł��B���΂炭���҂����������B
IF EXIST "%TARGET_DIR%"online-update\var\recipe.txt DEL /F /Q "%TARGET_DIR%"online-update\var\recipe.txt
python "%SCRIPT%" "%TARGET_DIR%"
IF ERRORLEVEL 2 GOTO END_FAILURE
IF ERRORLEVEL 1 GOTO END_SUCCESS
GOTO END_NOTUPDATED

:END_FAILURE
ECHO Vim�̍X�V�Ɏ��s���܂����B
GOTO END
:END_NOTUPDATED
ECHO Vim�̍X�V�͂���܂���ł����B
GOTO END
:END_SUCCESS
ECHO Vim�̍X�V���������܂����B
GOTO END

:END
ECHO ��10�b��ɂ��̃E�B���h�E�͎����I�ɕ��܂��B
PING localhost -n 10 > nul
