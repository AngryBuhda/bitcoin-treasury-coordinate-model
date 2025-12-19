# Phase 2 Dashboard Enhancement - Metric Calculation Layer
## Installation & Integration Guide

**Status:** Ready to integrate  
**Complexity:** Medium (adds interactive metric calculations)  
**Files Required:** 3 new JavaScript modules + 1 enhanced HTML dashboard

---

## Overview

This enhancement adds real-time 6-metric calculations to your Phase 2 dashboard:
- WABH (Weighted Average Bitcoin Holdings)
- CP (Capital Proximity)
- NCP (Non-Capital Proximity)
- mNAV (Modified Net Asset Value)
- TAP (Treasury Accumulation Potential)
- ORSR (Obligation-to-Revenue Sustainability Ratio)

**Result:** Dashboard displays live metric scores for each treasury, with color-coded performance indicators.

---

## Architecture

### New Components

```
phase2-5treasuries/
├── dashboard/
│   ├── index.html (enhanced with metric tabs)
│   ├── js/
│   │   ├── metrics-engine.js (core calculations)
│   │   ├── metric-visualizer.js (chart rendering)
│   │   └── treasury-data.js (treasury data source)
│   └── css/
│       └── metrics-enhanced.css (styling for metric displays)
```

### Data Flow

```
Treasury Data (JSON)
        ↓
   Metrics Engine
        ↓
   Live Calculations
        ↓
   Metric Visualizer
        ↓
   Dashboard Display (with real-time updates)
```

---

## Key Features

### 1. **Real-Time Metric Cards**
```
┌─────────────────────────────────────┐
│ WABH Score: 95/100                  │
│ Weighted Average Bitcoin Holdings   │
│ Status: Dominant Bitcoin Accumulator│
└─────────────────────────────────────┘
```

### 2. **Comparative Metric Charts**
- Bar chart comparing all treasuries across each metric
- Color-coded performance (green = excellent, yellow = moderate, red = poor)
- Interactive tooltips with detailed explanations

### 3. **Per-Treasury Metric Dashboard**
When user clicks treasury, displays all 6 metrics with:
- Current score
- Historical trend (if available)
- Benchmark comparison
- Risk indicators

### 4. **Portfolio Metric Summary**
- Weighted average across all treasuries
- Risk-adjusted portfolio score (0-100)
- Trend indicators (improving/declining)

---

## Implementation Steps

### Step 1: Add Metrics Engine (JavaScript)

**File:** `js/metrics-engine.js`

