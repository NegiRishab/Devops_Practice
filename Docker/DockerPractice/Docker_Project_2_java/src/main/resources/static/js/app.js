const API = '/api/superheroes';

const form = document.getElementById('hero-form');
const heroList = document.getElementById('hero-list');
const messageEl = document.getElementById('message');

function showMessage(text, type) {
    messageEl.textContent = text;
    messageEl.className = `message ${type}`;
    messageEl.hidden = false;
    setTimeout(() => { messageEl.hidden = true; }, 3000);
}

async function loadHeroes() {
    try {
        const res = await fetch(API);
        const heroes = await res.json();

        if (!heroes.length) {
            heroList.innerHTML = '<li class="empty">No superheroes yet. Add one above!</li>';
            return;
        }

        heroList.innerHTML = heroes.map(h => `
            <li>
                <span class="hero-name">${escapeHtml(h.name)}</span>
                <span class="hero-power">${escapeHtml(h.power)}</span>
            </li>
        `).join('');
    } catch {
        heroList.innerHTML = '<li class="empty">Could not load collection. Is the backend running?</li>';
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value.trim();
    const power = document.getElementById('power').value.trim();

    try {
        const res = await fetch(API, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, power })
        });

        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
            showMessage(data.error || 'Failed to add superhero', 'error');
            return;
        }

        showMessage(`Added ${name} to your collection!`, 'success');
        form.reset();
        loadHeroes();
    } catch {
        showMessage('Network error. Check if the app is running.', 'error');
    }
});

loadHeroes();
