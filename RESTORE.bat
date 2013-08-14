@ECHO OFF
SETLOCAL
SET BASEDIR=%~dp0

REM Pythonの有無をチェックする。
python -V > NUL 2>&1
IF NOT ERRORLEVEL 1 GOTO END_PYTHON_CHECK
ECHO Vimの自動更新を利用するにはPythonをインストールしてください。
GOTO END
:END_PYTHON_CHECK

REM ディレクトリ構成を調査する。
IF EXIST "%BASEDIR%"vim-online-update.py GOTO FOUND_SCRIPT
ECHO 更新用スクリプトが見つかりません。
GOTO END
:FOUND_SCRIPT
SET SCRIPT=%BASEDIR%vim-online-update.py
SET TARGET_DIR=%BASEDIR%

REM データファイル削除。
IF EXIST "%TARGET_DIR%"online_updater\var\vim74-anchor.txt DEL /F /Q "%TARGET_DIR%"online_updater\var\vim74-anchor.txt
IF EXIST "%TARGET_DIR%"online_updater\var\vim74-recipe.txt DEL /F /Q "%TARGET_DIR%"online_updater\var\vim74-recipe.txt

REM スクリプト実行。
python "%SCRIPT%" "%TARGET_DIR%"

:END
ECHO 約10秒後にこのウィンドウは自動的に閉じます。
PING localhost -n 10 > nul