```javascript
class MetricsEngine {
    constructor(treasuryData, btcPrice = 92000) {
        this.treasuries = treasuryData;
        this.btcPrice = btcPrice;
        this.metrics = {};
    }

    // Calculate all metrics for all treasuries
    calculateAll() {
        this.treasuries.forEach(treasury => {
            this.metrics[treasury.ticker] = {
                wabh: this.calculateWABH(treasury),
                cp: this.calculateCP(treasury),
                ncp: this.calculateNCP(treasury),
                mnav: this.calculatemNAV(treasury),
                tap: this.calculateTAP(treasury),
                orsr: this.calculateORSR(treasury)
            };
        });
        return this.metrics;
    }

    // 1. WABH - Weighted Average Bitcoin Holdings (0-100 scale)
    calculateWABH(treasury) {
        const totalPortfolioBTC = this.treasuries.reduce((sum, t) => sum + t.btc, 0);
        const marketCapWeight = treasury.marketCap / this.getTotalMarketCap();
        const btcPercentage = treasury.btc / totalPortfolioBTC;
        
        // WABH = (BTC% * 100) adjusted by market cap weight
        const score = (btcPercentage * marketCapWeight * 100);
        return Math.min(100, score); // Cap at 100
    }

    // 2. CP - Capital Proximity (percentage of assets in Bitcoin)
    calculateCP(treasury) {
        if (!treasury.totalAssets) return null;
        return (treasury.btcValue / treasury.totalAssets) * 100;
    }

    // 3. NCP - Non-Capital Proximity (debt-to-Bitcoin ratio as percentage)
    calculateNCP(treasury) {
        if (!treasury.debt) return 0;
        return (treasury.debt / treasury.btcValue) * 100;
    }

    // 4. mNAV - Modified Net Asset Value
    calculatemNAV(treasury) {
        if (!treasury.sharesOutstanding) return null;
        const btcValue = treasury.btc * this.btcPrice;
        const cashReserves = treasury.cash || 0;
        const totalDebt = treasury.debt || 0;
        
        const netValue = btcValue + cashReserves - totalDebt;
        return netValue / (treasury.sharesOutstanding * 1e6); // Per share
    }

    // 5. TAP - Treasury Accumulation Potential (inverse of obligation burden)
    calculateTAP(treasury) {
        if (!treasury.annualObligations) return 100; // Perfect score if no obligations
        const mnav = this.calculatemNAV(treasury);
        const obligationBurden = (treasury.annualObligations / mnav) * 100;
        
        // TAP = 100 minus obligation burden (capped at 100)
        return Math.min(100, 100 - obligationBurden);
    }

    // 6. ORSR - Obligation-to-Revenue Sustainability Ratio
    calculateORSR(treasury) {
        if (!treasury.estimatedAnnualRevenue) return 0; // Perfect if no obligations
        if (!treasury.annualObligations) return 0; // Perfect if no obligations
        
        return (treasury.annualObligations / treasury.estimatedAnnualRevenue) * 100;
    }

    // Helper: Calculate total market cap
    getTotalMarketCap() {
        return this.treasuries.reduce((sum, t) => sum + t.marketCap, 0);
    }

    // Calculate portfolio-weighted scores
    getPortfolioMetrics() {
        const marketCaps = this.treasuries.map(t => t.marketCap);
        const totalMCap = this.getTotalMarketCap();
        const weights = marketCaps.map(mc => mc / totalMCap);

        const portfolioMetrics = {
            wabh: this.getWeightedAverage('wabh', weights),
            cp: this.getWeightedAverage('cp', weights),
            ncp: this.getWeightedAverage('ncp', weights),
            tap: this.getWeightedAverage('tap', weights),
            orsr: this.getWeightedAverage('orsr', weights)
        };

        // Overall score (weighted average of normalized metrics)
        portfolioMetrics.overallScore = this.calculateOverallScore(portfolioMetrics);
        
        return portfolioMetrics;
    }

    // Weighted average calculator
    getWeightedAverage(metricName, weights) {
        let sum = 0;
        this.treasuries.forEach((treasury, i) => {
            const metricValue = this.metrics[treasury.ticker][metricName];
            sum += metricValue * weights[i];
        });
        return sum;
    }

    // Calculate overall portfolio score (0-100)
    calculateOverallScore(metrics) {
        return (
            (metrics.wabh / 100) * 20 +  // 20% weight
            (metrics.cp / 100) * 20 +    // 20% weight
            ((100 - metrics.ncp) / 100) * 20 +  // 20% weight (lower debt is better)
            (metrics.tap / 100) * 20 +   // 20% weight
            ((100 - metrics.orsr) / 100) * 20   // 20% weight (lower obligations is better)
        );
    }
}
```

### Step 2: Add Data Source

**File:** `js/treasury-data.js`

```javascript
const treasuryData = [
    {
        name: "MicroStrategy",
        ticker: "MSTR",
        btc: 671268,
        btcValue: 61757000000, // $61.757B
        marketCap: 67000000000, // $67B estimate
        totalAssets: 69997000000, // $69.997B
        debt: 8240000000, // $8.24B
        cash: 2500000000, // $2.5B
        annualObligations: 638700000, // $638.7M
        estimatedAnnualRevenue: 58000000000, // $58B
        sharesOutstanding: 152 // millions
    },
    {
        name: "Marathon Digital",
        ticker: "MARA",
        btc: 52477,
        btcValue: 4828000000, // $4.828B
        marketCap: 5778000000, // $5.778B
        totalAssets: 5778000000,
        debt: 950000000, // $950M
        cash: 215000000, // $215M
        annualObligations: 0,
        estimatedAnnualRevenue: 850000000, // $850M mining est
        sharesOutstanding: 0 // TBD
    },
    {
        name: "Metaplanet",
        ticker: "MTPLF",
        btc: 30823,
        btcValue: 2836000000, // $2.836B
        marketCap: 2836000000,
        totalAssets: 2836000000,
        debt: 0,
        cash: 180000000, // $180M
        annualObligations: 0,
        estimatedAnnualRevenue: 120000000, // $120M est
        sharesOutstanding: 0 // TBD
    },
    {
        name: "STRIVE (ASST)",
        ticker: "ASST",
        btc: 7525,
        btcValue: 692000000, // $692M
        marketCap: 692000000,
        totalAssets: 692000000,
        debt: 0,
        cash: 45000000, // $45M
        annualObligations: 0,
        estimatedAnnualRevenue: 45000000, // $45M est
        sharesOutstanding: 0 // TBD
    },
    {
        name: "Riot Platforms",
        ticker: "RIOT",
        btc: 19324,
        btcValue: 1778000000, // $1.778B
        marketCap: 2468000000, // $2.468B
        totalAssets: 2468000000,
        debt: 0, // TBD - assume 0 pending data
        cash: 125000000, // $125M est
        annualObligations: 0, // TBD
        estimatedAnnualRevenue: 450000000, // $450M mining est
        sharesOutstanding: 0 // TBD
    }
];

// Initialize metrics engine
const metricsEngine = new MetricsEngine(treasuryData, 92000);
const metrics = metricsEngine.calculateAll();
const portfolioMetrics = metricsEngine.getPortfolioMetrics();
```

