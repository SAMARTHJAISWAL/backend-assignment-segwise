const apiBaseURL = "http://127.0.0.1:8000";
const apiKey = "your-secure-secret-key-123456";

let currentPage = 1;

async function loadEvents(archived) {
    const eventsList = document.getElementById("events-list");
    eventsList.innerHTML = "Loading...";

    try {
        const response = await fetch(`${apiBaseURL}/events/?archived=${archived}&page=${currentPage}&limit=5`, {
            headers: {
                "X-API-KEY": apiKey,
                "Accept": "application/json",
            },
        });

        if (response.ok) {
            const events = await response.json();
            eventsList.innerHTML = "";

            events.forEach((event) => {
                const eventItem = document.createElement("div");
                eventItem.innerHTML = `
                    <p><strong>ID:</strong> ${event.id}</p>
                    <p><strong>Details:</strong> ${event.details}</p>
                    <p><strong>Timestamp:</strong> ${event.timestamp}</p>
                    <hr>
                `;
                eventsList.appendChild(eventItem);
            });

            updatePaginationButtons(archived, events.length);
        } else {
            eventsList.innerHTML = "Failed to load events.";
        }
    } catch (error) {
        console.error("Error loading events:", error);
        eventsList.innerHTML = "Error loading events.";
    }
}

function updatePaginationButtons(archived, eventsLength) {
    document.getElementById("prev-btn").disabled = currentPage === 1;
    document.getElementById("next-btn").disabled = eventsLength < 5;

    document.getElementById("prev-btn").onclick = () => {
        if (currentPage > 1) {
            currentPage--;
            loadEvents(archived);
        }
    };

    document.getElementById("next-btn").onclick = () => {
        if (eventsLength === 5) {
            currentPage++;
            loadEvents(archived);
        }
    };
}

document.getElementById("active-events").addEventListener("click", () => {
    currentPage = 1;
    loadEvents(false);
});

document.getElementById("archived-events").addEventListener("click", () => {
    currentPage = 1;
    loadEvents(true);
});
