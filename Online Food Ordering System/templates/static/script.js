
document.addEventListener("DOMContentLoaded", function () {
    // Ask for confirmation before removing an item or placing an order.
    const confirmForms = document.querySelectorAll("[data-confirm]");

    confirmForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const message = form.dataset.confirm;

            if (message && !window.confirm(message)) {
                event.preventDefault();
            }
        });
    });

    // Prevent accidental submission when quantity is invalid.
    const quantityInputs = document.querySelectorAll(
        'input[name="quantity"]'
    );

    quantityInputs.forEach(function (input) {
        input.addEventListener("change", function () {
            const value = Number(input.value);

            if (
                !Number.isInteger(value) ||
                value < Number(input.min) ||
                value > Number(input.max)
            ) {
                input.setCustomValidity(
                    "Enter a valid quantity within the allowed range."
                );
            } else {
                input.setCustomValidity("");
            }
        });
    });

    console.log("Foodie Online Ordering System is ready!");
});