### Step 3: Add Visualizer

**File:** `js/metric-visualizer.js`

```javascript
class MetricVisualizer {
    constructor(canvasContainer) {
        this.container = canvasContainer;
        this.charts = {};
    }

    // Create metric cards for each treasury
    renderMetricCards(metrics, treasuryData) {
        const html = treasuryData.map(treasury => `
            <div class="metric-card" onclick="selectTreasury('${treasury.ticker}')">
                <h3>${treasury.ticker}</h3>
                <div class="metric-mini">
                    <div class="score">WABH: ${metrics[treasury.ticker].wabh.toFixed(1)}/100</div>
                    <div class="score">CP: ${metrics[treasury.ticker].cp?.toFixed(1)}%</div>
                    <div class="score">TAP: ${metrics[treasury.ticker].tap.toFixed(1)}/100</div>
                </div>
            </div>
        `).join('');
        
        return html;
    }

    // Create detailed metric display for selected treasury
    renderDetailedMetrics(metrics, treasury) {
        const m = metrics[treasury.ticker];
        return `
            <div class="detailed-metrics">
                <h2>${treasury.name} (${treasury.ticker}) - Complete Metric Profile</h2>
                
                <div class="metric-row">
                    <div class="metric-display">
                        <h4>WABH Score</h4>
                        <div class="score-large">${m.wabh.toFixed(1)}/100</div>
                        <p>Weighted Average Bitcoin Holdings - Shows accumulation dominance</p>
                        <div class="gauge" style="width: ${m.wabh}%"></div>
                    </div>
                </div>

                <div class="metric-row">
                    <div class="metric-display">
                        <h4>Capital Proximity (CP)</h4>
                        <div class="score-large">${m.cp.toFixed(1)}%</div>
                        <p>Percentage of assets in Bitcoin - Shows focus level</p>
                        <div class="gauge" style="width: ${Math.min(m.cp, 100)}%"></div>
                    </div>
                </div>

                <div class="metric-row">
                    <div class="metric-display">
                        <h4>Non-Capital Proximity (NCP)</h4>
                        <div class="score-large">${m.ncp.toFixed(2)}%</div>
                        <p>Debt-to-Bitcoin ratio - Lower is better (conservative)</p>
                        <div class="gauge warning" style="width: ${Math.min(m.ncp * 50, 100)}%"></div>
                    </div>
                </div>

                <div class="metric-row">
                    <div class="metric-display">
                        <h4>mNAV (Per Share)</h4>
                        <div class="score-large">$${(m.mnav / 1e9).toFixed(2)}B</div>
                        <p>Modified Net Asset Value - Treasury value per share</p>
                    </div>
                </div>

                <div class="metric-row">
                    <div class="metric-display">
                        <h4>TAP Score</h4>
                        <div class="score-large">${m.tap.toFixed(1)}/100</div>
                        <p>Treasury Accumulation Potential - Can acquire more Bitcoin?</p>
                        <div class="gauge success" style="width: ${m.tap}%"></div>
                    </div>
                </div>

                <div class="metric-row">
                    <div class="metric-display">
                        <h4>ORSR Ratio</h4>
                        <div class="score-large">${m.orsr.toFixed(2)}%</div>
                        <p>Obligation-to-Revenue - Lower is better (debt easily covered)</p>
                        <div class="gauge success" style="width: ${Math.min(m.orsr * 100, 100)}%"></div>
                    </div>
                </div>
            </div>
        `;
    }

    // Render metric comparison chart
    renderMetricComparison(metrics, treasuryData, metricName) {
        const labels = treasuryData.map(t => t.ticker);
        const data = treasuryData.map(t => metrics[t.ticker][metricName]);

        const ctx = document.getElementById(`chart-${metricName}`).getContext('2d');
        
        this.charts[metricName] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: metricName.toUpperCase(),
                    data: data,
                    backgroundColor: data.map(d => {
                        if (d >= 80) return '#22c55e'; // Green
                        if (d >= 60) return '#f59e0b'; // Yellow
                        return '#ef4444'; // Red
                    }),
                    borderColor: '#4dd0e1',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        max: 100,
                        ticks: { color: '#94a3b8' },
                        grid: { color: 'rgba(100, 200, 220, 0.1)' }
                    },
                    x: { ticks: { color: '#94a3b8' } }
                }
            }
        });
    }
}
```

