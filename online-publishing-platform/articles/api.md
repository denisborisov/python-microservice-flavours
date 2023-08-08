# Проектирование API для Articles Microservice

## Определение целей

Это нам позволит создать системный дизайн и оформить endpoint.

<table>
  <tbody>
    <tr>
      <th align="center">№</th>
      <th align="center">Кто пользователи</th>
      <th align="center">Что они могут делать</th>
      <th align="center">Как они это делают</th>
      <th align="center">Входные данные</th>
      <th align="center">Выходные данные</th>
      <th align="center">Цели</th>
    </tr>
    <tr>
      <td align="center">1</td>
      <td align="center">API Gateway</td>
      <td>[C] публикация статьи</td>
      <td>отправить запрос на публикацию</td>
      <td>
        <ul>
            <li>идентификатор пользователя</li>
            <li>содержимое статьи</li>
        </ul>
      </td>
      <td></td>
      <td>публикация статьи</td>
    </tr>
    <tr>
      <td align="center">2</td>
      <td align="center">API Gateway</td>
      <td>[R] получение всех статей</td>
      <td>отправить запрос на получение всех статей</td>
      <td align="center">пагинация</td>
      <td>все статьи</td>
      <td>отображение всех статей</td>
    </tr>
    <tr>
      <td align="center">3</td>
      <td align="center">API Gateway</td>
      <td>[R] получение конкретной статьи</td>
      <td>отправить запрос на получение конкретной статьи</td>
      <td align="center">идентификатор статьи</td>
      <td>конкретная статья</td>
      <td>отображение конкретной статьи</td>
    </tr>
    <tr>
      <td align="center">4</td>
      <td align="center">API Gateway</td>
      <td>[U] изменение конкретной статьи</td>
      <td>отправить запрос на изменение конкретной статьи</td>
      <td>
        <ul>
            <li>идентификатор пользователя</li>
            <li>содержимое статьи</li>
        </ul>
      </td>
      <td></td>
      <td>изменение конкретной статьи</td>
    </tr>
    <tr>
      <td align="center">5</td>
      <td align="center">API Gateway</td>
      <td>[D] удаление статьи</td>
      <td>отправить запрос на удаление</td>
      <td>
        <ul>
            <li>идентификатор пользователя</li>
            <li>идентификатор статьи</li>
        </ul>
      </td>
      <td></td>
      <td>удаление статьи</td>
    </tr>
  </tbody>
</table>
<br />

## Формирование путей на основе ресурсов и представление действий

<table>
  <tbody>
    <tr>
      <th align="center">№</th>
      <th align="center">Действие</th>
      <th align="center">HTTP-метод</th>
      <th align="center">Путь ресурса</th>
      <th align="center">Request</th>
      <th align="center">Response</th>
    </tr>
    <tr>
      <td align="center">1</td>
      <td>получить описание конкретного приложения</td>
      <td align="center">GET</td>
      <td>/api/products/{product_id}</td>
      <td>path parameters</td>
      <td>
        <ul>
          <li>json body</li>
          <li>status code</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td align="center">2</td>
      <td>[C] отправить запрос на установку приложения</td>
      <td align="center">POST</td>
      <td>/api/installations</td>
      <td>json body</td>
      <td>status code</td>
    </tr>
    <tr>
      <td align="center">3</td>
      <td>[R] получить детальную информацию по последним установкам приложения на виртуалки</td>
      <td align="center">GET</td>
      <td>/api/products/{product_id}/users/{user_id}/installations/latest</td>
      <td>path parameters</td>
      <td>
        <ul>
          <li>json body</li>
          <li>status code</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td align="center">4</td>
      <td>[D] отправить запрос на удаление приложения</td>
      <td align="center">DELETE</td>
      <td>/api/installations/{installation_id}</td>
      <td>path parameters</td>
      <td>status code</td>
    </tr>
    <tr>
      <td align="center">5</td>
      <td>получить статус конкретной установки приложения</td>
      <td align="center">GET</td>
      <td>/api/products/{product_id}/installations/{installation_id}/status</td>
      <td>path parameters</td>
      <td>
        <ul>
          <li>json body</li>
          <li>status code</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td align="center">6</td>
      <td>изменить статус конкретной установки приложения</td>
      <td align="center">PATCH</td>
      <td>/api/products/{product_id}/installations/{installation_id}/status</td>
      <td>
        <ul>
          <li>path parameters</li>
          <li>json body</li>
        </ul>
      </td>
      <td>status code</td>
    </tr>
  </tbody>
