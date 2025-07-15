

document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll('.reply-btn');
    const forms = document.querySelectorAll('.reply-form');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const id = button.getAttribute('data-id');
            forms.forEach(form => {
                if (form.getAttribute('data-parent') === id) {
                    form.classList.toggle('hidden');
                }
            });
        });
    });
});