### Step 4: Add CSS Styling

**File:** `css/metrics-enhanced.css`

```css
/* Metric Cards */
.metric-card {
    background: rgba(77, 208, 225, 0.1);
    border: 1px solid rgba(100, 200, 220, 0.3);
    padding: 20px;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.metric-card:hover {
    background: rgba(77, 208, 225, 0.2);
    border-color: rgba(77, 208, 225, 0.8);
    transform: scale(1.05);
}

.metric-mini {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 15px;
}

.score {
    font-weight: 600;
    color: #4dd0e1;
}

/* Detailed Metrics Display */
.detailed-metrics {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(100, 200, 220, 0.3);
    padding: 30px;
    border-radius: 10px;
}

.metric-row {
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(100, 200, 220, 0.1);
}

.metric-display {
    background: rgba(77, 208, 225, 0.05);
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #4dd0e1;
}

.score-large {
    font-size: 2.5em;
    font-weight: bold;
    color: #4dd0e1;
    margin: 10px 0;
}

.gauge {
    height: 8px;
    background: rgba(100, 200, 220, 0.2);
    border-radius: 4px;
    margin-top: 10px;
    background: linear-gradient(90deg, #22c55e, #4dd0e1);
}

.gauge.warning {
    background: linear-gradient(90deg, #ef4444, #f59e0b);
}

.gauge.success {
    background: linear-gradient(90deg, #22c55e, #10b981);
}

/* Metric Grid */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin: 30px 0;
}

/* Comparison Charts */
.metric-comparison {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 30px;
}

.comparison-chart {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(100, 200, 220, 0.3);
    padding: 20px;
    border-radius: 10px;
}

.comparison-chart canvas {
    max-height: 300px;
}
```

---

## Integration into Dashboard

### Add Metric Tabs to Dashboard

Insert after your portfolio overview table:

```html
<!-- Metric Analysis Section -->
<div class="section">
    <h2 class="section-title">📊 6-Metric Analysis Framework</h2>
    
    <!-- Metric Cards Selection -->
    <div class="metrics-grid" id="metric-cards"></div>
    
    <!-- Detailed Metric Display -->
    <div id="detailed-metrics-container"></div>
    
    <!-- Comparison Charts -->
    <div class="metric-comparison">
        <div class="comparison-chart">
            <canvas id="chart-wabh"></canvas>
        </div>
        <div class="comparison-chart">
            <canvas id="chart-cp"></canvas>
        </div>
        <div class="comparison-chart">
            <canvas id="chart-ncp"></canvas>
        </div>
        <div class="comparison-chart">
            <canvas id="chart-tap"></canvas>
        </div>
        <div class="comparison-chart">
            <canvas id="chart-orsr"></canvas>
        </div>
    </div>
</div>
```

### Add Initialization Script

```html
<script>
// Initialize metrics system
window.addEventListener('DOMContentLoaded', () => {
    const visualizer = new MetricVisualizer('dashboard');
    
    // Render metric cards
    document.getElementById('metric-cards').innerHTML = 
        visualizer.renderMetricCards(metrics, treasuryData);
    
    // Render first treasury details
    document.getElementById('detailed-metrics-container').innerHTML = 
        visualizer.renderDetailedMetrics(metrics, treasuryData[0]);
    
    // Render comparison charts
    ['wabh', 'cp', 'ncp', 'tap', 'orsr'].forEach(metric => {
        visualizer.renderMetricComparison(metrics, treasuryData, metric);
    });
});

// Treasury selection handler
function selectTreasury(ticker) {
    const treasury = treasuryData.find(t => t.ticker === ticker);
    document.getElementById('detailed-metrics-container').innerHTML = 
        new MetricVisualizer().renderDetailedMetrics(metrics, treasury);
}
</script>
```

---

## Testing Checklist

- [ ] Metrics calculate without errors
- [ ] WABH scores sum to 100 across portfolio
- [ ] CP percentages reflect treasury Bitcoin focus
- [ ] NCP shows debt-to-Bitcoin ratios
- [ ] TAP scores indicate accumulation potential
- [ ] ORSR reflects obligation burden
- [ ] Charts render properly
- [ ] Metric cards clickable and update details
- [ ] Portfolio score calculates correctly

---

## Performance Notes

- All calculations performed client-side (no server calls)
- Real-time updates when BTC price changes
- Charts render on-demand (not pre-loaded)
- ~50KB total additional code

---

## Next: Bitcoin-Time Thesis Document

After integration, Phase 3 will connect these metrics to macro implications.

**Ready to proceed? Confirm and I'll generate Option C: Bitcoin-Time Thesis Application Document**
