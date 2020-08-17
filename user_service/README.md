--------
Сервис предоставляет функционал по работе с юзерами приложения. 

--------

## API приложения

- ```/auth/register/ ``` POST - регистрация нового юзера.
    - параметры в body запроса регистрации:
    - ```"username": string (unique) ```
    - ``` "pass": string ```
    
- ```/auth/login/ ``` POST - авторизация юзера.
    - параметры в body запроса регистрации:
    - ```"username": string ```
    - ``` "pass": string ```
    
- ```/auth/refreshtokens ``` POST - обновить токены
    - параметры запроса регистрации:
    - header запроса - *refresh token*: ```"Authorization": string```
    - body запроса - *access token*: ``` "access": string ```
- ```/auth/user/info ``` POST - получить полную информацию по юзеру. 
    - для данного запроса параметры не задаются
    - *нужна авторизация*
- ```/auth/logout ``` GET - логаут юзера
    - параметры запроса регистрации:
    - header запроса - *refresh token*: ```"Authorization": string```
    - *нужна авторизация*
