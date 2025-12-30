import pytest
from .pages.product_page import ProductPage
from .pages.basket_page import BasketPage
import time


@pytest.mark.parametrize(
    "link",
    [
        "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer0",
        "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer1",
        "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer2",
        "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer3",
        "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer4",
        "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer5",
        "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer6",
        pytest.param(
            "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer7",
            marks=pytest.mark.xfail(reason="Bug found on this affer"),
        ),
        "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer8",
        "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer9",
    ],
)
def test_guest_can_add_product_to_basket(browser, link):
    page = ProductPage(browser, link)
    page.open()
    page.add_to_basket()

    time.sleep(2)

    try:
        page.solve_quiz_and_get_code()
    except Exception as e:
        print(f"Error solving quiz: {e}")
        time.sleep(3)
        page.solve_quiz_and_get_code()

    time.sleep(2)

    page.should_be_product_added_to_basket()
    page.should_be_basket_total_equals_product_price()


def test_guest_can_add_shellcoders_handbook_to_basket(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/the-shellcoders-handbook_209/?promo=newYear"
    page = ProductPage(browser, link)
    page.open()
    page.add_to_basket()
    page.solve_quiz_and_get_code()
    page.should_be_product_added_to_basket()
    page.should_be_basket_total_equals_product_price()


def test_guest_shoild_see_login_link_on_product_page(browser):
    link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
    page = ProductPage(browser, link)
    page.open()
    page.should_be_login_link()


def test_guest_can_go_to_login_page_from_product_page(browser):
    link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
    page = ProductPage(browser, link)
    page.open()
    page.go_to_login_page()
    page.should_be_login_link()


# ИСПРАВЛЕНО: Реализован тест для проверки пустой корзины со страницы товара
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    link = (
        "http://selenium1py.pythonanywhere.com/catalogue/the-shellcoders-handbook_209/"
    )
    page = ProductPage(browser, link)
    page.open()

    # Переходим в корзину
    page.go_to_basket_page()

    # Создаем объект страницы корзины и выполняем проверки
    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_be_basket_page()
    basket_page.should_be_empty_basket()
