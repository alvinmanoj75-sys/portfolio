// ════════════════════════════════════════════════════════════════
// SUPABASE CLIENT INITIALIZATION
// ════════════════════════════════════════════════════════════════

let supabaseClient = null;

function initializeSupabase() {
    if (!supabaseConfig || !supabaseConfig.url || !supabaseConfig.anonKey) {
        console.error('❌ Supabase credentials not configured. Please add them to supabase-config.js');
        return false;
    }
    
    try {
        supabaseClient = supabase.createClient(
            supabaseConfig.url,
            supabaseConfig.anonKey
        );
        console.log('✅ Supabase initialized successfully');
        return true;
    } catch (error) {
        console.error('❌ Failed to initialize Supabase:', error);
        return false;
    }
}

// ════════════════════════════════════════════════════════════════
// FORM SUBMISSION
// ════════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Supabase
    initializeSupabase();
    
    const form = document.getElementById('visitor-form');
    if (!form) {
        console.error("Form not found! Check id='visitor-form' in HTML");
        return;
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log("Form submit clicked!");

        const name = form.querySelector('input[name="name"]').value.trim();
        const email = form.querySelector('input[name="email"]').value.trim();
        const message = form.querySelector('textarea[name="message"]').value.trim();

        if (!name || !email || !message) {
            alert("Please fill all fields");
            return;
        }

        // Disable submit button to prevent duplicate submissions
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Submitting...';

        try {
            if (!supabaseClient) {
                throw new Error('Supabase client not initialized. Please configure your credentials.');
            }

            // Insert data into Supabase messages table
            const { data, error } = await supabaseClient
                .from('messages')
                .insert([
                    {
                        name: name,
                        email: email,
                        message: message
                    }
                ]);

            if (error) {
                console.error('Supabase insert error:', error);
                throw new Error(error.message || 'Failed to save inquiry');
            }

            console.log('✅ Inquiry saved successfully:', data);
            alert(`Thank you, ${name}! Your inquiry has been received and saved.`);
            form.reset();

        } catch (err) {
            console.error("Error:", err);
            alert("Error: " + (err.message || "Failed to submit form. Please try again."));
        } finally {
            // Re-enable submit button
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Details';
        }
    });

    // ════════════════════════════════════════════════════════════════
    // SCROLL REVEAL ANIMATION
    // ════════════════════════════════════════════════════════════════
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

