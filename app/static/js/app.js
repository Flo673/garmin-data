document.addEventListener("DOMContentLoaded", function () {
    const searchBox = document.getElementById("search");
    if (searchBox) {
        searchBox.addEventListener("input", function () {
            applyFilters();
        });
    }

    // Close dropdown when clicking outside
    document.addEventListener("click", function (e) {
        const dropdown = document.getElementById("category-dropdown");
        if (dropdown && !dropdown.contains(e.target)) {
            dropdown.classList.remove("open");
        }
    });
});

function toggleCategoryDropdown() {
    const dropdown = document.getElementById("category-dropdown");
    dropdown.classList.toggle("open");
}

function applyFilters() {
    const searchBox = document.getElementById("search");
    const query = searchBox ? searchBox.value.toLowerCase() : "";
    const checkboxes = document.querySelectorAll("#category-dropdown-menu input[type=checkbox]");
    const selectedCategories = [];
    checkboxes.forEach(function (cb) {
        if (cb.checked) selectedCategories.push(cb.value);
    });

    // Update button label
    const btn = document.getElementById("category-dropdown-btn");
    const total = checkboxes.length;
    if (selectedCategories.length === total) {
        btn.textContent = "🏷️ Filter";
    } else {
        btn.textContent = "🏷️ " + selectedCategories.length + "/" + total;
    }

    const cards = document.querySelectorAll(".exercise-card");
    cards.forEach(function (card) {
        const name = card.getAttribute("data-name").toLowerCase().replace(/_/g, " ");
        let muscles = [];
        try {
            muscles = JSON.parse(card.getAttribute("data-muscles") || "[]");
        } catch (e) {
            muscles = [];
        }
        // Muscle names are already uppercase with underscores, matching category values
        const normalizedMuscles = muscles;
        const matchesSearch = name.includes(query);
        const matchesCategory = selectedCategories.length === 0 || normalizedMuscles.some(function (m) {
            return selectedCategories.includes(m);
        });

        card.style.display = (matchesSearch && matchesCategory) ? "" : "none";
    });
}