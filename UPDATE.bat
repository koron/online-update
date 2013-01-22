@ECHO OFF
SETLOCAL
SET BASEDIR=%~dp0

REM Python�̗L�����`�F�b�N����B
python -V > NUL 2>&1
IF NOT ERRORLEVEL 1 GOTO END_PYTHON_CHECK
ECHO Vim�̎����X�V�𗘗p����ɂ�Python���C���X�g�[�����Ă��������B
GOTO END
:END_PYTHON_CHECK

REM �f�B���N�g���\���𒲍�����B
IF EXIST "%BASEDIR%"vim-online-update.py GOTO FOUND_SCRIPT
ECHO �X�V�p�X�N���v�g��������܂���B
GOTO END
:FOUND_SCRIPT
SET SCRIPT=%BASEDIR%vim-online-update.py
SET TARGET_DIR=%BASEDIR%

REM �X�N���v�g���s�B
python "%SCRIPT%" "%TARGET_DIR%"

:END
ECHO ��10�b��ɂ��̃E�B���h�E�͎����I�ɕ��܂��B
PING localhost -n 10 > nul
