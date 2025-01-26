document.addEventListener("DOMContentLoaded", () => {
    const apiBaseURL = "http://127.0.0.1:8000";
    const apiKey = "your-secure-secret-key-123456";

    let currentPage = 1;

    // Create a new trigger
    async function createTrigger() {
        const triggerName = document.getElementById("trigger-name").value;
        const triggerType = document.getElementById("trigger-type").value; // Dynamic trigger type
        const payload = document.getElementById("trigger-payload").value || null;
        const scheduleTime = document.getElementById("schedule-time").value || null;

        if (!triggerName) {
            alert("Please provide a trigger name.");
            return;
        }

        if (triggerType === "scheduled" && !scheduleTime) {
            alert("Scheduled triggers require a schedule time.");
            return;
        }

        try {
            const response = await fetch(`${apiBaseURL}/triggers/`, {
                method: "POST",
                headers: {
                    "X-API-KEY": apiKey,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name: triggerName,
                    type: triggerType,
                    payload: payload,
                    schedule_time: scheduleTime,
                }),
            });

            if (response.ok) {
                alert("Trigger created successfully!");
                fetchTriggers(); // Reload triggers
            } else {
                const error = await response.json();
                console.error("Error creating trigger:", error);
                alert(`Failed to create trigger: ${error.detail || response.statusText}`);
            }
        } catch (error) {
            console.error("Network error:", error);
            alert("Failed to create trigger due to a network error.");
        }
    }

    // Load events (archived or recent)
    async function loadEvents(archived) {
        const eventsList = document.getElementById("event-logs");
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
                    const eventRow = document.createElement("tr");
                    eventRow.innerHTML = `
                        <td>${event.id}</td>
                        <td>${event.timestamp}</td>
                        <td>${event.details}</td>
                    `;
                    eventsList.appendChild(eventRow);
                });

                updatePaginationButtons(events.length);
            } else {
                const error = await response.json();
                console.error("Error loading events:", error);
                eventsList.innerHTML = "Failed to load events.";
            }
        } catch (error) {
            console.error("Network error:", error);
            eventsList.innerHTML = "Failed to load events.";
        }
    }

    // Fetch and display triggers
    async function fetchTriggers() {
        const triggersList = document.getElementById("triggers-list");
        triggersList.innerHTML = "Loading triggers...";

        try {
            const response = await fetch(`${apiBaseURL}/triggers/`, {
                method: "GET",
                headers: {
                    "X-API-KEY": apiKey,
                    "Accept": "application/json",
                },
            });

            if (response.ok) {
                const triggers = await response.json();
                triggersList.innerHTML = "";

                triggers.forEach((trigger) => {
                    const triggerRow = document.createElement("tr");
                    triggerRow.innerHTML = `
                        <td>${trigger.id}</td>
                        <td>${trigger.name}</td>
                        <td>${trigger.type}</td>
                        <td>${trigger.schedule_time || "N/A"}</td>
                        <td>${trigger.payload || "N/A"}</td>
                        <td>${trigger.is_active ? "Yes" : "No"}</td>
                    `;
                    triggersList.appendChild(triggerRow);
                });
            } else {
                const error = await response.json();
                console.error("Error fetching triggers:", error);
                triggersList.innerHTML = "Failed to load triggers.";
            }
        } catch (error) {
            console.error("Network error:", error);
            triggersList.innerHTML = "Error loading triggers.";
        }
    }

    // Update pagination buttons
    function updatePaginationButtons(totalEvents) {
        const prevButton = document.getElementById("prev-button");
        const nextButton = document.getElementById("next-button");

        prevButton.disabled = currentPage === 1;
        nextButton.disabled = totalEvents < 5;

        prevButton.onclick = () => {
            if (currentPage > 1) {
                currentPage--;
                loadEvents(false);
            }
        };

        nextButton.onclick = () => {
            currentPage++;
            loadEvents(false);
        };
    }

    // Attach event listeners
    document.getElementById("create-trigger-btn").addEventListener("click", createTrigger);
    document.getElementById("recent-events-btn").addEventListener("click", () => loadEvents(false));
    document.getElementById("archived-events-btn").addEventListener("click", () => loadEvents(true));

    // Initial load of triggers and recent events
    fetchTriggers();
    loadEvents(false);
});
