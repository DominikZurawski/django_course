from selenium.common.exceptions import TimeoutException
from django.shortcuts import render, redirect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests

from .models import KRSCompany


def scrape(request):
    if request.method == "POST":
        phrase = request.POST.get("query")  # Fraza do wyszukania
        # Typ podmiotu: 'przedsiebiorca' lub 'stowarzyszenie'
        entity_type = request.POST.get("search_type")

        # Uruchomienie scrapowania
        scrape_krs_logic(phrase, entity_type)

        # Pobieranie danych z bazy
        data = KRSCompany.objects.all()

        return render(request, "myapp/result.html", {"data": data})

    return render(request, "myapp/result.html")


# def scrape_krs_logic(phrase, entity_type):
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(options=options)

#     try:
#         driver.get("https://wyszukiwarka-krs.ms.gov.pl/")

#         # Wybór typu podmiotu
#         if entity_type == "przedsiebiorca":
#             checkbox_label = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Przedsiębiorcy')]"))
#             )
#             checkbox_label.click()  # Kliknij na label, aby zaznaczyć checkbox
#         else:
#             checkbox_label = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Stowarzyszenia')]"))
#             )
#             checkbox_label.click()  # Kliknij na label, aby zaznaczyć checkbox

#         # Wyszukiwanie pola 'Nazwa' po tekście etykiety
#         search_box = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Nazwa')]/following-sibling::div//input"))
#         )
#         search_box.send_keys(phrase)  # Wysyłamy frazę

#         # Naciśnięcie Tab 12 razy po wpisaniu frazy
#         body = driver.find_element(By.TAG_NAME, "body")
#         for _ in range(12):  # 12 razy Tab
#             body.send_keys(Keys.TAB)

#         actions = ActionChains(driver)
#         actions.send_keys(Keys.ENTER).perform()  # Naciśnięcie Enter
#         time.sleep(10)  # Czekamy na wyniki

#         # Iterowanie po stronach wyników
#         krs_data = []  # Lista do przechowywania wyników
#         last_page_content = None
#         while True:
#             results = driver.find_elements(By.XPATH, '//tr[contains(@class, "table-row")]')

#             if not results:  # Jeśli brak wyników na stronie, kończymy
#                 print("Brak wyników na stronie.")
#                 break

#             # Przechowujemy zawartość strony, aby sprawdzić, czy się zmieniła
#             page_content = [result.text for result in results]

#             for result in results:
#                 try:
#                     krs_number = result.find_element(By.XPATH, ".//td[1]//a").text
#                     name = result.find_element(By.XPATH, ".//td[2]").text
#                     krs_data.append((krs_number, name))

#                     # Zapisanie danych do bazy
#                     KRSCompany.objects.get_or_create(
#                         krs_number=krs_number,
#                         defaults={'name': name}
#                     )
#                     print(f"Zapisano: {name} ({krs_number})")  # Potwierdzenie zapisu

#                 except Exception as e:
#                     print(f"Błąd przy ekstrakcji danych: {e}")

#             # Sprawdzamy, czy zawartość strony zmieniła się po kliknięciu "następnej strony"
#             if page_content == last_page_content:
#                 print("Brak zmiany wyników, zakończenie.")
#                 break  # Jeśli zawartość strony się nie zmieniła, kończymy

#             last_page_content = page_content  # Zaktualizowanie zawartości strony

#             # Czekamy, aż przycisk "następna strona" będzie widoczny i klikalny
#             try:
#                 next_page_button = WebDriverWait(driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'p-paginator-next')]"))
#                 )

#                 # Sprawdzamy, czy przycisk nie jest wyłączony (np. brak kolejnej strony)
#                 if 'ng-disabled' not in next_page_button.get_attribute('class'):
#                     next_page_button.click()  # Klikamy na przycisk następnej strony
#                     time.sleep(5)  # Czekamy na załadowanie wyników
#                 else:
#                     print("Brak przycisku 'następna strona', kończymy.")
#                     break  # Jeśli nie ma kolejnej strony, kończymy
#             except TimeoutException:
#                 print("Czas oczekiwania na przycisk 'następna strona' minął.")
#                 break  # Jeśli czas oczekiwania minął, kończymy

#         # Po zakończeniu zbierania wyników, możemy zwrócić dane
#         print(f"Zebrano {len(krs_data)} wyników.")
#         return krs_data

#     except Exception as e:
#         print(f"Błąd: {e}")
#     finally:
#         driver.quit()


