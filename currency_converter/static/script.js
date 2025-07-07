window.addEventListener('DOMContentLoaded', () => {
    const fromSelect = document.getElementById('from_currency');
    const toSelect = document.getElementById('to_currency');
    const rateDisplay = document.getElementById('rateDisplay');

    function fetchRate() {
        const from = fromSelect.value;
        const to = toSelect.value;

        if (from && to && from !== to) {
            fetch(`/rate?from=${from}&to=${to}`)
                .then(response => response.json())
                .then(data => {
                    if (data.rate) {
                        rateDisplay.innerText = `💱 1 ${from} = ${data.rate} ${to}`;
                    } else {
                        rateDisplay.innerText = "❌ Rate not available.";
                    }
                });
        } else {
            rateDisplay.innerText = '';
        }
    }

    fromSelect.addEventListener('change', fetchRate);
    toSelect.addEventListener('change', fetchRate);
});
