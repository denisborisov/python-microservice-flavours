# Development of Articles Microservice API

## Goals

<table>
  <tbody>
    <tr>
      <th align="center">№</th>
      <th align="center">User</th>
      <th align="center">Action</th>
      <th align="center">Input</th>
      <th align="center">Output</th>
    </tr>
    <tr>
      <td align="center">1</td>
      <td align="center">GTWMS</td>
      <td>[C] create an article</td>
      <td align="center">article data</td>
      <td></td>
    </tr>
    <tr>
      <td align="center">2</td>
      <td align="center">GTWMS</td>
      <td>[R] retrieve an article</td>
      <td align="center">article id</td>
      <td>article data</td>
    </tr>
    <tr>
      <td align="center">3</td>
      <td align="center">GTWMS</td>
      <td>[U] update an article</td>
      <td align="center">
        <ul>
          <li>article id</li>
          <li>article data</li>
        </ul>
      </td>
      <td></td>
    </tr>
    <tr>
      <td align="center">4</td>
      <td align="center">GTWMS</td>
      <td>[D] delete an article</td>
      <td align="center">article id</td>
      <td></td>
    </tr>
    <tr>
      <td align="center">5</td>
      <td align="center">GTWMS</td>
      <td>retrieve all articles</td>
      <td align="center"></td>
      <td>list of articles:
        <ul>
          <li>article id</li>
          <li>article preview</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>
<br />

## URI Design

<table>
  <tbody>
    <tr>
      <th align="center">№</th>
      <th align="center">Action</th>
      <th align="center">HTTP Method</th>
      <th align="center">URI</th>
      <th align="center">Request</th>
      <th align="center">Response</th>
    </tr>
    <tr>
      <td align="center">1</td>
      <td>[C] create an article</td>
      <td align="center">POST</td>
      <td>/api/articles</td>
      <td>json body</td>
      <td>status code</td>
    </tr>
    <tr>
      <td align="center">2</td>
      <td>[R] retrieve an article</td>
      <td align="center">GET</td>
      <td>/api/articles/{article_id}</td>
      <td>path parameters</td>
      <td>
        <ul>
          <li>json body</li>
          <li>status code</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td align="center">3</td>
      <td>[U] update an article</td>
      <td align="center">PATCH</td>
      <td>/api/articles/{article_id}</td>
      <td>
        <ul>
          <li>path parameters</li>
          <li>json body</li>
        </ul>
      </td>
      <td>status code</td>
    </tr>
    <tr>
      <td align="center">4</td>
      <td>[D] delete an article</td>
      <td align="center">DELETE</td>
      <td>/api/articles/{article_id}</td>
      <td>path parameters</td>
      <td>status code</td>
    </tr>
    <tr>
      <td align="center">5</td>
      <td>retrieve all articles</td>
      <td align="center">GET</td>
      <td>/api/articles</td>
      <td>query parameters</td>
      <td>
        <ul>
          <li>json body</li>
          <li>status code</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>
<br />

## Requests and Responses

#### 1.1. Request data of POST /api/articles

<table>
  <tbody>
    <tr>
      <th colspan="4">JSON Body</th>
    </tr>
    <tr>
      <th align="center">Name</th>
      <th align="center">Type</th>
      <th align="center">Required</th>
      <th align="center">Description</th>
    </tr>
    <tr>
      <td>title</td>
      <td align="center">string</td>
      <td align="center">true</td>
      <td>article title</td>
    </tr>
    <tr>
      <td>preview</td>
      <td align="center">string</td>
      <td align="center">true</td>
      <td>article preview</td>
    </tr>
    <tr>
      <td>body</td>
      <td align="center">string</td>
      <td align="center">true</td>
      <td>article body</td>
    </tr>
    <tr>
      <td>created_by</td>
      <td align="center">int</td>
      <td align="center">true</td>
      <td>user id</td>
    </tr>
  </tbody>
</table>
<br />

#### 1.2. Response data of POST /api/articles

Status Codes:

- 201 Created
- 400 Bad Request
  <br />

#### 2.1. Request data of GET /api/articles/{article_id}

<table>
  <tbody>
    <tr>
      <th colspan="4">Path Parameters</th>
    </tr>
    <tr>
      <th align="center">Name</th>
      <th align="center">Type</th>
      <th align="center">Required</th>
      <th align="center">Description</th>
    </tr>
    <tr>
      <td>article_id</td>
      <td align="center">int</td>
      <td align="center">true</td>
      <td>article id</td>
    </tr>
  </tbody>