def scrape_krs_basic(phrase, entity_type):
    driver.get("https://wyszukiwarka-krs.ms.gov.pl/")

    # Wybór typu podmiotu
    if entity_type == "przedsiebiorca":
        checkbox_label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), 'Przedsiębiorcy')]"))
        )
        checkbox_label.click()  # Kliknij na label, aby zaznaczyć checkbox
    else:
        checkbox_label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), 'Stowarzyszenia')]"))
        )
        checkbox_label.click()  # Kliknij na label, aby zaznaczyć checkbox

    # Wyszukiwanie pola 'Nazwa' po tekście etykiety
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//label[contains(text(), 'Nazwa')]/following-sibling::div//input"))
    )
    search_box.send_keys(phrase)  # Wysyłamy frazę


def scrape_krs_confirm():
    body = driver.find_element(By.TAG_NAME, "body")

    while True:
        # Klikamy TAB
        body.send_keys(Keys.TAB)
        # time.sleep(0.2)  # Krótkie opóźnienie, aby strona miała czas na reakcję

        # Sprawdzamy aktywny element
        active_element = driver.switch_to.active_element

        try:
            # Wypisujemy szczegóły aktywnego elementu
            tag_name = active_element.tag_name
            element_id = active_element.get_attribute('id')
            classes = active_element.get_attribute('class')
            text = active_element.text.strip()

            # Przerwij, jeśli to jest przycisk 'Wyszukaj'
            if "Wyszukaj" in text:
                print("Znaleziono przycisk 'Wyszukaj'!")
                break  # Zatrzymujemy pętlę, jeśli trafiliśmy na 'Wyszukaj'

        except Exception as e:
            print("Błąd podczas sprawdzania aktywnego elementu:", e)
            pass  # W razie błędów, przejdź do kolejnego elementu

    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER).perform()  # Naciśnięcie Enter
    time.sleep(10)  # Czekamy na wyniki

    # Sprawdzamy, czy są wyniki
    try:
        result_text = driver.find_element(By.XPATH, "//ds-panel-header[contains(text(), 'Wyniki wyszukiwania')]").text
        if "Wyniki wyszukiwania" in result_text:
            # Odczytujemy liczbę wyników
            result_count = int(result_text.split(" - ")[1])
            if result_count > 100:
                print(f"Znaleziono {result_count} to więcej niż 100 wyników. Zawężam wyszukiwanie.")
                return False
            else:
                print(f"Znaleziono {result_count}. Przechodzimy do szczegółów.")
                return True
        else:
            print("Nie znaleziono żadnych wyników.")
            return False
    except Exception as e:
        return False

def scrape_krs():
    krs_data = []  # Lista do przechowywania wyników
    last_page_content = None
    while True:
        results = driver.find_elements(
            By.XPATH, '//tr[contains(@class, "table-row")]')

        if not results:  # Jeśli brak wyników na stronie, kończymy
            print("Brak wyników na stronie.")
            break

        # Przechowujemy zawartość strony, aby sprawdzić, czy się zmieniła
        page_content = [result.text for result in results]

        for result in results:
            try:
                krs_number = result.find_element(By.XPATH, ".//td[1]//a").text
                name = result.find_element(By.XPATH, ".//td[2]").text
                krs_data.append((krs_number, name))

                ## W tym miejscu zapytanie do API
                # Zapytanie do API
                api_url = f"https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/{krs_number}?rejestr={short_entity_type}&format=json"
                response = requests.get(api_url)

                if response.status_code == 200:
                    data = response.json()

                    # Wyciąganie danych z odpowiedzi API
                    nip = data["odpis"]["dane"]["dzial1"]["danePodmiotu"]["identyfikatory"].get("nip", None)
                    regon = data["odpis"]["dane"]["dzial1"]["danePodmiotu"]["identyfikatory"].get("regon", None)
                    legal_form = data["odpis"]["dane"]["dzial1"]["danePodmiotu"]["formaPrawna"]

                    # Adres
                    city = data["odpis"]["dane"]["dzial1"]["siedzibaIAdres"].get("siedziba", {}).get("miejscowosc", None)
                    street_address = data["odpis"]["dane"]["dzial1"]["siedzibaIAdres"]["adres"].get("ulica", "") + " " + data["odpis"]["dane"]["dzial1"]["siedzibaIAdres"]["adres"].get("nrDomu", "")
                    postal_code = data["odpis"]["dane"]["dzial1"]["siedzibaIAdres"]["adres"].get("kodPocztowy", None)

                    # Email i strona
                    website = data["odpis"]["dane"]["dzial1"]["siedzibaIAdres"].get("adresStronyInternetowej", None)
                    email = data["odpis"]["dane"]["dzial1"]["siedzibaIAdres"].get("adresPocztyElektronicznej", None)

                else:
                    print(f"Błąd API dla {krs_number}: {response.status_code}")

                # Zapisanie danych do bazy
                KRSCompany.objects.get_or_create(
                    krs_number=krs_number,
                    defaults={
                        'name': name,
                        'nip': nip,
                        'regon': regon,
                        'legal_form': legal_form,
                        'city': city,
                        'street_address': street_address,
                        'postal_code': postal_code,
                        'website': website,
                        'email': email
                    }
                )
                # Potwierdzenie zapisu
                print(f"Zapisano: {name} ({krs_number})")

            except Exception as e:
                print(f"Błąd przy ekstrakcji danych: {e}")

        # Sprawdzamy, czy zawartość strony zmieniła się po kliknięciu "następnej strony"
        if page_content == last_page_content:
            print("Brak zmiany wyników, zakończenie.")
            break  # Jeśli zawartość strony się nie zmieniła, kończymy

        last_page_content = page_content  # Zaktualizowanie zawartości strony

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # Czekamy, aż przycisk "następna strona" będzie widoczny i klikalny
        try:
            next_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'p-paginator-next')]"))
            )

            # Sprawdzamy, czy przycisk nie jest wyłączony (np. brak kolejnej strony)
            if 'ng-disabled' not in next_page_button.get_attribute('class'):
                next_page_button.click()  # Klikamy na przycisk następnej strony
                time.sleep(2)  # Czekamy na załadowanie wyników
            else:
                print("Brak przycisku 'następna strona', kończymy.")
                break  # Jeśli nie ma kolejnej strony, kończymy
        except TimeoutException:
            print("Czas oczekiwania na przycisk 'następna strona' minął.")
            break  # Jeśli czas oczekiwania minął, kończymy

    # Po zakończeniu zbierania wyników, możemy zwrócić dane
    print(f"Zebrano {len(krs_data)} wyników.")
    return krs_data

