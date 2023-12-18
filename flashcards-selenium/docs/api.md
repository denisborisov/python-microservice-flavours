# Development of Flashcards Microservice API

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
      <td>[R] retrieve a flashcard</td>
      <td align="center">word</td>
      <td>flashcard data</td>
    </tr>
    <tr>
      <td align="center">2</td>
      <td align="center">GTWMS</td>
      <td>[R] retrieve the list of flashcards stored in the DB</td>
      <td align="center">optional: word (partial match)</td>
      <td>list of flashcards:
        <ul>
          <li>required: word</li>
          <li>optional: definitions</li>
          <li>optional: synonyms</li>
          <li>optional: translations</li>
          <li>optional: examples</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td align="center">3</td>
      <td align="center">GTWMS</td>
      <td>[D] delete a flashcard</td>
      <td align="center">word</td>
      <td></td>
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
      <td>[R] retrieve a flashcard</td>
      <td align="center">GET</td>
      <td>/api/flashcards/{word}</td>
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
      <td>[R] retrieve the list of flashcards stored in the DB</td>
      <td align="center">GET</td>
      <td>/api/flashcards</td>
      <td>query parameters</td>
      <td>
        <ul>
          <li>json body</li>
          <li>status code</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td align="center">3</td>
      <td>[D] delete a flashcard</td>
      <td align="center">DELETE</td>
      <td>/api/flashcards/{word}</td>
      <td>path parameters</td>
      <td>status code</td>
    </tr>
  </tbody>
</table>
<br />

## Requests and Responses

#### 1.1. Request data of GET /api/flashcards/{word}

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
      <td>word</td>
      <td align="center">string</td>
      <td align="center">true</td>
      <td>word to be translated</td>
    </tr>
  </tbody>
</table>
<br />

#### 1.2. Response data of GET /api/flashcards/{word}

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
      <td>word</td>
      <td align="center">string</td>
      <td align="center">true</td>
      <td>word to be translated</td>
    </tr>
    <tr>
      <td>definitions</td>
      <td align="center">list of strings</td>
      <td align="center">true</td>
      <td>list of definitions of the given word</td>
    </tr>
    <tr>
      <td>synonyms</td>
      <td align="center">list of strings</td>
      <td align="center">true</td>
      <td>list of synonyms of the given word</td>
    </tr>
    <tr>
      <td>translations</td>
      <td align="center">list of strings</td>
      <td align="center">true</td>
      <td>list of translations of the given word</td>
    </tr>
    <tr>
      <td>examples</td>
      <td align="center">list of strings</td>
      <td align="center">true</td>
      <td>list of usage examples of the given word</td>
    </tr>
  </tbody>
</table>
<br />

#### 2.1. Request data of GET /api/flashcards

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
      <td>word</td>
      <td align="center">string</td>
      <td align="center">false</td>
      <td>patrial match of word used for filtering</td>
    </tr>
    <tr>
      <td>with_definitions</td>
      <td align="center">boolean</td>
      <td align="center">false</td>
      <td>true if we need to show definitions</td>
    </tr>
    <tr>
      <td>with_synonyms</td>
      <td align="center">boolean</td>
      <td align="center">false</td>
      <td>true if we need to show synonyms</td>
    </tr>
    <tr>
      <td>with_translations</td>
      <td align="center">boolean</td>
      <td align="center">false</td>
      <td>true if we need to show translations</td>
    </tr>
    <tr>
      <td>with_examples</td>
      <td align="center">boolean</td>
      <td align="center">false</td>
      <td>true if we need to show examples</td>
    </tr>
  </tbody>
</table>
<br />

#### 2.2. Response data of GET /api/flashcards

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
      <td>word</td>
      <td align="center">string</td>
      <td align="center">true</td>
      <td>word to be translated</td>
    </tr>
    <tr>
      <td>definitions</td>
      <td align="center">list of strings</td>
      <td align="center">true</td>
      <td>list of definitions of the given word</td>
    </tr>
    <tr>
      <td>synonyms</td>
      <td align="center">list of strings</td>
      <td align="center">true</td>
      <td>list of synonyms of the given word</td>
    </tr>
    <tr>
      <td>translations</td>
      <td align="center">list of strings</td>
      <td align="center">true</td>
      <td>list of translations of the given word</td>
    </tr>
    <tr>
      <td>examples</td>
      <td align="center">list of strings</td>
      <td align="center">true</td>
      <td>list of usage examples of the given word</td>
    </tr>
  </tbody>
</table>
<br />

#### 3.1. Request data of DELETE /api/flashcards/{word}

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
      <td>word</td>
      <td align="center">string</td>
      <td align="center">true</td>
      <td>word to be deleted from the database</td>
    </tr>
  </tbody>
</table>
<br />

#### 3.2. Response data of DELETE /api/flashcards/{flashcard_id}

Status Codes:

- 204 No Content
- 404 Not Found
  <br />