</table>
<br />

#### 2.2. Response data of GET /api/articles/{article_id}

Status Codes:

- 200 OK
- 404 Not Found
  <br />

<table>
  <tbody>
    <tr>
      <th colspan="4">JSON Body</th>
    </tr>
    <tr>
      <th align="center">Name</th>
      <th align="center">Type</th>
      <th align="center">Required</th>
      <th align="center">Description</th>
    </tr>
    <tr>
      <td>article_id</td>
      <td align="center">int</td>
      <td align="center">true</td>
      <td>article id</td>
    </tr>
    <tr>
      <td>title</td>
      <td align="center">string</td>
      <td align="center">true</td>
      <td>article title</td>
    </tr>
    <tr>
      <td>preview</td>
      <td align="center">string</td>
      <td align="center">true</td>
      <td>article preview</td>
    </tr>
    <tr>
      <td>body</td>
      <td align="center">string</td>
      <td align="center">true</td>
      <td>article body</td>
    </tr>
    <tr>
      <td>created_by</td>
      <td align="center">int</td>
      <td align="center">true</td>
      <td>user id</td>
    </tr>
  </tbody>
</table>
<br />

#### 3.1. Request data of PATCH /api/articles/{article_id}

<table>
  <tbody>
    <tr>
      <th colspan="4">Path Parameters</th>
    </tr>
    <tr>
      <th align="center">Name</th>
      <th align="center">Type</th>
      <th align="center">Required</th>
      <th align="center">Description</th>
    </tr>
    <tr>
      <td>article_id</td>
      <td align="center">int</td>
      <td align="center">true</td>
      <td>article id</td>
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
      <th align="center">Name</th>
      <th align="center">Type</th>
      <th align="center">Required</th>
      <th align="center">Description</th>
    </tr>
    <tr>
      <td>title</td>
      <td align="center">string</td>
      <td align="center">false</td>
      <td>article title</td>
    </tr>
    <tr>
      <td>preview</td>
      <td align="center">string</td>
      <td align="center">false</td>
      <td>article preview</td>
    </tr>
    <tr>
      <td>body</td>
      <td align="center">string</td>
      <td align="center">false</td>
      <td>article body</td>
    </tr>
  </tbody>
</table>
<br />

#### 3.2. Response data of PATCH /api/articles/{article_id}

Status Codes:

- 200 OK
- 404 Not Found
  <br />

#### 4.1. Request data of DELETE /api/articles/{article_id}

<table>
  <tbody>
    <tr>
      <th colspan="4">Path Parameters</th>
    </tr>
    <tr>
      <th align="center">Name</th>
      <th align="center">Type</th>
      <th align="center">Required</th>
      <th align="center">Description</th>
    </tr>
    <tr>
      <td>article_id</td>
      <td align="center">int</td>
      <td align="center">true</td>
      <td>article id</td>
    </tr>
  </tbody>
</table>
<br />

#### 4.2. Response data of DELETE /api/articles/{article_id}

Status Codes:

- 204 No Content
- 404 Not Found
  <br />

#### 5.1. Request data of GET /api/articles

<table>
  <tbody>
    <tr>
      <th colspan="4">Query Parameters</th>
    </tr>
    <tr>
      <th align="center">Name</th>
      <th align="center">Type</th>
      <th align="center">Required</th>
      <th align="center">Description</th>
    </tr>
    <tr>
      <td>user_id</td>
      <td align="center">int</td>
      <td align="center">false</td>
      <td>user id</td>
    </tr>
  </tbody>
</table>
<br />

#### 5.2. Response data of GET /api/articles

Status Codes:

- 200 OK
- 404 Not Found
  <br />

<table>
  <tbody>
    <tr>
      <th colspan="4">JSON Body</th>
    </tr>
    <tr>
      <th align="center">Name</th>
      <th align="center">Type</th>
      <th align="center">Required</th>
      <th align="center">Description</th>
    </tr>
    <tr>
      <td>article_id</td>
      <td align="center">int</td>
      <td align="center">true</td>
      <td>article id</td>
    </tr>
    <tr>
      <td>title</td>
      <td align="center">string</td>
      <td align="center">true</td>
      <td>article title</td>
    </tr>
    <tr>
      <td>preview</td>
      <td align="center">string</td>
      <td align="center">true</td>
      <td>article preview</td>
    </tr>
    <tr>
      <td>created_by</td>
      <td align="center">int</td>
      <td align="center">true</td>
      <td>user id</td>
    </tr>
  </tbody>
</table>
<br />
