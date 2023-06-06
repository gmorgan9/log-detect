async function getUserModePreference() {
    try {
        const response = await fetch('https://ld-api.morganserver.com/api/data');
        const data = await response.json();
        return data.mode;
    } catch (error) {
        console.error('Error fetching user mode preference:', error);
        // Return a default mode value or handle the error as needed
        return 1; // Default to dark mode
    }
}

// Function to set the theme based on the user's mode preference
async function setTheme() {
    var mode = await getUserModePreference();
    var theme = mode === 1 ? "light" : "dark";
    document.documentElement.setAttribute("data-bs-theme", theme);
}

// Call the setTheme function when the page loads
window.onload = setTheme;