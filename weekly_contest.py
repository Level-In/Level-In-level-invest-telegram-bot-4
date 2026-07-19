import os
import sys

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


PHOTO_CANDIDATES = [
    "konkurs_tygodniowy.png",
    "konkurs tygodniowy.png",
    "konkurs_tygodniowy.jpg",
    "konkurs tygodniowy.jpg",
    "konkurs_tygodniowy.jpeg",
    "konkurs tygodniowy.jpeg",
]


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


def find_photo_path() -> str:
    for photo_path in PHOTO_CANDIDATES:
        if os.path.exists(photo_path):
            print(f"Znaleziono grafikę: {photo_path}")
            return photo_path

    print("Nie znaleziono grafiki konkursowej.")
    print("Pliki widoczne w repozytorium:")

    for file_name in os.listdir("."):
        print(file_name)

    sys.exit(1)


def send_photo(chat_id: str, photo_path: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"

    try:
        with open(photo_path, "rb") as photo:
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

        print(f"PHOTO CHAT_ID={chat_id} STATUS={response.status_code}")
        print(f"PHOTO RESPONSE={response.text}")

        if response.ok:
            print(f"Grafika wysłana do {chat_id}")
            return True

        print(f"Nie udało się wysłać grafiki do {chat_id}")
        return False

    except FileNotFoundError:
        print(f"Nie znaleziono pliku grafiki: {photo_path}")
        return False

    except requests.RequestException as error:
        print(f"Błąd połączenia przy wysyłce grafiki do {chat_id}: {error}")
        return False


def send_text(chat_id: str, text: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": text,
                "disable_web_page_preview": True,
            },
            timeout=30,
        )

        print(f"TEXT CHAT_ID={chat_id} STATUS={response.status_code}")
        print(f"TEXT RESPONSE={response.text}")

        if response.ok:
            print(f"Tekst wysłany do {chat_id}")
            return True

        print(f"Nie udało się wysłać tekstu do {chat_id}")
        return False

    except requests.RequestException as error:
        print(f"Błąd połączenia przy wysyłce tekstu do {chat_id}: {error}")
        return False


def main() -> None:
    photo_path = find_photo_path()
    success_count = 0

    for chat_id in CHAT_IDS:
        print("=" * 60)
        print(f"Wysyłam konkurs do grupy: {chat_id}")

        photo_ok = send_photo(chat_id, photo_path)

        if not photo_ok:
            print(f"Grafika nie została wysłana do {chat_id}. Nie wysyłam samego tekstu.")
            continue

        text_ok = send_text(chat_id, MESSAGE_TEXT)

        if photo_ok and text_ok:
            success_count += 1
            print(f"Komplet wysłany poprawnie do {chat_id}")
        else:
            print(f"Nie wysłano kompletu do {chat_id}")

    print("=" * 60)
    print(f"Wysłano grafikę i tekst do {success_count}/{len(CHAT_IDS)} grup.")

    if success_count != len(CHAT_IDS):
        print("Nie wszystkie grupy dostały komplet. Sprawdź uprawnienia bota do wysyłania multimediów.")
        sys.exit(1)


if __name__ == "__main__":
    main()
