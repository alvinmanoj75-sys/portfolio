document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('visitor-form');
    if (!form) {
        console.error("Form not found! Check id='visitor-form' in HTML");
        return;
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log("Form submit clicked!");

        const name = form.querySelector('input[type="text"]').value.trim();
        const email = form.querySelector('input[type="email"]').value.trim();
        const message = form.querySelector('textarea').value.trim();

        if (!name || !email || !message) {
            alert("Please fill all fields");
            return;
        }

        try {
            const response = await fetch('/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, message })
            });

            const data = await response.json();
            console.log("Server response:", data);

            if (data.success) {
                alert(data.message || "Thank you! Your inquiry is saved.");
                form.reset();
            } else {
                alert("Error: " + (data.message || "Unknown error"));
            }
        } catch (err) {
            console.error("Fetch error:", err);
            alert("Network error - check console for details");
        }
    });

    // Scroll Reveal Animation Logic
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.card').forEach(el => {
        el.style.opacity = "0";
        el.style.transform = "translateY(20px)";
        el.style.transition = "all 0.6s ease-out";
        observer.observe(el);
    });
});
