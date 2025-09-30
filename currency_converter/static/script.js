document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;

    themeToggle.addEventListener('change', () => {
        body.classList.toggle('dark');
        localStorage.setItem("theme", body.classList.contains('dark') ? "dark" : "light");
    });

    // Load theme
    if (localStorage.getItem("theme") === "dark") {
        body.classList.add('dark');
        themeToggle.checked = true;
    }

    // Live rate preview
    const from = document.getElementById('from_currency');
    const to = document.getElementById('to_currency');
    const rateDisplay = document.getElementById('rateDisplay');

    function updateRate() {
        const f = from.value;
        const t = to.value;
        if (f !== t) {
            fetch(`/rate?from=${f}&to=${t}`)
                .then(res => res.json())
                .then(data => {
                    if (data.rate)
                        rateDisplay.innerText = `💱 1 ${f} = ${data.rate} ${t}`;
                    else
                        rateDisplay.innerText = `❌ Rate not available.`;
                });
        } else {
            rateDisplay.innerText = "";
        }
    }

    from.addEventListener('change', updateRate);
    to.addEventListener('change', updateRate);
});

// Spinner logic
function showSpinner() {
    document.getElementById('spinner').style.display = 'block';
}
