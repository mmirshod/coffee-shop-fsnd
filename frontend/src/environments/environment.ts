export const environment = {
  production: false,
  apiServerUrl: 'https://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-acwjt8y7mhe56bf8.us.auth0.com', // the auth0 domain prefix
    audience: 'drinks', // the audience set for the auth0 app
    clientId: 'x4FSXhHIn6S2ZnZ9lxeT2hFgMmTnOpci', // the client id generated for the auth0 app
    callbackURL: 'https://localhost:8100', // the base url of the running ionic application.
  }
};

// JWT of user with role manager
// eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktQYlk4clktZjJYVXFQUW0xOTlJLSJ9.eyJpc3MiOiJodHRwczovL2Rldi1hY3dqdDh5N21oZTU2YmY4LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwNDQ4MjM5NjExODk1MzY0OTA0MCIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTY4MzIyOTIxNywiZXhwIjoxNjgzMjM2NDE3LCJhenAiOiJ4NEZTWGhISW42UzJablo5bHhlVDJoRmdNbVRuT3BjaSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.WeJ3pm3_KhpoDbDwgWtSItYGUYHPEQtasyGG3c3fes4QFJS84fGcjxU8QBFDOu0H2Q1g9a_bYADro52hTNJm89XnsF0aZGSck_GdasDXxWtVEsC_0ViDBFcSIOMJLWW8rYwy0Zzocup2dt6XdGd2EpsAgwanqND74yFpoGypyH2DXPqzKXx0KneSixnkuqI0E0G6L0k6yNc25a7ZllMWMvXKk_2v2jsA6sm2F2UcT7D_94QvZLci4RXtqWJ7l2Ns4rCeadTYhyBaY9McrXAf4PACltwSa3h5OpycL-XFqsGGai871IMfPscVIoZBvfkbhirpNsVs_MfPjlq12ENHGQ