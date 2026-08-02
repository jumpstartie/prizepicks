/*
 * PrizePicks MLB props finder.
 *
 * Ranks the day's MLB player props by a value score that blends model edge
 * (projection vs. the posted line), matchup softness, and recent form, then
 * recommends an Over or Under lean for each prop. Users can filter the board
 * and add plays to a prop slip.
 *
 * The prop data comes from `MLB_PROPS` (see data.js). Replace that array with
 * a live PrizePicks feed to run against real projections.
 */
(function () {
  "use strict";

  const props = (typeof MLB_PROPS !== "undefined" ? MLB_PROPS : []).map(decorateProp);

  const slip = new Set();

  const filters = {
    statType: "ALL",
    lean: "ALL",
    minScore: 0,
    search: "",
  };

  /**
   * Add derived fields to a raw prop:
   *  - edge:        projection minus line (positive => Over lean)
   *  - lean:        "Over" or "Under"
   *  - edgePct:     edge as a fraction of the line
   *  - valueScore:  0-100 ranking that rewards edge, soft matchups, and form
   *  - confidence:  High / Medium / Low tier derived from valueScore
   */
  function decorateProp(prop) {
    const edge = round(prop.projection - prop.line, 2);
    const lean = edge >= 0 ? "Over" : "Under";
    const edgePct = prop.line > 0 ? Math.abs(edge) / prop.line : 0;

    // Recent form agreement: does L10 sit on the same side of the line as our
    // projection? Rewards props where the model and recent form agree.
    const projSide = Math.sign(prop.projection - prop.line);
    const formSide = Math.sign(prop.l10 - prop.line);
    const formAgrees = projSide !== 0 && projSide === formSide;

    // Matchup softness: rank 30 (softest) -> ~1.0, rank 1 (toughest) -> ~0.03.
    const matchupSoftness = prop.matchupRank / 30;

    // Blend the signals into a 0-100 score. Edge is the primary driver; a soft
    // matchup and agreeing recent form provide bounded bonuses.
    const edgeComponent = Math.min(edgePct, 0.6) / 0.6; // cap runaway edges
    let score =
      edgeComponent * 62 + matchupSoftness * 26 + (formAgrees ? 12 : 0);
    score = Math.max(0, Math.min(100, Math.round(score)));

    let confidence = "Low";
    if (score >= 70) confidence = "High";
    else if (score >= 50) confidence = "Medium";

    return Object.assign({}, prop, {
      id: `${prop.player}-${prop.statType}`.replace(/\s+/g, "-").toLowerCase(),
      edge,
      lean,
      edgePct,
      formAgrees,
      valueScore: score,
      confidence,
    });
  }

  function round(value, digits) {
    const factor = Math.pow(10, digits);
    return Math.round(value * factor) / factor;
  }

  function getStatTypes() {
    return Array.from(new Set(props.map((p) => p.statType))).sort();
  }

  function applyFilters() {
    const search = filters.search.trim().toLowerCase();
    return props
      .filter((p) => filters.statType === "ALL" || p.statType === filters.statType)
      .filter((p) => filters.lean === "ALL" || p.lean === filters.lean)
      .filter((p) => p.valueScore >= filters.minScore)
      .filter((p) => {
        if (!search) return true;
        return (
          p.player.toLowerCase().includes(search) ||
          p.team.toLowerCase().includes(search) ||
          p.opponent.toLowerCase().includes(search) ||
          p.statType.toLowerCase().includes(search)
        );
      })
      .sort((a, b) => b.valueScore - a.valueScore);
  }

  function formatSigned(value) {
    const rounded = round(value, 2);
    return (rounded >= 0 ? "+" : "") + rounded.toFixed(2);
  }

  function render() {
    const rows = applyFilters();
    const tbody = document.getElementById("props-table");
    tbody.innerHTML = "";

    rows.forEach((prop, index) => {
      const tr = document.createElement("tr");
      if (slip.has(prop.id)) tr.classList.add("in-slip");

      tr.innerHTML = `
        <td class="rank">${index + 1}</td>
        <td class="player">
          <strong>${prop.player}</strong>
          <span class="matchup">${prop.team} vs ${prop.opponent} &middot; ${prop.gameTime}</span>
        </td>
        <td>${prop.statType}</td>
        <td class="num">${prop.line}</td>
        <td class="num">${prop.projection.toFixed(2)}</td>
        <td class="num ${prop.edge >= 0 ? "pos" : "neg"}">${formatSigned(prop.edge)}</td>
        <td><span class="lean lean-${prop.lean.toLowerCase()}">${prop.lean}</span></td>
        <td><span class="conf conf-${prop.confidence.toLowerCase()}">${prop.confidence}</span></td>
        <td class="num score">${prop.valueScore}</td>
        <td>
          <button type="button" class="slip-toggle" data-id="${prop.id}">
            ${slip.has(prop.id) ? "Remove" : "Add"}
          </button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    const summary = document.getElementById("table-summary");
    summary.textContent = rows.length
      ? `Showing ${rows.length} prop${rows.length === 1 ? "" : "s"} sorted by value score.`
      : "No props match the current filters.";

    renderSlip();
  }

  function renderSlip() {
    const list = document.getElementById("slip-list");
    const count = document.getElementById("slip-count");
    list.innerHTML = "";

    const entries = props.filter((p) => slip.has(p.id));
    count.textContent = String(entries.length);

    if (!entries.length) {
      const li = document.createElement("li");
      li.className = "slip-empty";
      li.textContent = "No props added yet. Tap Add on a play to build your slip.";
      list.appendChild(li);
      return;
    }

    entries
      .sort((a, b) => b.valueScore - a.valueScore)
      .forEach((prop) => {
        const li = document.createElement("li");
        li.innerHTML = `
          <span class="slip-pick">
            <strong>${prop.player}</strong>
            <span>${prop.lean} ${prop.line} ${prop.statType}</span>
          </span>
          <span class="slip-score">${prop.valueScore}</span>
        `;
        list.appendChild(li);
      });
  }

  function bindEvents() {
    document.getElementById("stat-filter").addEventListener("change", (e) => {
      filters.statType = e.target.value;
      render();
    });
    document.getElementById("lean-filter").addEventListener("change", (e) => {
      filters.lean = e.target.value;
      render();
    });
    document.getElementById("score-filter").addEventListener("change", (e) => {
      filters.minScore = Number(e.target.value);
      render();
    });
    document.getElementById("search-filter").addEventListener("input", (e) => {
      filters.search = e.target.value;
      render();
    });
    document.getElementById("reset-filters").addEventListener("click", () => {
      filters.statType = "ALL";
      filters.lean = "ALL";
      filters.minScore = 0;
      filters.search = "";
      document.getElementById("stat-filter").value = "ALL";
      document.getElementById("lean-filter").value = "ALL";
      document.getElementById("score-filter").value = "0";
      document.getElementById("search-filter").value = "";
      render();
    });
    document.getElementById("clear-slip").addEventListener("click", () => {
      slip.clear();
      render();
    });

    document.getElementById("props-table").addEventListener("click", (e) => {
      const button = e.target.closest(".slip-toggle");
      if (!button) return;
      const id = button.getAttribute("data-id");
      if (slip.has(id)) slip.delete(id);
      else slip.add(id);
      render();
    });
  }

  function populateStatFilter() {
    const select = document.getElementById("stat-filter");
    getStatTypes().forEach((stat) => {
      const option = document.createElement("option");
      option.value = stat;
      option.textContent = stat;
      select.appendChild(option);
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    populateStatFilter();
    bindEvents();
    render();
  });
})();
