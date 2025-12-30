from .base_page import BasePage
from .locators import BasketPageLocators


class BasketPage(BasePage):
    def should_be_basket_page(self):
        """Проверка, что мы на странице корзины"""
        self.should_be_basket_url()
        self.should_be_basket_content()

    def should_be_basket_url(self):
        """Проверка URL корзины"""
        assert "basket" in self.browser.current_url, "Not a basket page"

    def should_be_basket_content(self):
        """Проверка наличия контента корзины"""
        assert self.is_element_present(
            *BasketPageLocators.BASKET_CONTENT
        ), "Basket content is not presented"

    def should_be_empty_basket(self):
        """Полная проверка пустой корзины"""
        self.should_not_be_basket_items()
        self.should_be_empty_basket_message()

    def should_not_be_basket_items(self):
        """Отрицательная проверка: товаров в корзине нет"""
        assert self.is_not_element_present(
            *BasketPageLocators.BASKET_ITEMS
        ), "Basket items are presented, but should not be"

    def should_be_empty_basket_message(self):
        """Проверка сообщения о пустой корзине"""
        assert self.is_element_present(
            *BasketPageLocators.EMPTY_BASKET_MESSAGE
        ), "Empty basket message is not presented"
        # Дополнительная проверка текста сообщения
        message = self.browser.find_element(
            *BasketPageLocators.EMPTY_BASKET_MESSAGE
        ).text
        # Проверка на разных языках
        assert (
            "empty" in message.lower() or "пуста" in message.lower()
        ), f"Expected empty basket message, but got: {message}"
