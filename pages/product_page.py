from .base_page import BasePage
from .locators import ProductPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import math


class ProductPage(BasePage):
    def add_to_basket(self):
        add_button = self.browser.find_element(
            *ProductPageLocators.ADD_TO_BASKET_BUTTON
        )
        add_button.click()

    def solve_quiz_and_get_code(self):
        try:
            WebDriverWait(self.browser, 10).until(EC.alert_is_present())
            alert = self.browser.switch_to.alert
            x = alert.text.split(" ")[2]
            answer = str(math.log(abs((12 * math.sin(float(x))))))
            alert.send_keys(answer)
            alert.accept()

            try:
                WebDriverWait(self.browser, 3).until(EC.alert_is_present())
                alert = self.browser.switch_to.alert
                alert_text = alert.text
                print(f"Your code: {alert_text}")
                alert.accept()
            except TimeoutException:
                print("No second alert presented")

        except TimeoutException:
            print("No alert presented within 10 seconds")

    def should_be_product_added_to_basket(self):
        assert self.is_element_present(
            *ProductPageLocators.SUCCESS_MESSAGE
        ), "Success message is not presented"

        product_name = self.browser.find_element(*ProductPageLocators.PRODUCT_NAME).text
        message_product_name = self.browser.find_element(
            *ProductPageLocators.MESSAGE_PRODUCT_NAME
        ).text

        assert (
            product_name == message_product_name
        ), f"Product name in message doesn't match. Expected: '{product_name}', got: '{message_product_name}'"

    def should_be_basket_total_equals_product_price(self):
        assert self.is_element_present(
            *ProductPageLocators.BASKET_TOTAL_MESSAGE
        ), "Basket total message is not presented"

        product_price = self.browser.find_element(
            *ProductPageLocators.PRODUCT_PRICE
        ).text
        basket_total = self.browser.find_element(*ProductPageLocators.BASKET_TOTAL).text

        assert (
            product_price == basket_total
        ), f"Basket total doesn't match product price. Expected: '{product_price}', got: '{basket_total}'"

    def should_not_be_success_message(self):
        assert self.is_not_element_present(
            *ProductPageLocators.SUCCESS_MESSAGE
        ), "Success message is presented, but should not be"

    def should_be_success_message_disappeared(self):
        assert self.is_disappeared(
            *ProductPageLocators.SUCCESS_MESSAGE
        ), "Success message is not disappesred, but should bel"