</table>
<br />

## Описание свойств структуры данных

#### 1.1. Request-данные запроса **GET /api/products/{product_id}**

<table>
  <tbody>
    <tr>
      <th colspan="4">Path Parameters</th>
    </tr>
    <tr>
      <th align="center">Имя</th>
      <th align="center">Тип</th>
      <th align="center">Обязательно</th>
      <th align="center">Описание</th>
    </tr>
    <tr>
      <td>product_id</td>
      <td align="center">int</td>
      <td align="center">yes</td>
      <td>идентификатор приложения</td>
    </tr>
  </tbody>
</table>
<br />

#### 1.2. Response-данные запроса **GET /api/products/{product_id}**

Status Codes:
  * 200 OK
  * 404 Not Found
<br />

<table>
  <tbody>
    <tr>
      <th colspan="4">JSON Body</th>
    </tr>
    <tr>
      <th align="center">Имя</th>
      <th align="center">Тип</th>
      <th align="center">Обязательно</th>
      <th align="center">Описание</th>
    </tr>
    <tr>
      <td>product_id</td>
      <td align="center">int</td>
      <td align="center">yes</td>
      <td>идентификатор приложения</td>
    </tr>
    <tr>
      <td>name</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>имя приложения</td>
    </tr>
    <tr>
      <td>version</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>версия приложения</td>
    </tr>
    <tr>
      <td>picture</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>картинка приложения PNG</td>
    </tr>
    <tr>
      <td>publisher</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>издатель приложения</td>
    </tr>
    <tr>
      <td>description</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>описание приложения</td>
    </tr>
    <tr>
      <td>guide</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>как применить это приложение для решения задач - markdown</td>
    </tr>
    <tr>
      <td>links</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>ссылки на документацию по использованию конкретного приложения</td>
    </tr>
    <tr>
      <td>repository_link</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>ссылка на репозиторий</td>
    </tr>
    <tr>
      <td>support_type</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>вид поддержки приложения</td>
    </tr>
    <tr>
      <td>created</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>дата публикации приложения</td>
    </tr>
  </tbody>
</table>
<br />

#### 2.1. Request-данные запроса **POST /api/installations**

<table>
  <tbody>
    <tr>
      <th colspan="4">JSON Body</th>
    </tr>
    <tr>
      <th align="center">Имя</th>
      <th align="center">Тип</th>
      <th align="center">Обязательно</th>
      <th align="center">Описание</th>
    </tr>
    <tr>
      <td>user_id</td>
      <td align="center">int</td>
      <td align="center">yes</td>
      <td>идентификатор пользователя</td>
    </tr>
    <tr>
      <td>product_id</td>
      <td align="center">int</td>
      <td align="center">yes</td>
      <td>идентификатор приложения</td>
    </tr>
    <tr>
      <td>product_settings</td>
      <td align="center">...</td>
      <td align="center">...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>hostname</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>имя хоста виртуальной машины</td>
    </tr>
  </tbody>
</table>
<br />

#### 2.2. Response-данные запроса **POST /api/installations**

Status Codes:
  * 201 Created
  * 400 Bad Request
<br />

#### 3.1. Request-данные запроса **GET /api/products/{product_id}/users/{user_id}/installations/latest**

<table>
  <tbody>
    <tr>
      <th colspan="4">Path Parameters</th>
    </tr>
    <tr>
      <th align="center">Имя</th>
      <th align="center">Тип</th>
      <th align="center">Обязательно</th>
      <th align="center">Описание</th>
    </tr>
    <tr>
      <td>product_id</td>
      <td align="center">int</td>
      <td align="center">yes</td>
      <td>идентификатор приложения</td>
    </tr>
    <tr>
      <td>user_id</td>
      <td align="center">int</td>
      <td align="center">yes</td>
      <td>идентификатор пользователя</td>
    </tr>
  </tbody>
</table>
<br />

#### 3.2. Response-данные запроса **GET /api/products/{product_id}/users/{user_id}/installations/latest**

Status Codes:
  * 200 OK
  * 404 Not Found
<br />

