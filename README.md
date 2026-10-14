# Pliki konkursu tygodniowego Telegram

To repozytorium przechowuje skrypt `weekly_contest.py`, grafikę `konkurs_tygodniowy.png` i zależności.

Automatyczna wysyłka jest uruchamiana z repozytorium
[Level-In-level-invest-telegram-bot-5](https://github.com/Level-In/Level-In-level-invest-telegram-bot-5/actions/workflows/weekly_contest.yml)
w poniedziałki o **11:35 Europe/Warsaw**, z automatyczną obsługą zmiany czasu.
Workflow pobiera bieżące pliki z gałęzi `main` tego repozytorium i korzysta ze sprawdzonego sekretu Telegram w bot-5.

Tutaj nie ma aktywnego harmonogramu. Ręczny workflow jest zachowany jako wersja historyczna;
zapisany w tym repozytorium sekret Telegram nie przeszedł testu połączenia podczas migracji.
Do testu lub ręcznej wysyłki używaj Actions w repozytorium bot-5.
