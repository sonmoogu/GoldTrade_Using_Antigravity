const API_BASE = "http://localhost:8000/api";

// Elements
const toggleBtn = document.getElementById("toggle-trading-btn");
const statusDot = document.getElementById("status-dot");
const statusText = document.getElementById("status-text");

const priceVal = document.getElementById("price-val");
const smaVal = document.getElementById("sma-val");
const volVal = document.getElementById("vol-val");

const balanceVal = document.getElementById("balance-val");
const inventoryVal = document.getElementById("inventory-val");
const positionsList = document.getElementById("positions-list");

let isTrading = false;

// Formatters
const fmtKRW = new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' });
const fmtNum = new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 });

// Fetch Status
async function fetchStatus() {
    try {
        const res = await fetch(`${API_BASE}/status`);
        if (!res.ok) throw new Error("Network response was not ok");
        const data = await res.json();
        updateUI(data);
    } catch (error) {
        console.error("Failed to fetch status:", error);
    }
}

// Toggle Trading
async function toggleTrading() {
    try {
        const res = await fetch(`${API_BASE}/toggle`, { method: "POST" });
        if (!res.ok) throw new Error("Toggle failed");
        const data = await res.json();
        isTrading = data.status === "active";
        updateStatusIndicator();
    } catch (error) {
        console.error("Failed to toggle trading:", error);
    }
}

// Update UI
function updateUI(data) {
    // Status
    isTrading = data.status === "active";
    updateStatusIndicator();

    // Market
    const market = data.market;
    priceVal.textContent = fmtKRW.format(market.current_price);
    
    // Animate price change (micro-animation)
    priceVal.style.transform = "scale(1.05)";
    setTimeout(() => { priceVal.style.transform = "scale(1)"; }, 150);

    smaVal.textContent = fmtNum.format(data.sma);
    volVal.textContent = `${fmtNum.format(market.buy_bids_volume)} / ${fmtNum.format(market.sell_asks_volume)}`;

    // Account
    const account = data.account;
    balanceVal.textContent = fmtKRW.format(account.balance);
    inventoryVal.textContent = `${fmtNum.format(account.gold_inventory)} g`;

    // Positions
    renderPositions(account.positions);
}

function updateStatusIndicator() {
    if (isTrading) {
        statusDot.classList.add("active");
        statusText.textContent = "Trading Active";
        toggleBtn.textContent = "Stop Trading";
        toggleBtn.style.background = "var(--status-paused)";
        toggleBtn.style.color = "#fff";
    } else {
        statusDot.classList.remove("active");
        statusText.textContent = "Paused";
        toggleBtn.textContent = "Start Trading";
        toggleBtn.style.background = "var(--accent-gold)";
        toggleBtn.style.color = "#000";
    }
}

function renderPositions(positions) {
    positionsList.innerHTML = "";
    if (!positions || positions.length === 0) {
        positionsList.innerHTML = `<div class="empty-state">No active positions.</div>`;
        return;
    }

    positions.forEach(pos => {
        const item = document.createElement("div");
        item.className = "position-item";
        item.innerHTML = `
            <span>Entry: ${fmtKRW.format(pos.entry_price)}</span>
            <span>Amount: ${fmtNum.format(pos.amount_grams)}g</span>
        `;
        positionsList.appendChild(item);
    });
}

// Event Listeners
toggleBtn.addEventListener("click", toggleTrading);

// Initial Load & Polling
fetchStatus();
setInterval(fetchStatus, 2000); // Poll every 2 seconds
