document.addEventListener("DOMContentLoaded", function () {
    // Handling IMEI form submission
    document.getElementById("imeiForm").addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission

        let imeiInput = document.getElementById("imei");
        let statusSelect = document.getElementById("status");
        let messageBox = document.getElementById("messageBox");

        let imei = imeiInput.value.trim();
        let status = statusSelect.value;

        if (!imei) {
            messageBox.innerHTML = "<p style='color: red;'>IMEI cannot be empty!</p>";
            return;
        }

        try {
            let response = await fetch("/add_imei", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ imei, status })
            });

            let result = await response.json();
            if (response.ok) {
                messageBox.innerHTML = `<p style="color: green;">${result.message}</p>`;
                imeiInput.value = ""; // Clear input field
            } else {
                messageBox.innerHTML = `<p style="color: red;">${result.error}</p>`;
            }
        } catch (error) {
            messageBox.innerHTML = `<p style="color: red;">Error: Unable to process request.</p>`;
        }
    });

    // Dark mode toggle functionality
    const toggleDarkMode = () => {
        const body = document.body;
        const isDarkMode = body.classList.contains("dark-mode");

        // Toggle dark mode class
        if (isDarkMode) {
            body.classList.remove("dark-mode");
            // Remove dark mode from elements like inputs and selects
            document.querySelectorAll("input, select").forEach(input => input.classList.remove("dark-mode"));
        } else {
            body.classList.add("dark-mode");
            // Apply dark mode to inputs and selects as well
            document.querySelectorAll("input, select").forEach(input => input.classList.add("dark-mode"));
        }

        // Store user preference in localStorage
        localStorage.setItem("darkMode", body.classList.contains("dark-mode"));
    };

    // Check for saved dark mode preference
    const savedDarkMode = localStorage.getItem("darkMode");
    if (savedDarkMode === "true") {
        document.body.classList.add("dark-mode");
        document.querySelectorAll("input, select").forEach(input => input.classList.add("dark-mode"));
    }

    // Set up the dark mode toggle event
    const darkModeButton = document.getElementById("darkModeToggle");
    if (darkModeButton) {
        darkModeButton.addEventListener("click", toggleDarkMode);
    }
});
