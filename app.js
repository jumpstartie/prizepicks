const wallets = [
  {
    wallet: "0x842ac9...7422",
    winRate: 54.9,
    trades: 3760,
    maxDrawdown: 0.73,
    risk: "LOW",
    flags: ["clean"],
  },
  {
    wallet: "0x448861...e319",
    winRate: 64.6,
    trades: 2755,
    maxDrawdown: 8.2,
    risk: "LOW",
    flags: ["posVol"],
  },
  {
    wallet: "0xcd66d7...664f",
    winRate: 59.1,
    trades: 649,
    maxDrawdown: 0.07,
    risk: "LOW",
    flags: ["clean"],
  },
  {
    wallet: "0xea2b42...1fc6",
    winRate: 88.5,
    trades: 3728,
    maxDrawdown: 1.79,
    risk: "MEDIUM",
    flags: ["susWR"],
  },
  {
    wallet: "0xd3b034...329e",
    winRate: 61.8,
    trades: 2461,
    maxDrawdown: 0.15,
    risk: "LOW",
    flags: ["clean"],
  },
  {
    wallet: "0x3e04fb...564d",
    winRate: 53.0,
    trades: 2880,
    maxDrawdown: 3.88,
    risk: "LOW",
    flags: ["clean"],
  },
  {
    wallet: "0x162f6f...798d",
    winRate: 55.0,
    trades: 3492,
    maxDrawdown: 0.36,
    risk: "LOW",
    flags: ["posVol"],
  },
  {
    wallet: "0x23073a...3934",
    winRate: 58.2,
    trades: 1447,
    maxDrawdown: 0.46,
    risk: "LOW",
    flags: ["clean"],
  },
  {
    wallet: "0x39fcd0...e2f2",
    winRate: 55.9,
    trades: 2888,
    maxDrawdown: 0.14,
    risk: "LOW",
    flags: ["posVol"],
  },
  {
    wallet: "0x88d17a...18da",
    winRate: 74.7,
    trades: 2736,
    maxDrawdown: 0.14,
    risk: "LOW",
    flags: ["clean"],
  },
];

const riskRank = {
  LOW: 1,
  MEDIUM: 2,
  HIGH: 3,
};

const watchedWallets = new Set();

const tableBody = document.querySelector("#wallet-table");
const summary = document.querySelector("#table-summary");
const winRateFilter = document.querySelector("#win-rate-filter");
const riskFilter = document.querySelector("#risk-filter");
const tradesFilter = document.querySelector("#trades-filter");
const searchFilter = document.querySelector("#search-filter");
const resetFilters = document.querySelector("#reset-filters");

function formatNumber(value) {
  return new Intl.NumberFormat("en-US").format(value);
}

function getCopyScore(wallet) {
  const tradeDepth = Math.min(wallet.trades / 4000, 1) * 18;
  const winEdge = Math.max(wallet.winRate - 50, 0) * 1.15;
  const drawdownPenalty = Math.min(wallet.maxDrawdown * 2.4, 22);
  const riskPenalty = wallet.risk === "LOW" ? 0 : wallet.risk === "MEDIUM" ? 9 : 18;
  const flagPenalty = wallet.flags.includes("susWR") ? 7 : wallet.flags.includes("posVol") ? 3 : 0;

  return Math.max(0, Math.round(50 + tradeDepth + winEdge - drawdownPenalty - riskPenalty - flagPenalty));
}

function getScoreLabel(score) {
  if (score >= 85) return "prime";
  if (score >= 75) return "strong";
  if (score >= 65) return "watch";
  return "review";
}

function passesFilters(wallet) {
  const minimumWinRate = Number(winRateFilter.value);
  const maximumRisk = riskFilter.value;
  const minimumTrades = Number(tradesFilter.value);
  const searchTerm = searchFilter.value.trim().toLowerCase();
  const searchableText = `${wallet.wallet} ${wallet.flags.join(" ")} ${wallet.risk}`.toLowerCase();

  if (wallet.winRate < minimumWinRate) return false;
  if (wallet.trades < minimumTrades) return false;
  if (maximumRisk !== "ALL" && riskRank[wallet.risk] > riskRank[maximumRisk]) return false;
  if (searchTerm && !searchableText.includes(searchTerm)) return false;

  return true;
}

function renderTable() {
  const rankedWallets = wallets
    .map((wallet) => ({
      ...wallet,
      score: getCopyScore(wallet),
    }))
    .filter(passesFilters)
    .sort((first, second) => second.score - first.score);

  if (rankedWallets.length === 0) {
    tableBody.innerHTML = '<tr><td class="empty-state" colspan="9">No wallets match these filters.</td></tr>';
    summary.textContent = "No wallets match the current scan filters.";
    return;
  }

  tableBody.innerHTML = rankedWallets
    .map((wallet, index) => {
      const scoreLabel = getScoreLabel(wallet.score);
      const isWatched = watchedWallets.has(wallet.wallet);
      const flagHtml = wallet.flags.map((flag) => `<span class="flag-pill">${flag}</span>`).join("");
      const riskClass = `risk-${wallet.risk.toLowerCase()}`;

      return `
        <tr>
          <td>${index + 1}</td>
          <td class="wallet">${wallet.wallet}</td>
          <td class="${wallet.winRate >= 70 ? "metric-strong" : ""}">${wallet.winRate.toFixed(1)}%</td>
          <td>${formatNumber(wallet.trades)}</td>
          <td class="${wallet.maxDrawdown <= 0.75 ? "metric-strong" : ""}">${wallet.maxDrawdown.toFixed(2)}</td>
          <td><span class="risk-pill ${riskClass}">${wallet.risk}</span></td>
          <td>${flagHtml}</td>
          <td class="copy-score">${wallet.score}<small>${scoreLabel}</small></td>
          <td>
            <button class="watch-pill ${isWatched ? "active" : ""}" type="button" data-wallet="${wallet.wallet}">
              ${isWatched ? "Watching" : "Add"}
            </button>
          </td>
        </tr>
      `;
    })
    .join("");

  const watchedCount = rankedWallets.filter((wallet) => watchedWallets.has(wallet.wallet)).length;
  summary.textContent = `Showing ${rankedWallets.length} wallet${rankedWallets.length === 1 ? "" : "s"} sorted by copy score. ${watchedCount} in current watchlist.`;
}

function resetAllFilters() {
  winRateFilter.value = "0";
  riskFilter.value = "ALL";
  tradesFilter.value = "0";
  searchFilter.value = "";
  renderTable();
}

[winRateFilter, riskFilter, tradesFilter, searchFilter].forEach((control) => {
  control.addEventListener("input", renderTable);
});

resetFilters.addEventListener("click", resetAllFilters);

tableBody.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-wallet]");
  if (!button) return;

  const wallet = button.dataset.wallet;
  if (watchedWallets.has(wallet)) {
    watchedWallets.delete(wallet);
  } else {
    watchedWallets.add(wallet);
  }

  renderTable();
});

renderTable();
