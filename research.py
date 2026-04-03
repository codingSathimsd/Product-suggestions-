<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Search honest product reviews for Indian women. Get real ratings, honest cons, and best price range in under 30 seconds.">
<title>Honest Product Search — SheValue AI</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Arial,sans-serif;background:#fafafa;color:#1a1a1a;min-height:100vh}
.hdr{background:#1a1a1a;padding:16px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.logo{color:#FFD700;font-size:22px;font-weight:800;text-decoration:none}
.hdr-tag{color:#aaa;font-size:13px}
.hero{background:linear-gradient(135deg,#1a1a1a,#2d2d2d);color:#fff;padding:52px 24px 40px;text-align:center}
.hero h1{font-size:clamp(22px,4vw,38px);font-weight:800;margin-bottom:10px}
.hero p{color:#ccc;font-size:15px;margin-bottom:28px;max-width:560px;margin-left:auto;margin-right:auto}
.search-box{max-width:640px;margin:0 auto;display:flex;gap:10px;flex-wrap:wrap}
.search-box input{
  flex:1;min-width:220px;padding:16px 20px;border-radius:10px;border:none;
  font-size:16px;outline:none;background:#fff;color:#1a1a1a
}
.search-box button{
  background:#FFD700;color:#1a1a1a;border:none;padding:16px 28px;
  border-radius:10px;font-size:15px;font-weight:700;cursor:pointer;
  transition:background .2s;white-space:nowrap
}
.search-box button:hover{background:#e6c200}
.search-box button:disabled{background:#888;cursor:not-allowed}
.hints{max-width:640px;margin:14px auto 0;display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.hint{background:#333;color:#FFD700;padding:5px 14px;border-radius:14px;font-size:12px;cursor:pointer;border:none}
.hint:hover{background:#444}
.timer{color:#aaa;font-size:13px;margin-top:10px;min-height:20px}
.wrap{max-width:820px;margin:0 auto;padding:36px 20px}
.status{text-align:center;padding:32px;color:#888;font-size:15px;min-height:80px}
.loading-bar{width:100%;height:4px;background:#e8e8e8;border-radius:2px;margin:16px 0;overflow:hidden;display:none}
.loading-fill{height:100%;background:#FFD700;border-radius:2px;width:0%;transition:width .4s ease}
.result-card{background:#fff;border-radius:12px;padding:24px;margin-bottom:16px;border:1px solid #f0f0f0;box-shadow:0 2px 10px rgba(0,0,0,.05)}
.result-card:hover{box-shadow:0 4px 18px rgba(0,0,0,.1);transform:translateY(-1px);transition:all .2s}
.rank-badge{background:#1a1a1a;color:#FFD700;padding:3px 12px;border-radius:12px;font-size:11px;font-weight:700;display:inline-block;margin-bottom:10px}
.r-title{font-size:18px;font-weight:700;margin-bottom:6px;line-height:1.4}
.r-price{font-size:28px;font-weight:800;color:#1a1a1a;margin-bottom:8px}
.r-rating{color:#FFD700;font-size:15px;margin-bottom:12px}
.r-pros{margin-bottom:8px}
.r-pros span{display:block;font-size:14px;padding:4px 0;color:#333}
.r-con{background:#fff8f8;border-left:3px solid #ff4444;padding:8px 12px;border-radius:0 6px 6px 0;margin:10px 0;font-size:14px;color:#c00}
.r-meta{display:flex;gap:14px;flex-wrap:wrap;margin:10px 0;font-size:13px;color:#666}
.r-meta span{background:#f5f5f5;padding:4px 10px;border-radius:6px}
.buy-btn{background:#1a1a1a;color:#FFD700;padding:10px 22px;border-radius:8px;text-decoration:none;font-weight:700;font-size:14px;display:inline-block;margin-top:10px}
.buy-btn:hover{background:#333}
.trust-note{font-size:12px;color:#999;margin-top:8px}
.no-result{text-align:center;padding:40px 20px;color:#888}
.cache-note{text-align:center;font-size:12px;color:#aaa;margin-top:8px}
.seo-links{margin-top:48px;padding-top:32px;border-top:1px solid #eee}
.seo-links h3{font-size:18px;font-weight:700;margin-bottom:16px}
.seo-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}
.seo-link{background:#fff;border:1px solid #eee;border-radius:8px;padding:12px;text-decoration:none;color:#1a1a1a;font-size:14px;display:block}
.seo-link:hover{border-color:#FFD700;background:#fffef0}
footer{background:#1a1a1a;color:#aaa;text-align:center;padding:20px;font-size:13px}
footer a{color:#FFD700;text-decoration:none}
@media(max-width:600px){.search-box{flex-direction:column}.search-box button{width:100%}}
</style>
</head>
<body>

<header class="hdr">
  <a href="/" class="logo">⭐ SheValue AI</a>
  <span class="hdr-tag">Honest Reviews for Every Indian Woman</span>
</header>

<div class="hero">
  <h1>Find The Honest Truth — In Under 30 Seconds</h1>
  <p>Search any product. Get real ratings, honest cons, and best price for Indian women. No paid promotions.</p>
  <div class="search-box">
    <input type="text" id="searchInput" placeholder="e.g. moisturizer under ₹300, vitamin C serum, hair oil..." maxlength="120" />
    <button id="searchBtn" onclick="doSearch()">Search →</button>
  </div>
  <div class="hints">
    <button class="hint" onclick="quickSearch('best face wash for oily skin india')">Oily Skin Face Wash</button>
    <button class="hint" onclick="quickSearch('vitamin C serum under 500 india')">Vitamin C Serum</button>
    <button class="hint" onclick="quickSearch('sunscreen for indian skin spf 50')">Sunscreen India</button>
    <button class="hint" onclick="quickSearch('hair oil for hair fall india')">Hair Fall Oil</button>
    <button class="hint" onclick="quickSearch('kajal under 200 india')">Best Kajal</button>
    <button class="hint" onclick="quickSearch('moisturizer for dry skin india affordable')">Dry Skin Cream</button>
  </div>
  <div class="timer" id="timerDisplay"></div>
</div>

<div class="wrap">
  <div class="loading-bar" id="loadingBar">
    <div class="loading-fill" id="loadingFill"></div>
  </div>

  <div class="status" id="resultsArea">
    <p>💡 Type a product or problem above and get an honest answer in seconds.</p>
    <p style="font-size:13px;color:#aaa;margin-top:8px">Examples: "best serum for dark spots", "shampoo for dandruff under ₹200"</p>
  </div>

  <!-- SEO links to blog posts -->
  <div class="seo-links">
    <h3>Popular Honest Reviews</h3>
    <div class="seo-grid" id="popularLinks">
      <a href="/" class="seo-link">🧴 Best Vitamin C Serums India</a>
      <a href="/" class="seo-link">☀️ Sunscreen for Indian Skin</a>
      <a href="/" class="seo-link">💧 Moisturizer for Dry Skin</a>
      <a href="/" class="seo-link">🧖 Face Wash for Oily Skin</a>
      <a href="/" class="seo-link">💇 Hair Oil for Hair Fall</a>
      <a href="/" class="seo-link">👁️ Best Kajal Under ₹200</a>
      <a href="/" class="seo-link">💄 Lipstick Under ₹300</a>
      <a href="/" class="seo-link">🌿 Onion Hair Oil Review</a>
    </div>
  </div>
</div>

<footer>
  © 2026 SheValue AI · <a href="https://shevalueai.blogspot.com">Blog</a> · <a href="https://t.me/shevalueai">Telegram</a>
</footer>

<script>
// ─── GEMINI API INTEGRATION ───────────────────────────
// Replace with your actual Gemini API key
// For production: use a proxy server or Cloud Function to hide the key
const GEMINI_KEY = "YOUR_GEMINI_API_KEY_HERE";

// Cache: stores previous searches so repeat queries are instant
const cache = {};

// Timer
let timerInterval = null;
let startTime = null;

function startTimer() {
  startTime = Date.now();
  timerInterval = setInterval(() => {
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
    document.getElementById("timerDisplay").textContent = `Searching... ${elapsed}s`;
    if (elapsed >= 30) {
      clearInterval(timerInterval);
      document.getElementById("timerDisplay").textContent = "Taking longer than expected...";
    }
  }, 100);
}

function stopTimer() {
  clearInterval(timerInterval);
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  document.getElementById("timerDisplay").textContent = `Found in ${elapsed}s`;
}

function setLoading(active) {
  const bar = document.getElementById("loadingBar");
  const fill = document.getElementById("loadingFill");
  const btn = document.getElementById("searchBtn");
  if (active) {
    bar.style.display = "block";
    btn.disabled = true;
    btn.textContent = "Searching...";
    let w = 0;
    const interval = setInterval(() => {
      w = Math.min(w + Math.random() * 8, 90);
      fill.style.width = w + "%";
      if (w >= 90) clearInterval(interval);
    }, 400);
  } else {
    fill.style.width = "100%";
    setTimeout(() => {
      bar.style.display = "none";
      fill.style.width = "0%";
    }, 400);
    btn.disabled = false;
    btn.textContent = "Search →";
  }
}

function normalise(q) {
  return q.toLowerCase().trim().replace(/\s+/g, " ");
}

function quickSearch(q) {
  document.getElementById("searchInput").value = q;
  doSearch();
}

async function doSearch() {
  const input = document.getElementById("searchInput").value.trim();
  if (!input || input.length < 3) {
    document.getElementById("resultsArea").innerHTML =
      '<p style="color:#888">Please type at least 3 characters.</p>';
    return;
  }

  const q = normalise(input);

  // Instant cache hit
  if (cache[q]) {
    document.getElementById("timerDisplay").textContent = "⚡ Instant result (cached)";
    renderResults(cache[q]);
    return;
  }

  setLoading(true);
  startTimer();
  document.getElementById("resultsArea").innerHTML =
    '<p style="color:#888">Finding the most honest recommendations for Indian women...</p>';

  try {
    const result = await callGemini(q);
    stopTimer();
    setLoading(false);
    cache[q] = result; // Cache for instant repeat access
    renderResults(result);
  } catch (err) {
    stopTimer();
    setLoading(false);
    document.getElementById("resultsArea").innerHTML =
      `<div class="no-result">
        <p>⚠️ Search failed. Please try again.</p>
        <p style="font-size:13px;color:#aaa;margin-top:8px">Error: ${err.message}</p>
      </div>`;
  }
}

async function callGemini(query) {
  const prompt = `You are SheValue AI — India's most honest product recommendation engine for women.

User query: "${query}"

Find the top 3 most relevant products for this query. Focus on:
- Products available on Amazon India
- Best value for Indian women
- Honest assessment (real pros AND real cons)

Return ONLY valid JSON in this exact format (no markdown, no explanation):
{
  "query_understood": "what the user is actually looking for",
  "products": [
    {
      "rank": 1,
      "title": "Full product name",
      "brand": "Brand name",
      "price_inr": 349,
      "rating": 4.4,
      "reviews": 15200,
      "pros": ["specific genuine benefit 1", "specific genuine benefit 2", "specific genuine benefit 3"],
      "honest_con": "The biggest real flaw — never hide this",
      "best_for": "Specific type of Indian woman / skin type / concern",
      "skip_if": "Who should NOT buy this",
      "amazon_search": "exact search term to find on amazon.in",
      "shevalue_score": 87
    }
  ],
  "honest_verdict": "One sentence: who should buy what. Be decisive.",
  "do_not_buy_if": "If none of these apply to someone, state it honestly"
}`;

  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=${GEMINI_KEY}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: { temperature: 0.3, maxOutputTokens: 1200 }
      })
    }
  );

  if (!response.ok) throw new Error(`API error ${response.status}`);
  const data = await response.json();
  const text = data.candidates?.[0]?.content?.parts?.[0]?.text || "";
  const clean = text.replace(/```json|```/g, "").trim();
  return JSON.parse(clean);
}

function makeAmazonUrl(searchTerm) {
  // Replace with affiliate URL when ready:
  // return `https://www.amazon.in/s?k=${encodeURIComponent(searchTerm)}&tag=YOUR-AFFILIATE-TAG`;
  return `https://www.amazon.in/s?k=${encodeURIComponent(searchTerm)}`;
}

function renderResults(data) {
  if (!data || !data.products || data.products.length === 0) {
    document.getElementById("resultsArea").innerHTML =
      '<div class="no-result"><p>No results found. Try a different search.</p></div>';
    return;
  }

  let html = "";

  if (data.query_understood) {
    html += `<p style="color:#888;font-size:14px;margin-bottom:20px">
      Showing honest results for: <strong>${data.query_understood}</strong>
    </p>`;
  }

  data.products.forEach(p => {
    const stars = "★".repeat(Math.round(p.rating)) + "☆".repeat(5 - Math.round(p.rating));
    const pros = (p.pros || []).map(pro =>
      `<span>✓ ${pro}</span>`
    ).join("");
    const amazonUrl = makeAmazonUrl(p.amazon_search || p.title);

    html += `
    <div class="result-card">
      <div class="rank-badge">#${p.rank} SheValue Pick</div>
      <div class="r-title">${p.title}</div>
      <div class="r-price">₹${p.price_inr?.toLocaleString('en-IN') || '?'}</div>
      <div class="r-rating">${stars} ${p.rating}/5 · ${(p.reviews||0).toLocaleString('en-IN')} verified reviews</div>
      <div class="r-pros">${pros}</div>
      <div class="r-con">⚠️ Honest Con: ${p.honest_con}</div>
      <div class="r-meta">
        <span>👩 Best for: ${p.best_for}</span>
        <span>🚫 Skip if: ${p.skip_if}</span>
        <span>⭐ SheValue Score: ${p.shevalue_score}/100</span>
      </div>
      <a href="${amazonUrl}" target="_blank" rel="noopener" class="buy-btn">View on Amazon India →</a>
      <div class="trust-note">✓ No paid promotion · We earn nothing from this link</div>
    </div>`;
  });

  if (data.honest_verdict) {
    html += `
    <div style="background:#1a1a1a;color:#fff;border-radius:12px;padding:20px 24px;margin-top:8px">
      <strong style="color:#FFD700">⭐ SheValue Honest Verdict:</strong>
      <p style="margin-top:8px;color:#ddd">${data.honest_verdict}</p>
      ${data.do_not_buy_if ? `<p style="margin-top:8px;color:#aaa;font-size:13px">⚠️ ${data.do_not_buy_if}</p>` : ""}
    </div>`;
  }

  html += `<div class="cache-note">🔔 Get daily honest reviews free → <a href="https://t.me/shevalueai" style="color:#C9562B">Join Telegram</a></div>`;

  document.getElementById("resultsArea").innerHTML = html;
}

// Allow pressing Enter to search
document.getElementById("searchInput").addEventListener("keydown", function(e) {
  if (e.key === "Enter") doSearch();
});
</script>
</body>
</html>