<table>
  <tbody>
    <tr>
      <th colspan="4">JSON Body</th>
    </tr>
    <tr>
      <th align="center">Имя</th>
      <th align="center">Тип</th>
      <th align="center">Обязательно</th>
      <th align="center">Описание</th>
    </tr>
    <tr>
      <td>installation_id</td>
      <td align="center">int</td>
      <td align="center">yes</td>
      <td>идентификатор установки приложения</td>
    </tr>
    <tr>
      <td>product_id</td>
      <td align="center">int</td>
      <td align="center">yes</td>
      <td>идентификатор приложения</td>
    </tr>
    <tr>
      <td>product_settings</td>
      <td align="center">...</td>
      <td align="center">...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>hostname</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>имя хоста виртуальной машины</td>
    </tr>
    <tr>
      <td>status</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>статус установки приложения</td>
    </tr>
  </tbody>
</table>
<br />

#### 4.1. Request-данные запроса **DELETE /api/installations/{installation_id}**

<table>
  <tbody>
    <tr>
      <th colspan="4">Path Parameters</th>
    </tr>
    <tr>
      <th align="center">Имя</th>
      <th align="center">Тип</th>
      <th align="center">Обязательно</th>
      <th align="center">Описание</th>
    </tr>
    <tr>
      <td>installation_id</td>
      <td align="center">int</td>
      <td align="center">yes</td>
      <td>идентификатор установки приложения</td>
    </tr>
  </tbody>
</table>
<br />

#### 4.2. Response-данные запроса **DELETE /api/installations/{installation_id}**

Status Codes:
  * 202 No Content
  * 404 Not Found
<br />

#### 5.1. Request-данные запроса **GET /api/products/{product_id}/installations/{installation_id}/status**

<table>
  <tbody>
    <tr>
      <th colspan="4">Path Parameters</th>
    </tr>
    <tr>
      <th align="center">Имя</th>
      <th align="center">Тип</th>
      <th align="center">Обязательно</th>
      <th align="center">Описание</th>
    </tr>
    <tr>
      <td>product_id</td>
      <td align="center">int</td>
      <td align="center">yes</td>
      <td>идентификатор приложения</td>
    </tr>
    <tr>
      <td>installation_id</td>
      <td align="center">int</td>
      <td align="center">yes</td>
      <td>идентификатор установки приложения</td>
    </tr>
  </tbody>
</table>
<br />

#### 5.2. Response-данные запроса **GET /api/products/{product_id}/installations/{installation_id}/status**

Status Codes:
  * 200 OK
  * 404 Not Found
<br />

<table>
  <tbody>
    <tr>
      <th colspan="4">JSON Body</th>
    </tr>
    <tr>
      <th align="center">Имя</th>
      <th align="center">Тип</th>
      <th align="center">Обязательно</th>
      <th align="center">Описание</th>
    </tr>
    <tr>
      <td>status</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>статус установки приложения</td>
    </tr>
  </tbody>
</table>
<br />

#### 6.1. Request-данные запроса **PATCH /api/products/{product_id}/installations/{installation_id}/status**

<table>
  <tbody>
    <tr>
      <th colspan="4">Path Parameters</th>
    </tr>
    <tr>
      <th align="center">Имя</th>
      <th align="center">Тип</th>
      <th align="center">Обязательно</th>
      <th align="center">Описание</th>
    </tr>
    <tr>
      <td>product_id</td>
      <td align="center">int</td>
      <td align="center">yes</td>
      <td>идентификатор приложения</td>
    </tr>
    <tr>
      <td>installation_id</td>
      <td align="center">int</td>
      <td align="center">yes</td>
      <td>идентификатор установки приложения</td>
    </tr>
  </tbody>
</table>
<br />

<table>
  <tbody>
    <tr>
      <th colspan="4">JSON Body</th>
    </tr>
    <tr>
      <th align="center">Имя</th>
      <th align="center">Тип</th>
      <th align="center">Обязательно</th>
      <th align="center">Описание</th>
    </tr>
    <tr>
      <td>status</td>
      <td align="center">str</td>
      <td align="center">yes</td>
      <td>статус установки приложения</td>
    </tr>
  </tbody>
</table>
<br />

#### 6.2. Response-данные запроса **PATCH /api/products/{product_id}/installations/{installation_id}/status**

Status Codes:
  * 200 OK
  * 404 Not Found
