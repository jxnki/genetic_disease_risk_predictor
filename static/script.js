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
        
        renderResults([
            { label: 'Autosomal Recessive Risk', val: data.risk }
        ]);
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

        renderResults([
            { label: 'Boy (Affected)', val: data.boy },
            { label: 'Girl (Carrier)', val: data.girl_carrier },
            { label: 'Girl (Affected)', val: data.girl_affected }
        ]);
    } catch (err) {
        console.error(err);
        alert("Error connecting to backend");
    }
    
    btn.innerText = originalText;
}

function renderResults(items) {
    const container = document.getElementById('bars-container');
    container.innerHTML = '';
    
    items.forEach(item => {
        let color = '#10b981'; // Green (Low)
        if(item.val > 50) color = '#ef4444'; // Red (High)
        else if(item.val > 20) color = '#f59e0b'; // Orange (Med)

        const html = `
            <div class="bar-wrapper">
                <div class="bar-header">
                    <span>${item.label}</span>
                    <span style="color:${color}">${item.val}%</span>
                </div>
                <div class="bar-bg">
                    <div class="bar-fill" style="width:${item.val}%; background:${color}"></div>
                </div>
            </div>
        `;
        container.innerHTML += html;
    });
    
    document.getElementById('results').style.display = 'block';
}