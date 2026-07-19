import os
import sys
from datetime import datetime, date
from zoneinfo import ZoneInfo

import requests


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    print("Brak zmiennej środowiskowej TELEGRAM_TOKEN")
    sys.exit(1)


CHAT_IDS = [
    "-1004231126426",
    "-1004249984029",
    "-1003932802265",
]


START_DATE = date.fromisoformat("2026-07-20")
TIMEZONE = ZoneInfo("Europe/Warsaw")

PHOTO_PATH = "konkurs_tygodniowy.png"

FORCE_SEND = os.getenv("FORCE_SEND", "false").lower() in ("1", "true", "yes", "tak")


MESSAGE_TEXT = """⚡ KONKURS TYGODNIOWY

Każdy tydzień to nowa szansa na dodatkową premię! Nie odkładaj wyniku na koniec miesiąca. Zacznij mocno od pierwszego dnia i pokaż, na co Cię stać! 🔥

🥉 3 umowy najmu w tygodniu to premia 300 zł

🥈 4 umowy najmu w tygodniu to premia 600 zł

🥇 5 umów najmu w tygodniu to aż 1 000 zł premii 💰🎉

Jeden dobry tydzień może znacząco zwiększyć Twoją wypłatę. Pięć umów to konkretny cel, konkretna nagroda i ogromna satysfakcja! 💪😎

📌 Warunki konkursu tygodniowego

✅ Umowy muszą być poprawnie zdane i wolne od błędów formalnych

✅ Premie zostaną wypłacone razem z bieżącym wynagrodzeniem za dany miesiąc

✅ Premia zostanie wypłacona po osiągnięciu minimum 6 wynajętych nieruchomości w miesiącu

🚀 DZIAŁAMY PO WYNIKI

Nie licz dni. Nie czekaj na okazję. Twórz okazje! 🔥

Każdy telefon może zakończyć się spotkaniem. Każde spotkanie może zakończyć się umową. Każda umowa przybliża Cię do premii! 💰

🎯 Ustal swój cel

📞 Zwiększ aktywność

🤝 Dbaj o jakość obsługi

📝 Pilnuj poprawności dokumentów

🏆 Walcz o najwyższy próg

Wynik jest w Twoich rękach. Czas włączyć pełną moc i sięgnąć po dodatkowe pieniądze! 💪🔥💸"""


def send_photo(chat_id: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"

    try:
        with open(PHOTO_PATH, "rb") as photo:
            response = requests.post(
                url,
                data={
                    "chat_id": chat_id,
                },
                files={
                    "photo": photo,
                },
                timeout=30,
            )

        print(f"PHOTO CHAT_ID={chat_id} STATUS={response.status_code} RESPONSE={response.text}")
        return response.ok

    except FileNotFoundError:
        print(f"Nie znaleziono pliku zdjęcia: {PHOTO_PATH}")
        return False

    except requests.RequestException as error:
        print(f"Błąd połączenia przy wysyłce zdjęcia do {chat_id}: {error}")
        return False


def send_text(chat_id: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": MESSAGE_TEXT,
                "disable_web_page_preview": True,
            },
            timeout=30,
        )

        print(f"TEXT CHAT_ID={chat_id} STATUS={response.status_code} RESPONSE={response.text}")
        return response.ok

    except requests.RequestException as error:
        print(f"Błąd połączenia przy wysyłce tekstu do {chat_id}: {error}")
        return False


def should_send_today() -> bool:
    today = datetime.now(TIMEZONE).date()
    weekday = today.weekday()

    print(f"Dzisiejsza data: {today.isoformat()}")
    print(f"Dzień tygodnia numer: {weekday}")
    print(f"FORCE_SEND={FORCE_SEND}")

    if FORCE_SEND:
        print("Tryb testowy FORCE_SEND=true. Wysyłam mimo daty i dnia tygodnia.")
        return True

    if today < START_DATE:
        print(f"System konkursowy startuje od {START_DATE.isoformat()}. Dzisiaj brak wysyłki.")
        return False

    if weekday != 0:
        print("Dzisiaj nie jest poniedziałek. Brak wysyłki konkursu.")
        return False

    return True


def main() -> None:
    if not should_send_today():
        return

    success_count = 0

    for chat_id in CHAT_IDS:
        photo_ok = send_photo(chat_id)
        text_ok = send_text(chat_id)

        if photo_ok and text_ok:
            success_count += 1

    print(f"Wysłano komplet zdjęcie plus tekst do {success_count}/{len(CHAT_IDS)} grup.")

    if success_count != len(CHAT_IDS):
        sys.exit(1)


if __name__ == "__main__":
    main()
