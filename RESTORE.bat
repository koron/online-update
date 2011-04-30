@ECHO OFF
SETLOCAL
SET BASEDIR=%~dp0

REM TODO:Pythonの有無をチェックする。

REM 環境を調査する。
IF EXIST "%BASEDIR%"vim-online-update.py GOTO FOUND_CURR
IF EXIST "%BASEDIR%"online-update\vim-online-update.py GOTO FOUND_BOTTOM
ECHO 更新用スクリプトが見つかりません。
GOTO END_FAILURE
:FOUND_CURR
SET SCRIPT=%BASEDIR%vim-online-update.py
SET TARGET_DIR=%BASEDIR%var\vim73
GOTO START_UPDATE
:FOUND_BOTTOM
SET SCRIPT=%BASEDIR%online-update\vim-online-update.py
SET TARGET_DIR=%BASEDIR%
SET PYTHONPATH=%BASEDIR%online-update
GOTO START_UPDATE

:START_UPDATE
ECHO Vimの復元中です。しばらくお待ちください。
CD "%BASEDIR%"
IF EXIST %TARGET_DIR%var\online-update\recipe.txt DEL /F /Q %TARGET_DIR%var\online-update\recipe.txt
python "%SCRIPT%" %TARGET_DIR%
REM TODO:エラー処理
GOTO END_SUCCESS

:END_FAILURE
ECHO Vimの復元に失敗しました。
GOTO END
:END_SUCCESS
ECHO Vimの復元を完了しました。
GOTO END
:END
ECHO 約10秒後にこのウィンドウは自動的に閉じます。
PING localhost -n 10 > nul
