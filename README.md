<h4>Небольшой обзор приложения "Py Social", созданного в целях практики использования Postgre SQL, Tkinter и Tortoise ORM</h4>
<p>Приложение представляет собой небольшой мессенджер, в котором можно добавлять друзей, отправлять сообщения и редактировать свой профиль.</p>

<h4>Строки из файла «config» необходимо заменить на свои значения.</h4>

![capture_250130_204201](https://github.com/user-attachments/assets/60087c2e-2069-4576-bf1b-20303e8bf34d)

<h4>Для начала запустим приложение, выбрав необходимую конфигурацию</h4>

![Снимок экрана 2025-01-30 204302](https://github.com/user-attachments/assets/9c92b3f8-ced4-4808-a870-e3d1690300f4)

<h4>Открывается окно, с выбором регистрации или авторизации</h4>

![Снимок экрана 2025-01-30 204317](https://github.com/user-attachments/assets/7b1000bb-cd0f-4a28-a276-d5ee4968fb34)

<h4>Пойдём по пути нового пользователя</h4>

![Снимок экрана 2025-01-30 204327](https://github.com/user-attachments/assets/ce7cc70c-5615-4eb7-9945-3116d354d23c)

<h4>Нажимаем "регистрацию"</h4>

![Снимок экрана 2025-01-30 204414](https://github.com/user-attachments/assets/02aab5eb-054f-4e64-91f1-cb490fbbc4f7)

<h4>Ошибка!</h4>

![Снимок экрана 2025-01-30 204421](https://github.com/user-attachments/assets/08ab976d-03af-42da-bb36-ae8d081a4e8f)


<h4>Редактируем данные и пробуем снова</h4>

![Снимок экрана 2025-01-30 204441](https://github.com/user-attachments/assets/d5ac7009-3917-49ac-a0a3-47065dbb34bb)


<h4>Опять ошибка</h4>

![Снимок экрана 2025-01-30 204449](https://github.com/user-attachments/assets/81aa06d9-e915-4888-a6c5-c0008d681fca)

<h4>Возможно теперь получится</h4>

![Снимок экрана 2025-01-30 204501](https://github.com/user-attachments/assets/e66249bf-6273-4202-839a-5b4c9293d478)

<h4>Точно! Попадаем на страницу своего профиля</h4>

![Снимок экрана 2025-01-30 204512](https://github.com/user-attachments/assets/18beb52a-dc26-4473-811f-dea0c2ed1d2e)

<h4>Сразу сменим фото, чтобы подчеркнуть индивидуальность</h4>

![Снимок экрана 2025-01-30 204518](https://github.com/user-attachments/assets/069846bc-3c28-4cfa-a0b9-f9916941b789)

<h4>Кра-со-та</h4>

![Снимок экрана 2025-01-30 204603](https://github.com/user-attachments/assets/469ebb4d-0d94-4385-8485-ff0947fc5eb6)

<h4>Заглянем на главную</h4>

![Снимок экрана 2025-01-30 204616](https://github.com/user-attachments/assets/1b176b89-3f46-48f6-aad5-263162921f01)

<h4>Можно выбрать город для отображения погоды в текущем регионе (пока городов не очень много, но планируется расширить их список и сделать его более автоматизированным)</h4>

![capture_250130_204648](https://github.com/user-attachments/assets/561c880e-86fe-42bf-b919-8123dad5632b)

<h4>"Да"</h4>

![Снимок экрана 2025-01-30 204701](https://github.com/user-attachments/assets/2b879933-f0a9-43ec-a21c-ddaee7ac31da)

<h4>Получаем некоторые данные по погоде в Обнинске</h4>

![Снимок экрана 2025-01-30 204714](https://github.com/user-attachments/assets/627accb4-860f-455a-8329-87719c564fbb)

<h4>За погоду отвечает функция "weather_check", которая обращается к сайту "openweathermap.org"</h4>

![Снимок экрана 2025-01-30 204742](https://github.com/user-attachments/assets/0809e012-8ace-4d25-954b-307601aba65d)

<h4>Вернёмся на "главную" и перейдём в "мессенджер". Здесь уже автоматически создался диалог с самим собой, для заметок</h4>

![Снимок экрана 2025-01-30 204802](https://github.com/user-attachments/assets/f74446df-c91f-4536-854e-baf139abecbf)

<h4>Откроем "заметки"</h4>

![Снимок экрана 2025-01-30 204811](https://github.com/user-attachments/assets/3ca03d7c-8b81-4679-a547-8df6a84c71d5)

<h4>Пробуем отправить сообщение</h4>

![Снимок экрана 2025-01-30 204821](https://github.com/user-attachments/assets/b502121c-2332-4021-8764-9aeeff3f4d2b)
<br>--- --- ---<br>
![Снимок экрана 2025-01-30 204828](https://github.com/user-attachments/assets/fd939c83-93b1-4f41-a0d0-d933b2e1dddf)


<h4>А теперь прикрепим фотографию</h4>

![Снимок экрана 2025-01-30 204917](https://github.com/user-attachments/assets/bdee76fd-94b6-4274-b678-bbd034c8ea5e)
<br>--- --- ---<br>
![Снимок экрана 2025-01-30 204929](https://github.com/user-attachments/assets/b9cae4fd-f288-459d-ba9f-3d13a4f1a731)
<br>--- --- ---<br>
![Снимок экрана 2025-01-30 204948](https://github.com/user-attachments/assets/4874c2eb-5c71-4d0e-9695-f43d5a11ebf1)

<h4>Вернёмся на "главную" и перейдём в раздел "друзья". Тут можно найти пользователя по его email</h4>

![Снимок экрана 2025-01-30 204959](https://github.com/user-attachments/assets/e901efb6-55f1-4d6c-8fdc-0ba2a2d76f25)

<h4>Так как пока в базе данных только 1 пользователь, воспользуемся функциями из модуля "user_crud" для добавления ещё нескольких</h4>

![Снимок экрана 2025-01-30 205013](https://github.com/user-attachments/assets/d8c75503-e4c1-4bb9-b63c-8c06463b6e5a)
<br>--- --- ---<br>
![Снимок экрана 2025-01-30 205049](https://github.com/user-attachments/assets/9ebc717f-fb19-4cad-a70e-42d515379860)

<h4>Проверяем БД: записи появились</h4>

![Снимок экрана 2025-01-30 205140](https://github.com/user-attachments/assets/387398c4-9f42-49f3-8610-7704ee1b8663)

<h4>Возвращаемся в само приложение, в раздел "друзья". Пробуем добавить друга по email</h4>

![Снимок экрана 2025-01-30 205216](https://github.com/user-attachments/assets/dbcdb07d-fd9a-44bb-9bcc-a2efe2beb9ed)

<h4>Если нет полной уверенности в том, что этот тот пользователь, который нам нужен, то можем нажать "нет", чтобы перед отправкой запроса посмотреть его профиль</h4>

![Снимок экрана 2025-01-30 205222](https://github.com/user-attachments/assets/d2c8d50a-53e0-4f78-a059-ce8ceabedc2b)
<br>--- --- ---<br>
![Снимок экрана 2025-01-30 205231](https://github.com/user-attachments/assets/8b144f38-3780-473f-a61b-ac9e35009e14)

<h4>По нажатию на "да", открывается найденный профиль</h4>

![Снимок экрана 2025-01-30 205240](https://github.com/user-attachments/assets/8c557f5f-8a43-4f0b-ab75-40816a125e93)

<h4>Отсюда также можно отправить запрос на добавление в друзья. Тепрь заявка ожидает принятия</h4>

![Снимок экрана 2025-01-30 205248](https://github.com/user-attachments/assets/642766f9-54f8-4d69-bab4-fb6578a17e5c)

<h4>Есть возможность отозвать запрос</h4>

![Снимок экрана 2025-01-30 205308](https://github.com/user-attachments/assets/81766cef-8248-429b-88c6-daee7b1b3e71)

<h4>И снова его отправить, конечно же</h4>

![Снимок экрана 2025-01-30 205351](https://github.com/user-attachments/assets/5c9e7e30-bfab-4361-a745-df948d4cc4b9)
<br>--- --- ---<br>
![Снимок экрана 2025-01-30 205400](https://github.com/user-attachments/assets/491ed2bc-7d9e-4f5d-9d32-112d5d49a512)

<h4>Возвращаемся в раздел "друзья". Здесь появился выпадающий список пользователей, в нём содержаться значения, котрые ожидают подтверждения, а также подтверждённые друзья</h4>

![capture_250130_205456](https://github.com/user-attachments/assets/11a6b897-e402-4182-addf-63c96358f4aa)

<h4>По нажатию на email переходим на соответствующий профиль</h4>

![Снимок экрана 2025-01-30 205507](https://github.com/user-attachments/assets/eda718ba-c5b4-4e45-8fd3-371c7d0ed7df)

<h4>Посмотрим в БД. Пока что пользователь, которому мы отправили заявку на добавление не подтвердил её, испрвим это с помощью всё того же модуля "user_crud"</h4>

![Снимок экрана 2025-01-30 205550](https://github.com/user-attachments/assets/0114b046-2f66-427c-8a14-6c3b7b588dc9)
<br>--- --- ---<br>
![Снимок экрана 2025-01-30 205647](https://github.com/user-attachments/assets/5e4c4875-6c9f-4c17-b697-53f9aa15cafc)

<h4>Теперь "дружба" подтверждена</h4>

![Снимок экрана 2025-01-30 205816](https://github.com/user-attachments/assets/8d981de4-61c7-4620-bbe8-17cb53396d7b)

<h4>Вернёмся в приложение, увидим, что для "подтверждённого" друга появилась кнопка отправки сообщения</h4>

![Снимок экрана 2025-01-30 205844](https://github.com/user-attachments/assets/dc53d438-8005-4603-a302-00fc43878562)

<h4>Отправим что-нибудь</h4>

![Снимок экрана 2025-01-30 205852](https://github.com/user-attachments/assets/ad435d71-636d-489c-8055-b05da457d161)
<br>--- --- ---<br>
![Снимок экрана 2025-01-30 205902](https://github.com/user-attachments/assets/89b7a90f-5df9-42f3-89bb-d1b1bee6055f)
<br>--- --- ---<br>
![Снимок экрана 2025-01-30 205910](https://github.com/user-attachments/assets/f641106d-205d-437b-8aa4-945091ec7053)

<h4>Посмотрим в БД. Появился новый диалог. Всё работает</h4>

![Снимок экрана 2025-01-30 205930](https://github.com/user-attachments/assets/4e7e3d79-c36d-4e0f-9b32-f0f9a7e779a7)


<p>Планируется добавление новых функций, таких как отображения количества друзей на странице профиля, возможность удалять и редактировать сообщения, а также улучшение интерфейса и другое расширение функциональности.</p>
