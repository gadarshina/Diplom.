import allure
import pytest
from pages.main_page import MainPage

@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
class TestBookSearch:

    @allure.title("Поиск книги по заголовку")
    @allure.description("Тест проверяет возможность поиска книги по заголовку 'капитанская'.")
    def test_by_name(self, driver):
        main_page = MainPage(driver)
        main_page.search_book("капитанская")
        assert "Показываем результаты по запросу «капитанская», найдено:" in main_page.get_search_results_text()

    @allure.title("Проверка наличия результатов поиска")
    @allure.description("Проверяет, что результаты поиска не пустые для запроса 'капитанская'.")
    def test_search_results_not_empty(self, driver):
        main_page = MainPage(driver)
        main_page.search_book("капитанская")
        results_text = main_page.get_search_results_text()
        assert "ничего не найдено" not in results_text
        assert len(main_page.get_search_results_items()) > 0

    @allure.title("Проверка корректности заголовка результатов")
    @allure.description("Проверяет, что заголовок результатов содержит искомый запрос.")
    def test_results_header_contains_query(self, driver):
        main_page = MainPage(driver)
        query = "капитанская"
        main_page.search_book(query)
        header_text = main_page.get_search_results_header()
        assert query.lower() in header_text.lower()

    @allure.title("Проверка наличия конкретной книги в результатах")
    @allure.description("Проверяет, что в результатах поиска есть книга с названием 'Капитанская дочка'.")
    def test_specific_book_in_results(self, driver):
        main_page = MainPage(driver)
        main_page.search_book("капитанская")
        results = main_page.get_search_results_items()
        titles = [item.get_title() for item in results]
        assert any("Капитанская дочка" in title for title in titles)

    @allure.title("Проверка поиска по частичному совпадению")
    @allure.description("Проверяет, что поиск по частичному названию 'капит' возвращает релевантные результаты.")
    def test_partial_match_search(self, driver):
        main_page = MainPage(driver)
        main_page.search_book("капит")
        results_text = main_page.get_search_results_text()
        assert "ничего не найдено" not in results_text
        results = main_page.get_search_results_items()
        assert len(results) > 0
        for item in results:
            assert "капит" in item.get_title().lower()


@allure.epic("UI Тестирование")
@allure.feature("Поиск книжной информации")
class TestBookSearchNegative:

    def test_search_in_foreign_language(self, driver):
        main_page = MainPage(driver)
        main_page.search_book("こんにちは")
        result_text = main_page.get_search_results_text()
        print(f"Результат поиска: {repr(result_text)}")  # для отладки
        # Проверка, что результат содержит сообщение о отсутствии результатов
        assert "не принёс результатов" in result_text

    def test_search_nonexistent_book(self, driver):
        main_page = MainPage(driver)
        nonexistent_title = "Книга_которой_нет_в_базе_123456"
        main_page.search_book(nonexistent_title)
        result_text = main_page.get_search_results_text()
        print(f"Результат поиска: {repr(result_text)}")  # для отладки

        # Проверка, что сообщение содержит слова о отсутствии результатов
        assert ("не принёс результатов" in result_text.lower()) or ("ничего не найдено" in result_text.lower())

