# py2025-project-v1

## Temat projektu:

Stwórz system symulujący pracę kilku czujników (np. temperatury, wilgotności, ciśnienia) w środowisku monitoringu. System będzie generował dane w czasie rzeczywistym, zapisywał je na dysk, umożliwiał ich analizę i wizualizację oraz udostępniał dane przez prostą komunikację sieciową. Dodatkowo, system będzie posiadał prosty graficzny interfejs użytkownika (GUI).

---

## Uruchamianie:
```py  start_server.py ``` uruchamia nam serwer
```py start_client.py``` uruchamia nam klienta z GUI

### Główne funkcjonalności:

**Symulacja czujników:** Za pomocą generatorów i metod losowych (z wykorzystaniem Numpy) symulowane będą odczyty z czujników.

**Logowanie danych:** Dane z czujników będą zapisywane do plików csv.

**Serializacja konfiguracji:** System będzie umożliwiał zapisywanie i odczytywanie konfiguracji czujników przy użyciu JSON.

**Komunikacja sieciowa:** Realizacja prostego serwera-klienta wykorzystującego gniazda (sockets) do przesyłania danych z czujników na odległy terminal lub aplikację.

**GUI:** Implementacja interfejsu graficznego (przy użyciu Tkinter), który pozwoli na uruchomienie symulacji, podgląd odczytów oraz sterowanie pracą systemu.
         GUI WYKONANE NA WŁASNY SPOSÓB, działa ono na kliencie, korzysta z modułu sensor aby logger aby ściągać informacje o sensorach, pozwala na modyfikowanie aktualnych konfiguracji sensorów oraz podgląd do wykresu ostatnich wartości sensorów w czasie rzeczywistym

**Analiza i wizualizacja danych:** Przygotowanie Jupyter Notebooka, w którym dane z czujników zostaną zanalizowane przy użyciu Numpy, Scipy, Matplotlib oraz Pandas, a wyniki zaprezentowane graficznie.

## Propozycja podziału pracy i wskazówki implementacyjne

### Architektura i podział modułów

    Moduł czujników:
    Implementacja klas czujników oraz generatorów symulujących dane. Zadaniem tego modułu będzie generowanie danych według określonych reguł (np. cykliczne odczyty co kilka sekund).

    Moduł logowania i operacji na plikach:
    Klasa Logger odpowiada za zapisywanie odczytów do plików, zarządzanie archiwami i odczyt poprzednich logów.

    Moduł komunikacji sieciowej:
    Implementacja prostego serwera (oraz ewentualnie klienta), który przesyła dane czujników przez sieć. Może to być zastosowane do symulacji scenariusza zdalnego monitoringu.

    Moduł interfejsu graficznego:
    Prosty GUI umożliwiający włączenie/wyłączenie symulacji, podgląd aktualnych danych oraz konfigurację ustawień czujników.

## Jeśli wybierzesz ten projekt powinieneś:

- zrobić forka tego repozytorium na swoim koncie i commitować kolejne postępy,
- rozpocząć od implementacji modułu czujników, do którego wymagania opisane są w pliku sensors.md, wymagania do kolejnych modułów pojawią się na kolejnych laboratoriach.

### Struktura gałęzi

Warto przyjąć prostą strategię gałęzi, która umożliwi łatwe zarządzanie różnymi etapami pracy:

**Główna gałąź (main lub master):**
Zawiera stabilny kod – wersje gotowe do demonstracji lub udostępnienia.

**Gałąź deweloperska (develop):**
Na niej integrowane są wszystkie zmiany przed scalenie ich do głównej gałęzi. Może służyć jako staging area.

Gałęzie funkcjonalności (feature branches):
Każda nowa funkcjonalność lub moduł (np. „feature/symulacja-czujników”, „feature/gui”, „feature/komunikacja-sieciowa”) powinna być rozwijana w osobnej gałęzi. Po zakończeniu prac i przetestowaniu zmian scalamy tę gałąź z develop.

### Przykładowy schemat:

```text
main
 |
 └── develop
       |
       ├── feature/symulacja-czujników
       ├── feature/gui
       ├── feature/logger
       └── feature/komunikacja-sieciowa
```

### Moment commitowania

    Po zakończeniu konkretnego zadania lub funkcjonalności:
    Po implementacji logiki symulacji czujników, stworzeniu klasy obsługującej pliki, zaimplementowaniu GUI, czy dodaniu modułu komunikacji sieciowej warto wykonać commit.

    Przy implementacji małych, ale znaczących kroków:
    Każdy commit powinien reprezentować logicznie spójną zmianę – nie warto łączyć w jednym commicie zmian dotyczących zupełnie różnych obszarów (np. refaktoryzacji kodu plus dodanie nowej funkcjonalności).

    Po przetestowaniu i zaakceptowaniu zmian:
    Jeśli zostały napisane testy jednostkowe, warto zatwierdzić commit już po przejściu testów.

### Zalecenia dotyczące commitów

**Precyzyjne komunikaty:**

Każdy commit powinien mieć jasny i zwięzły komunikat, który opisuje, co zostało zmienione.

**Przykłady:**

    Dodanie klasy Sensor i podstawowej symulacji odczytów

    Implementacja zapisu danych do pliku CSV

    Refaktoryzacja modułu logger – dodanie logowania błędów

    Dodanie testów jednostkowych dla funkcji generujących dane


**Tworzenie tagów**

Tagi służą oznaczeniu istotnych momentów w projekcie, gdy kod osiąga pewien poziom dojrzałości. Tagowanie ważnych wersji projektu - po zakończeniu konkretnego etapu rozwoju, np.:

        v0.1: Po ukończeniu wstępnej wersji symulacji czujników – pełna funkcjonalność symulacji i pierwsze testy.

        v0.2: Po dodaniu operacji na plikach i serializacji konfiguracji.

        v0.3: Po wdrożeniu komunikacji sieciowej.

        v1.0: Stabilna wersja systemu, zawierająca wszystkie wymagane moduły (symulacja, logowanie, GUI, testy, analiza danych).

