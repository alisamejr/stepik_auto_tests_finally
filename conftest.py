from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import pytest


# для корректного отображения кириллицы в параметризаторах
def pytest_make_parametrize_id(config, val):
    return repr(val)


# добавляем параметр запуска тестов в командной строке
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name",
        action="store",
        default="chrome",
        help="Choose browser: chrome or firefox",
    )
    parser.addoption(
        "--language",
        action="store",
        default="en",
        help="Choose language: en, ru, fr, etc.",
    )


# Запуск браузера(для каждой функции) с поддержкой языка
@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")

    browser = None

    if browser_name == "chrome":
        print(f"\nstart Chrome browser for test with language: {user_language}..")
        options = ChromeOptions()
        options.add_experimental_option(
            "prefs", {"intl.accept_languages": user_language}
        )
        browser = webdriver.Chrome(options=options)

    elif browser_name == "firefox":
        print(f"\nstart Firefox browser for test with language: {user_language}..")
        options = FirefoxOptions()
        options.set_preference("intl.accept_languages", user_language)
        browser = webdriver.Firefox(options=options)

    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    # browser.implicitly_wait(5)
    yield browser
    print("\nquit browser..")
    browser.quit()
