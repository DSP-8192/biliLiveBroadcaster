call nuitka --mingw64 --standalone --show-progress --remove-output ^
--windows-icon-from-ico=.\lizi.ico ^
--plugin-enable=numpy ^
--follow-imports ^
--output-dir=nuitka_dist ^
--onefile ^
main.py

pause
