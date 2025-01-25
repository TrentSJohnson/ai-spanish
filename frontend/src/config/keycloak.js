import Keycloak from "keycloak-js";

const keycloakConfig = {
    url: import.meta.env.VITE_KEYCLOAK_URL || 'http://localhost:8080',
    realm: import.meta.env.VITE_KEYCLOAK_REALM || 'aispanish',
    clientId: import.meta.env.VITE_KEYCLOAK_CLIENT_ID || 'aispanish-frontend'
};

// Create a singleton instance
let keycloakInstance = null;

const initKeycloak = () => {
    if (!keycloakInstance) {
        keycloakInstance = new Keycloak(keycloakConfig);
    }
    return keycloakInstance;
};

export default initKeycloak();
