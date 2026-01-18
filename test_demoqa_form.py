from selene import browser, have, be
import os

def test_student_registration_form():
    # 1. Открываем нужную страницу
    browser.open('/automation-practice-form')
    
    # Убираем рекламу и футер, которые могут перекрывать кнопки (частая проблема на DemoQA)
    browser.execute_script('document.querySelector("#fixedban").remove()')
    browser.execute_script('document.querySelector("footer").remove()')

    # 2. Заполняем простые текстовые поля
    browser.element('#firstName').type('Ivan')
    browser.element('#lastName').type('Ivanov')
    browser.element('#userEmail').type('ivanov@example.com')
    
    # Выбираем пол (кликаем по тексту в лейбле, так как сам чекбокс часто скрыт)
    browser.all('[name=gender]').element_by(have.value('Male')).element('..').click()
    
    browser.element('#userNumber').type('8005553535')

    # 3. Работаем с календарем (симулируем действия пользователя)
    browser.element('#dateOfBirthInput').click()
    browser.element('.react-datepicker__month-select').send_keys('May')
    browser.element('.react-datepicker__year-select').send_keys('1995')
    # Выбираем число (используем класс, чтобы не попасть в соседний месяц)
    browser.element('.react-datepicker__day--015:not(.react-datepicker__day--outside-month)').click()

    # 4. Выбираем хобби и предметы
    browser.element('#subjectsInput').type('Computer Science').press_enter()
    # Кликаем по тексту лейбла для хобби
    browser.all('.custom-checkbox').element_by(have.exact_text('Sports')).click()

    # 5. Загрузка файла (используем относительный путь, если файл лежит рядом, 
    # но тут просто укажем путь к любому изображению в системе или пропустим, если файла нет)
    # browser.element('#uploadPicture').send_keys(os.path.abspath('image.png'))

    # 6. Адрес и выпадающие списки (State и City)
    browser.element('#currentAddress').type('Moscow, Red Square 1')
    
    # Прокручиваем до конца, чтобы кнопка Submit была видна
    browser.element('#submit').perform(command.js.scroll_into_view)
    
    browser.element('#state').click()
    browser.all('[id^=react-select-3-option]').element_by(have.exact_text('NCR')).click()
    
    browser.element('#city').click()
    browser.all('[id^=react-select-4-option]').element_by(have.exact_text('Delhi')).click()

    # 7. Отправка формы
    browser.element('#submit').press_enter()

    # 8. ПРОВЕРКА данных в поп-апе
    # Проверяем, что модальное окно появилось
    browser.element('.modal-content').should(be.visible)
    
    # Проверяем таблицу с данными (используем селектор таблицы и проверяем строки)
    browser.element('.table').all('td').even.should(
        have.exact_texts(
            'Ivan Ivanov',
            'ivanov@example.com',
            'Male',
            '8005553535',
            '15 May,1995',
            'Computer Science',
            'Sports',
            '',  # Тут будет имя файла, если загружала
            'Moscow, Red Square 1',
            'NCR Delhi'
        )
    )
