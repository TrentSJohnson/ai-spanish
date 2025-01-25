import { ReactKeycloakProvider } from '@react-keycloak/web';
import keycloak from '../config/keycloak';

const KeycloakProvider = ({ children }) => {
  const handleOnEvent = (event, error) => {
    console.log('Keycloak event:', event, error);
  };

  const loadingComponent = (
    <div>Loading authentication...</div>
  );

  return (
    <ReactKeycloakProvider
      authClient={keycloak}
      onEvent={handleOnEvent}
      LoadingComponent={loadingComponent}
    >
      {children}
    </ReactKeycloakProvider>
  );
};

export default KeycloakProvider;
