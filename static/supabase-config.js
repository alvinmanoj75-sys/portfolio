/**
 * SUPABASE CONFIGURATION FILE
 * ════════════════════════════════════════════════════════════════
 * 
 * INSTRUCTIONS:
 * 1. Go to your Supabase dashboard: https://supabase.com/dashboard
 * 2. Select your project
 * 3. Click on "Settings" > "API"
 * 4. Copy your Project URL and paste it below as SUPABASE_URL
 * 5. Copy your "anon public" API key and paste it below as SUPABASE_ANON_KEY
 * 
 * SECURITY NOTE:
 * - Only use the "anon public" key (not the service role key)
 * - It's safe to expose this key in frontend code
 * - This key only has limited access defined in your Supabase Row Level Security (RLS) policies
 * 
 * ════════════════════════════════════════════════════════════════
 */

// Your Supabase Project URL
// Format: https://your-project-name.supabase.co
const SUPABASE_URL = 'https://mgwocjsbzqztjbwgfytj.supabase.co';

// Your Supabase Anon Public Key
// Format: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1nd29janNienF6dGpid2dmeXRqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIwOTg3MzcsImV4cCI6MjA4NzY3NDczN30.bidQ-wg4BhXZzeAYg0TjPXDwDsS8AFZf4ASBhrNUKOw';

// Export configuration
const supabaseConfig = {
    url: SUPABASE_URL,
    anonKey: SUPABASE_ANON_KEY
};