def krs_details(ind):

    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.TAB * 2)
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER).perform()

    print(f"Przechodzę do województwa {ind}.")
    actions.send_keys(Keys.DOWN * ind).perform()
    actions.send_keys(Keys.ENTER).perform()

def krs_details_state(inx):

    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.TAB * 3)
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER).perform()

    print(f"Przechodzę do powiatu {inx}.")
    actions.send_keys(Keys.DOWN * inx).perform()
    actions.send_keys(Keys.ENTER).perform()

def scrape_krs_logic(phrase, entity_type):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Tryb bez interfejsu
    global driver
    driver = webdriver.Chrome(options=options)
    global short_entity_type
    if entity_type == "przedsiebiorca":
        short_entity_type = "P"
    else:
        short_entity_type = "S"

    try:
        scrape_krs_basic(phrase, entity_type)

        if scrape_krs_confirm():
            scrape_krs()
        else:
            # index = 0
            powiat_count_dict = {
                "DOLNOŚLĄSKIE": 30,
                "KUJAWSKO-POMORSKIE": 21,
                "LUBELSKIE": 24,
                "LUBUSKIE": 14,
                "ŁÓDZKIE": 24,
                "MAŁOPOLSKIE": 22,
                "MAZOWIECKIE": 42,
                "OPOLSKIE": 12,
                "PODKARPACKIE": 26,
                "PODLASKIE": 17,
                "POMORSKIE": 22,
                "ŚLĄSKIE": 19,
                "ŚWIĘTOKRZYSKIE": 14,
                "WARMIŃSKO-MAZURSKIE": 21,
                "WIELKOPOLSKIE": 35,
                "ZACHODNIOPOMORSKIE": 16
            }

            for index, (wojewodztwo, liczba_powiatow) in enumerate(powiat_count_dict.items()):
                driver.quit()
                driver = webdriver.Chrome(options=options)
                scrape_krs_basic(phrase, entity_type)
                krs_details(index + 1)

                if scrape_krs_confirm():
                    scrape_krs()
                else:
                    for i in range(liczba_powiatow):
                        driver.quit()
                        driver = webdriver.Chrome(options=options)
                        scrape_krs_basic(phrase, entity_type)
                        krs_details(index + 1)
                        krs_details_state(i+1)

                        if scrape_krs_confirm():
                            scrape_krs()

        # Po zakończeniu zbierania wyników, możemy zwrócić dane
        print("Zbieranie zakończone.")
    except Exception as e:
        print(f"Błąd: {e}")
    finally:
        driver.quit()





# def scrape_krs_logic(phrase, entity_type):
#     options = webdriver.ChromeOptions()
#     # options.add_argument("--headless")  # Tryb bez interfejsu
#     driver = webdriver.Chrome(options=options)

#     try:
#         driver.get("https://wyszukiwarka-krs.ms.gov.pl/")

#         # Wybór typu podmiotu
#         if entity_type == "przedsiebiorca":
#             checkbox_label = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Przedsiębiorcy')]"))
#             )
#             checkbox_label.click()  # Kliknij na label, aby zaznaczyć checkbox
#         else:
#             checkbox_label = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Stowarzyszenia')]"))
#             )
#             checkbox_label.click()  # Kliknij na label, aby zaznaczyć checkbox

