// Frontend configuration. Edit for your deployment.
// Note: everything in this file is visible to every visitor, so the API key here is
// only a light gate for a demo, not real security. It must match the backend's
// SECRET_API_KEY.
(function () {
    const isLocal = ["localhost", "127.0.0.1", ""].includes(window.location.hostname);
    window.APP_CONFIG = {
        apiBaseURL: isLocal
            ? "http://127.0.0.1:8000"
            : "https://backend-assignment-segwise.onrender.com",
        apiKey: "change-me",
    };
})();
