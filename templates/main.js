document.addEventListener('DOMContentLoaded', function () {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const htmlElement = document.documentElement;

    // Set initial theme based on localStorage or system preference
    if (localStorage.getItem('theme') === 'dark') {
        htmlElement.setAttribute('data-bs-theme', 'dark');
        darkModeToggle.checked = true;
    }

    darkModeToggle.addEventListener('change', function () {
        if (this.checked) {
            htmlElement.setAttribute('data-bs-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            htmlElement.setAttribute('data-bs-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });
});