#         # Wyszukiwanie pola 'Nazwa' po tekście etykiety
#         try:
#             search_box = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Nazwa')]/following-sibling::div//input"))
#             )
#             search_box.send_keys(phrase)  # Wysyłamy frazę

#             # Naciśnięcie Tab 12 razy po wpisaniu frazy
#             body = driver.find_element(By.TAG_NAME, "body")
#             for _ in range(12):  # 12 razy Tab
#                 body.send_keys(Keys.TAB)

#             actions = ActionChains(driver)
#             actions.send_keys(Keys.ENTER).perform()  # Naciśnięcie Enter
#             time.sleep(10)  # Czekamy na wyniki
#         except Exception as e:
#             print("Błąd podczas czekania na element 'Nazwa':", e)
#         body.send_keys(Keys.ENTER)

#         # Sprawdzamy, czy pojawiły się wyniki
#         try:
#             results = WebDriverWait(driver, 10).until(
#                 EC.presence_of_all_elements_located((By.XPATH, '//tr[contains(@class, "table-row")]'))
#             )
#             if not results:
#                 print("Brak wyników wyszukiwania!")
#             else:
#                 print(f"Znaleziono {len(results)} wyników.")
#         except Exception as e:
#             print("Błąd podczas sprawdzania wyników:", e)

#         # Iterowanie po stronach wyników
#         while True:
#             results = driver.find_elements(By.XPATH, '//tr[contains(@class, "table-row")]')

#             for result in results:
#                 try:
#                     krs_number = result.find_element(By.XPATH, ".//td[1]//a").text
#                     name = result.find_element(By.XPATH, ".//td[2]").text
#                     krs_link_element = result.find_element(By.XPATH, ".//td[1]//a")

#                     # Kliknięcie w link
#                     actions = ActionChains(driver)
#                     actions.move_to_element(krs_link_element).click().perform()
#                     print(f"Kliknięto na link KRS: {krs_number}")

#                     time.sleep(2)  # Czekaj na załadowanie strony szczegółów

#                     # Pobieranie szczegółów na stronie
#                     try:
#                         krs_number_details = WebDriverWait(driver, 10).until(
#                             EC.presence_of_element_located((By.XPATH, "//div[text()='Numer KRS']/following-sibling::div"))
#                         ).text
#                         nip = driver.find_element(By.XPATH, "//div[text()='NIP']/following-sibling::div").text
#                         regon = driver.find_element(By.XPATH, "//div[text()='REGON']/following-sibling::div").text
#                         legal_form = driver.find_element(By.XPATH, "//div[text()='Forma prawna']/following-sibling::div").text
#                         city = driver.find_element(By.XPATH, "//div[text()='Miejscowość']/following-sibling::div").text
#                         street_address = driver.find_element(By.XPATH, "//div[text()='Adres']/following-sibling::div").text
#                         postal_code = driver.find_element(By.XPATH, "//div[text()='Kod pocztowy']/following-sibling::div").text
#                         website = driver.find_element(By.XPATH, "//div[text()='Adres WWW']/following-sibling::div").text
#                         email = driver.find_element(By.XPATH, "//div[text()='E-mail']/following-sibling::div").text

#                         KRSCompany.objects.update_or_create(
#                             krs_number=krs_number_details,
#                             defaults={
#                                 "name": name,
#                                 "nip": nip,
#                                 "regon": regon,
#                                 "legal_form": legal_form,
#                                 "city": city,
#                                 "street_address": street_address,
#                                 "postal_code": postal_code,
#                                 "website": website if website != '-' else None,
#                                 "email": email if email != '-' else None,
#                             }
#                         )
#                     except Exception as e:
#                         print(f"Błąd przy pobieraniu szczegółów: {e}")

#                     driver.back()
#                     time.sleep(3)

#                 except Exception as e:
#                     print(f"Błąd przy kliknięciu na link KRS: {e}")

#             # Sprawdź, czy są kolejne strony wyników
#             try:
#                 next_button = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, "//button[@class='p-paginator-next']"))
#                 )
#                 if 'ng-disabled' not in next_button.get_attribute("class"):
#                     next_button.click()
#                     time.sleep(2)  # Poczekaj na załadowanie kolejnej strony
#                 else:
#                     print("Brak kolejnej strony")
#                     break
#             except Exception as e:
#                 print(f"Nie ma kolejnych stron: {e}")
#                 break

#     finally:
#         driver.quit()

def clear(request):
    # Funkcja czyszcząca wszystkie dane z bazy
    KRSCompany.objects.all().delete()
    return redirect('/')
