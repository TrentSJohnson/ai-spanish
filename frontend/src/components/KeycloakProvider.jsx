import { ReactKeycloakProvider } from '@react-keycloak/web';
import keycloak from '../config/keycloak';

const KeycloakProvider = ({ children }) => {
  const handleOnEvent = (event, error) => {
    console.log('Keycloak event:', event, error);
  };

  const handleTokens = (tokens) => {
    console.log('Token refreshed');
  };

  const loadingComponent = (
    <div>Loading authentication...</div>
  );

  const initOptions = {
    checkLoginIframe: false,
    onLoad: 'check-sso',
    silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html',
    pkceMethod: 'S256',
    enableLogging: true,
    tokenMinValidity: 30
  };

  return (
    <ReactKeycloakProvider
      authClient={keycloak}
      onEvent={handleOnEvent}
      onTokens={handleTokens}
      initOptions={initOptions}
      LoadingComponent={loadingComponent}
      autoRefreshToken={true}
    >
      {children}
    </ReactKeycloakProvider>
  );
};

export default KeycloakProvider;
