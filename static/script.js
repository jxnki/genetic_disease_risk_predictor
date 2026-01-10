/* static/script.js */

const thalData = {
    male: { affected: false },
    female: { affected: false }
};

function switchTab(type) {
    document.querySelectorAll('.form-section').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById(type + '-form').classList.add('active');
    event.currentTarget.classList.add('active');
    document.getElementById('results').style.display = 'none';
}

function toggleDisease(side, isAffected, btn) {
    thalData[side].affected = isAffected;
    
    // UI Updates
    const parent = btn.parentElement;
    parent.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    
    // Toggle tree visibility
    const tree = document.getElementById(side + '-tree');
    if (tree) {
        if (isAffected) {
            tree.classList.add('hidden');
        } else {
            tree.classList.remove('hidden');
        }
    }
}

function toggleNode(el) {
    el.classList.toggle('selected');
}

async function runThalassemia() {
    const btn = document.querySelector('#thalassemia-form .calc-btn');
    const originalText = btn.innerText;
    btn.innerText = "Calculating...";
    
    // Logic to determine history 'score'
    let historyVal = "none";
    if (thalData.male.affected && thalData.female.affected) {
        historyVal = "both_parents";
    } else if (thalData.male.affected || thalData.female.affected) {
        historyVal = "one_parent";
    } else {
        // Check grandparents
        const gps = document.querySelectorAll('.tree-container .node.selected').length;
        if (gps >= 2) historyVal = "both_parents"; 
        else if (gps > 0) historyVal = "one_parent";
    }

    const payload = {
        mother_population: document.getElementById('t_female_pop').value,
        father_population: document.getElementById('t_male_pop').value,
        relation: document.getElementById('t_relation').value,
        history: historyVal
    };
    
    try {
        const res = await fetch('/calculate_thalassemia', {
            method: 'POST', 
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        const img = document.getElementById("riskPlot");
        img.src = "data:image/png;base64," + data.plot;
        // Use responsive CSS classes instead of fixed pixel sizes
        img.classList.remove('plot-large');
        img.classList.add('plot-small');
        img.style.display = 'block';
        // Hide the bar chart area (we only want the circular plot)
        const bars = document.getElementById('bars-container');
        if (bars) { bars.innerHTML = ''; bars.style.display = 'none'; }
        document.getElementById('results').style.display = 'block';
    } catch (err) {
        console.error(err);
        alert("Error connecting to backend");
    }
    
    btn.innerText = originalText;
}

async function runHemophilia() {
    const btn = document.querySelector('#hemophilia-form .calc-btn');
    const originalText = btn.innerText;
    btn.innerText = "Calculating...";

    const payload = {
        mother_carrier: document.getElementById('h_carrier').value,
        mother_history: document.getElementById('h_history').value,
        mother_population: document.getElementById('h_pop').value,
        father_affected: document.getElementById('h_father').value
    };

    try {
        const res = await fetch('/calculate_hemophilia', {
            method: 'POST', 
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        const img = document.getElementById("riskPlot");
        img.src = "data:image/png;base64," + data.plot;
        // Use responsive CSS classes instead of fixed pixel sizes
        img.classList.remove('plot-small');
        img.classList.add('plot-large');
        img.style.display = 'block';
        const bars = document.getElementById('bars-container');
        if (bars) { bars.innerHTML = ''; bars.style.display = 'none'; }
        document.getElementById('results').style.display = 'block';
    } catch (err) {
        console.error(err);
        alert("Error connecting to backend");
    }
    
    btn.innerText = originalText;
}

function renderResults(items) {
    // Bar chart removed — keep function to avoid errors from other code paths
    const container = document.getElementById('bars-container');
    if (container) { container.innerHTML = ''; container.style.display = 'none'; }
}

// -----------------------------
// Drag-hover and home animations
// -----------------------------
(() => {
    let dragging = false;

    // Track pointer / touch dragging state
    window.addEventListener('pointerdown', (e) => { if (e.isPrimary) dragging = true; });
    window.addEventListener('pointerup', (e) => { if (e.isPrimary) dragging = false; clearDragHover(); });
    window.addEventListener('touchstart', (e) => { dragging = true; });
    window.addEventListener('touchend', (e) => { dragging = false; clearDragHover(); });

    function clearDragHover() {
        document.querySelectorAll('.drag-hover').forEach(el => el.classList.remove('drag-hover'));
    }

    // Add listeners for feature icons and tree nodes
    function initDragHoverTargets() {
        document.querySelectorAll('.feature-card').forEach(card => {
            card.addEventListener('pointerenter', (e) => { if (dragging) card.classList.add('drag-hover'); });
            card.addEventListener('pointerleave', (e) => { card.classList.remove('drag-hover'); });
            // also allow click-and-drag style movement
            card.addEventListener('pointerdown', (e) => { card.classList.add('drag-hover'); });
        });

        document.querySelectorAll('.node').forEach(node => {
            node.addEventListener('pointerenter', (e) => { if (dragging) node.classList.add('drag-hover'); });
            node.addEventListener('pointerleave', (e) => { node.classList.remove('drag-hover'); });
        });
    }

    // Trigger hero animation and floaty animation on load
    function initHeroAnimations() {
        const hero = document.querySelector('.hero');
        if (hero) {
            // add entrance class after a tick for smoother effect
            setTimeout(() => hero.classList.add('animate-in'), 80);
        }
        // animate feature icons with a stagger
        const cards = Array.from(document.querySelectorAll('.feature-card'));
        cards.forEach((c, i) => {
            setTimeout(() => c.classList.add('animate-float'), 400 + i * 180);
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        initDragHoverTargets();
        initHeroAnimations();
    });
})();