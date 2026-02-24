document.addEventListener('DOMContentLoaded', () => {
    
    // Smooth scroll for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Handle Visitor Form Submission
    const visitorForm = document.getElementById('visitor-form');
    if (visitorForm) {
        visitorForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // In a real scenario, you'd use a service like Formspree or EmailJS here
            alert("Thank you, Abhinand P. S has received your details!");
            visitorForm.reset();
        });
    }

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