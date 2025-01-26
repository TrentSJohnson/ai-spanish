import Keycloak from "keycloak-js";

const keycloakConfig = {
    url: import.meta.env.VITE_KEYCLOAK_URL || 'http://localhost:8080',
    realm: import.meta.env.VITE_KEYCLOAK_REALM || 'aispanish',
    clientId: import.meta.env.VITE_KEYCLOAK_CLIENT_ID || 'aispanish'
};

// Create a singleton instance that persists across re-renders
const keycloak = new Keycloak(keycloakConfig);

// Add a flag to track initialization
keycloak._initialized = false;

// Wrap the original init method to prevent multiple initializations
const originalInit = keycloak.init.bind(keycloak);
keycloak.init = async function(...args) {
    if (this._initialized) {
        return Promise.resolve(true);
    }
    this._initialized = true;
    return originalInit(...args);
};

export default keycloak;
