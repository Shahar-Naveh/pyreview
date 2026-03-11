/* pyreview - Minimal client-side JavaScript */

// Auto-refresh dashboard every 30 seconds if on dashboard page
if (window.location.pathname === '/') {
    setInterval(() => {
        fetch('/api/reviews?limit=20')
            .then(r => r.json())
            .then(data => {
                // Only reload if there's new data
                const currentRows = document.querySelectorAll('tbody tr').length;
                if (data.length !== currentRows) {
                    window.location.reload();
                }
            })
            .catch(() => {}); // Silent fail
    }, 30000);
}
