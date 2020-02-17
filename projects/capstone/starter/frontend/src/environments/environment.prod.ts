export const environment = {
  production: true,
  apiServerUrl: 'https://smaddali-casting-agency.herokuapp.com', // the running FLASK api server url
  auth0: {
    url: 'smaddcastingagency', // the auth0 domain prefix
    audience: 'casting agency', // the audience set for the auth0 app
    scope: 'openid email profile',
    clientId: 'ElZ8ooFtRdWttDtCMVBNwGsjIHlaMEJz', // the client id generated for the auth0 app
    callbackURL: 'https://smaddali-casting-agency-ui.herokuapp.com/movies', // the base url of the running ionic application.
    logoutURL: 'http://smaddali-casting-agency-ui.herokuapp.com'
  }
};
