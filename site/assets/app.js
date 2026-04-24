
const data = window.__NOTEBOOK_DATA__ || {};
const app = document.getElementById("app");

const views = [
  ["overview", "Overview"],
  ["claims", "Claims"],
  ["timeline", "Timeline"],
  ["sessions", "Sessions"],
  ["workstreams", "Workstreams"],
  ["artifacts", "Artifacts"],
  ["decisions", "Decisions"],
];

const statTargets = {
  claims: "claims",
  milestones: "timeline",
  sessions: "sessions",
  threads: "workstreams",
  artifacts: "artifacts",
  decisions: "decisions",
};

const viewMeta = {
  overview: {
    kicker: "Clinical evidence register",
    title: "Evidence Notebook",
    purpose: () => data.latestClaim.claim,
  },
  claims: {
    kicker: "Canonical dossier reader",
    title: "Claims",
    purpose: () => "Select a research claim and review its claim, evidence, uncertainty, and next action in one fixed reading frame.",
  },
  timeline: {
    kicker: "Milestone spine",
    title: "Timeline",
    purpose: () => "Track completed, active, planned, blocked, and review-needed work by phase, with the next visible move pinned beside the ledger.",
  },
  sessions: {
    kicker: "Run ledger",
    title: "Sessions",
    purpose: () => "Scan recent work by date, outcome, source log, uncertainty, and handoff.",
  },
  workstreams: {
    kicker: "Research lanes",
    title: "Workstreams",
    purpose: () => "Review each active lane by question, latest evidence, risk, and next move.",
  },
  artifacts: {
    kicker: "Artifact shelf",
    title: "Artifacts",
    purpose: () => "Group source documents, active evidence, generated outputs, planned visuals, and dissertation support by purpose and intended use.",
  },
  decisions: {
    kicker: "ADR-style register",
    title: "Decisions",
    purpose: () => "Read durable project decisions through rationale, consequence, and evidence links.",
  },
};

let state = {
  view: location.hash.replace("#", "") || "overview",
  query: "",
  selectedClaim: 0,
};

function textFromHtml(value) {
  const div = document.createElement("div");
  div.innerHTML = value || "";
  return div.textContent || "";
}

function includesQuery(record) {
  if (!state.query) return true;
  const haystack = JSON.stringify(record).toLowerCase();
  return haystack.includes(state.query.toLowerCase());
}

function filtered(records) {
  return records.filter(includesQuery);
}

function setView(view) {
  state.view = view;
  location.hash = view;
  render();
}

function render() {
  const activeView = views.some(([id]) => id === state.view) ? state.view : "overview";
  const meta = viewMeta[activeView] || viewMeta.overview;
  state.view = activeView;
  app.dataset.view = activeView;
  app.innerHTML = `
    <aside class="app-rail">
      <a class="app-mark" href="#overview" data-view-link="overview">EN</a>
      <nav>${views.map(([id, label]) => `<button type="button" class="${id === activeView ? "is-active" : ""}" data-view-link="${id}">${label}</button>`).join("")}</nav>
      <p>Local archive<br>${data.generatedAt}</p>
    </aside>
    <main class="app-main">
      <header class="app-header">
        <div>
          <p class="app-kicker">${meta.kicker}</p>
          <h1>${meta.title}</h1>
          <p>${meta.purpose()}</p>
          <div class="header-meta">
            <span>Generated ${data.generatedAt}</span>
            <span>${activeView === "overview" ? data.latestClaim.title : `${activeViewLabel(activeView)} view`}</span>
          </div>
        </div>
        <label class="app-search">
          <span>Search</span>
          <input type="search" value="${escapeAttr(state.query)}" placeholder="claims, sessions, artifacts..." />
        </label>
      </header>
      <section class="source-ledger">${data.sources.map((source, index) => sourceCard(source, data.sourceFreshness[index])).join("")}</section>
      <section class="app-stats">${data.stats.map((item) => statButton(item)).join("")}</section>
      <section class="app-view">${renderView(activeView)}</section>
    </main>
  `;

  app.querySelectorAll("[data-view-link]").forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      setView(button.dataset.viewLink);
    });
  });

  const search = app.querySelector(".app-search input");
  search.addEventListener("input", (event) => {
    state.query = event.target.value;
    render();
    const next = app.querySelector(".app-search input");
    next.focus();
    next.setSelectionRange(next.value.length, next.value.length);
  });

  app.querySelectorAll("[data-select-claim]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedClaim = Number(button.dataset.selectClaim);
      render();
    });
  });
}

function renderView(view) {
  if (view === "overview") return renderOverview();
  if (view === "claims") return renderClaims();
  if (view === "timeline") return renderTimeline();
  if (view === "sessions") return renderSessions();
  if (view === "workstreams") return renderWorkstreams();
  if (view === "artifacts") return renderArtifacts();
  if (view === "decisions") return renderDecisions();
  return renderOverview();
}

function renderOverview() {
  const claim = data.claims[state.selectedClaim] || data.claims[0];
  const latestDecision = data.decisions[0];
  return `
    <div class="overview-grid">
      ${claimDossier(claim, "Current claim")}
      <aside class="archive-panel action-panel">
        <p class="app-kicker">Active research path</p>
        <span class="status-chip ${statusClass(data.activeMilestone.status)}">${data.activeMilestone.status}</span>
        <h3>${data.activeMilestone.name}</h3>
        <p>${data.activeMilestone.next}</p>
        <button type="button" data-view-link="timeline">Open timeline</button>
      </aside>
      <section class="archive-panel evaluation-panel">
        <div class="panel-heading row">
          <div><p class="app-kicker">Evaluation signal</p><h2>${data.evaluationClaim.title}</h2></div>
          <button type="button" data-view-link="claims">Open claim</button>
        </div>
        <p class="body-lead">${data.evaluationClaim.claim}</p>
        <div class="compact-fields">
          <section><b>Evidence</b>${data.evaluationClaim.evidence}</section>
          <section><b>Uncertainty</b>${data.evaluationClaim.uncertainty}</section>
          <section><b>Next experiment</b>${data.evaluationClaim.next}</section>
        </div>
      </section>
      <section class="archive-panel index-panel session-panel">
        <div class="panel-heading row">
          <div><p class="app-kicker">Run ledger</p><h2>Recent Sessions</h2></div>
          <button type="button" data-view-link="sessions">View all</button>
        </div>
        ${rowsOrEmpty(data.sessions.slice(0, 3).map(sessionRow), "No session logs recorded.")}
      </section>
      <section class="archive-panel index-panel artifact-panel">
        <div class="panel-heading row">
          <div><p class="app-kicker">Output register</p><h2>Artifact Shelf</h2></div>
          <button type="button" data-view-link="artifacts">View all</button>
        </div>
        ${rowsOrEmpty(data.artifacts.slice(0, 5).map(artifactRow), "No artifacts recorded.")}
      </section>
      <section class="archive-panel decision-brief">
        <div class="panel-heading">
          <p class="app-kicker">Decision anchor</p>
          <h2>${latestDecision ? latestDecision.id : "None"}</h2>
        </div>
        ${latestDecision ? `<h3>${latestDecision.title}</h3><p>${latestDecision.decision}</p><small>${latestDecision.evidence}</small>` : `<p>No decisions recorded.</p>`}
      </section>
    </div>
  `;
}

function renderClaims() {
  const claims = filtered(data.claims);
  const selected = claims[state.selectedClaim] || claims[0] || data.claims[0];
  if (!selected) return emptyState("No matching claims.");
  return `
    <div class="claim-app">
      <aside class="record-list">
        ${claims.map((claim, index) => `<button type="button" class="${claim === selected ? "is-active" : ""}" data-select-claim="${index}"><span>${pad(index + 1)}</span>${claim.title}<small>${claimRiskLabel(claim)}</small></button>`).join("")}
      </aside>
      ${claimDossier(selected, "Claim record")}
    </div>
  `;
}

function renderTimeline() {
  const milestones = filtered(data.milestones);
  const next = nextMilestone(milestones);
  return `<section class="archive-panel timeline-panel"><div class="panel-heading"><p class="app-kicker">Milestone spine</p><h2>Timeline</h2></div>${renderTimelineSummary(milestones)}${renderPhaseStrip(milestones)}<aside class="timeline-next"><p class="app-kicker">Next visible move</p><h3>${next ? next.title : "No next milestone"}</h3><p>${next ? next.next : "All filtered milestones are complete."}</p></aside><ol class="app-timeline">${rowsOrEmpty(milestones.map((item) => `
    <li class="${statusClass(item.status)}">
      <span>${item.status}</span>
      <div><h3>${item.title}</h3><p>${item.outcome}</p><small>${item.evidence}</small><em>${item.next}</em></div>
    </li>`), "No matching milestones.")}</ol></section>`;
}

function renderTimelineSummary(milestones) {
  if (!milestones.length) return emptyState("No matching milestones.");
  const keyEvents = timelineKeyEvents(milestones);
  const completed = milestones.filter((item) => normalizedStatus(item.status) === "complete").length;
  const next = nextMilestone(milestones) || milestones[milestones.length - 1];
  const progress = Math.round((completed / milestones.length) * 100);
  return `<div class="timeline-summary">
    <section class="timeline-progress">
      <div>
        <p class="app-kicker">Progress map</p>
        <strong>${completed}/${milestones.length}</strong>
        <span>milestones complete</span>
      </div>
      <div class="progress-rail" aria-hidden="true"><i style="width: ${progress}%"></i></div>
      <p><b>Next visible move</b>${next ? next.title : "No next milestone recorded"}</p>
    </section>
    <section class="timeline-keyline">
      <div class="keyline-heading">
        <p class="app-kicker">Key sequence</p>
        <h3>Major events</h3>
      </div>
      <ol>${keyEvents.map((event, index) => `<li class="${statusClass(event.status)}">
        <span>${pad(index + 1)}</span>
        <strong>${event.title}</strong>
        <small>${event.status}</small>
      </li>`).join("")}</ol>
    </section>
  </div>`;
}

function renderPhaseStrip(milestones) {
  if (!milestones.length) return "";
  const phases = [
    ["Foundation", /source|repository|synthetic|evaluation|protocol|initial|seizure-free/i],
    ["Phase A", /local|provider|h003|ollama|single-prompt/i],
    ["Phase B", /role|multi-agent|verify|h004|evidence support/i],
    ["Dissertation", /visual|dissertation|packaging|write|poster|governance/i],
  ];
  const next = nextMilestone(milestones);
  return `<section class="phase-strip">${phases.map(([label, pattern], index) => {
    const items = milestones.filter((item) => pattern.test(`${item.title} ${item.outcome} ${item.next}`));
    const complete = items.filter((item) => normalizedStatus(item.status) === "complete").length;
    const current = next && items.includes(next);
    const sample = items.find((item) => normalizedStatus(item.status) !== "complete") || items[items.length - 1];
    return `<article class="${current ? "is-current" : ""}"><span>${pad(index + 1)} ${label}</span><strong>${items.length ? `${complete}/${items.length} complete` : "No matched entries"}</strong><small>${sample ? sample.title : "Awaiting source milestone"}</small></article>`;
  }).join("")}</section>`;
}

function nextMilestone(milestones) {
  return milestones.find((item) => normalizedStatus(item.status) !== "complete");
}

function timelineKeyEvents(milestones) {
  const patterns = [/project frame/i, /synthetic subset/i, /evaluation harness/i, /smoke/i, /local model/i, /local dashboard/i, /visual artifacts/i];
  const picked = [];
  patterns.forEach((pattern) => {
    const item = milestones.find((milestone) => pattern.test(milestone.title));
    if (item && !picked.includes(item)) picked.push(item);
  });
  if (picked.length < 4) {
    milestones.forEach((item) => {
      if (picked.length < 4 && !picked.includes(item)) picked.push(item);
    });
  }
  return picked.slice(0, 7);
}

function normalizedStatus(status) {
  return String(status || "").toLowerCase();
}

function renderSessions() {
  const sessions = filtered(data.sessions);
  return `<section class="archive-panel"><div class="panel-heading"><p class="app-kicker">Run ledger</p><h2>Recent Session Feed</h2></div>${rowsOrEmpty(sessions.map((session) => `
    <details class="session-record">
      <summary><span>${session.date}</span><strong>${session.title}</strong><a href="${session.href}">source log</a></summary>
      <p>${session.objective}</p>
      <div class="quad">
        <section><b>Outcome</b>${session.outcome}</section>
        <section><b>Evidence</b>${session.evidence}</section>
        <section><b>Uncertainty</b>${session.uncertainty}</section>
        <section><b>Handoff</b>${session.handoff}</section>
      </div>
      <footer>${session.decision}</footer>
    </details>`), "No matching session logs.")}</section>`;
}

function renderWorkstreams() {
  const workstreams = filtered(data.workstreams);
  return `<div class="card-grid">${rowsOrEmpty(workstreams.map((thread) => `
    <article class="archive-panel">
      <div class="panel-heading"><p class="app-kicker">Thread</p><h2>${thread.name}</h2></div>
      <p class="body-lead">${thread.question}</p>
      <div class="stacked-fields">
        <section><b>Latest evidence</b>${thread.evidence}</section>
        <section><b>Risk</b>${thread.risk}</section>
        <section><b>Next action</b>${thread.next}</section>
      </div>
    </article>`), "No matching workstreams.")}</div>`;
}

function renderArtifacts() {
  const artifacts = filtered(data.artifacts);
  const groups = groupedArtifacts(artifacts);
  return `<section class="archive-panel"><div class="panel-heading"><p class="app-kicker">Artifact shelf</p><h2>Outputs And Planned Visuals</h2></div><div class="artifact-groups">${rowsOrEmpty(groups.map(([label, rows]) => `
    <section class="artifact-group">
      <h3>${label}<small>${artifactGroupPurpose(label)}</small></h3>
      <div class="shelf">${rowsOrEmpty(rows.map(artifactShelfItem), "No artifacts in this group.")}</div>
    </section>`), "No matching artifacts.")}</div></section>`;
}

function renderDecisions() {
  const decisions = filtered(data.decisions);
  return `<section class="archive-panel"><div class="panel-heading"><p class="app-kicker">Decision register</p><h2>Decisions</h2></div>${rowsOrEmpty(decisions.map((decision) => `
    <article class="decision-record">
      <span>${decision.id}</span>
      <div><h3>${decision.title}</h3><p>${decision.decision}</p></div>
      <section><b>Consequence</b>${decision.consequence}<small>${decision.evidence}</small></section>
    </article>`), "No matching decisions.")}</section>`;
}

function claimDossier(claim, label) {
  return `<section class="archive-panel primary-panel claim-dossier">
    <div class="panel-heading">
      <p class="app-kicker">${label}</p>
      <h2>${claim.title}</h2>
    </div>
    <p class="claim-line">${claim.claim}</p>
    <div class="triad">
      <section><b>Evidence</b>${claim.evidence}</section>
      <section><b>Uncertainty</b>${claim.uncertainty}</section>
      <section><b>Next action</b>${claim.next}</section>
    </div>
    <div class="dossier-grid">
      <section class="dossier-block"><b>Claim</b><h3>${claim.title}</h3><p>${claim.claim}</p></section>
      <section class="dossier-block is-evidence"><b>Evidence</b>${claim.evidence}</section>
      <section class="dossier-block is-uncertainty"><b>Uncertainty</b>${claim.uncertainty}</section>
      <section class="dossier-block is-next"><b>Next action</b>${claim.next}</section>
    </div>
  </section>`;
}

function sourceCard(source, freshness) {
  return `<a class="source-card" href="${source.href}">
    <span>Source</span>
    <strong>${source.label}</strong>
    <small>Updated ${freshness ? freshness.updated : "Not recorded"}</small>
  </a>`;
}

function statButton(item) {
  const key = item.label.toLowerCase();
  const target = statTargets[key] || "overview";
  return `<button type="button" data-view-link="${target}"><strong>${item.value}</strong><span>${item.label}</span></button>`;
}

function sessionRow(session) {
  return `<article class="index-row"><span>${session.date}</span><strong>${session.title}</strong><small>${session.objective || session.decision}</small></article>`;
}

function artifactRow(item) {
  return `<article class="index-row artifact-row ${statusClass(item.status)}"><span>${item.status}</span><strong>${item.name}</strong><small>${item.path}</small></article>`;
}

function artifactShelfItem(item) {
  return `<article class="artifact-shelf-item ${statusClass(item.status)}">
    <header><span class="status-chip ${statusClass(item.status)}">${item.status}</span><h4>${item.name}</h4></header>
    <section><b>Purpose</b><p>${item.purpose || "Purpose not recorded."}</p></section>
    <section><b>Path and use</b><p class="artifact-path">${item.path}</p><small>${item.use || "Intended use not recorded."}</small></section>
  </article>`;
}

function rowsOrEmpty(rows, message) {
  return rows.length ? rows.join("") : emptyState(message);
}

function groupedArtifacts(artifacts) {
  const buckets = [
    ["Active evidence", []],
    ["Generated visuals", []],
    ["Session logs", []],
    ["Planned visuals", []],
    ["Dissertation support", []],
    ["Source documents", []],
  ];
  const byLabel = Object.fromEntries(buckets);
  artifacts.forEach((item) => {
    const name = `${item.name} ${item.path} ${item.purpose} ${item.use}`.toLowerCase();
    const status = String(item.status || "").toLowerCase();
    if (status.includes("planned") || name.includes("to be generated")) byLabel["Planned visuals"].push(item);
    else if (name.includes(".png") || name.includes("poster") || name.includes("diagram") || name.includes("visual")) byLabel["Generated visuals"].push(item);
    else if (name.includes("session log") || name.includes("run_logs/")) byLabel["Session logs"].push(item);
    else if (status.includes("active") || name.includes("manifest") || name.includes("run record") || name.includes("dashboard")) byLabel["Active evidence"].push(item);
    else if (name.includes("dissertation") || name.includes("governance") || name.includes("protocol") || name.includes("feasibility") || status.includes("reference")) byLabel["Dissertation support"].push(item);
    else byLabel["Source documents"].push(item);
  });
  return buckets.filter(([, rows]) => rows.length);
}

function artifactGroupPurpose(label) {
  const purposes = {
    "Active evidence": "Live records used to justify current claims.",
    "Generated visuals": "Rendered images and explanatory outputs already produced.",
    "Session logs": "Audit trail for work completed across agent sessions.",
    "Planned visuals": "Figures still to create for review, README, or dissertation use.",
    "Dissertation support": "Protocols, governance, and narrative scaffolding.",
    "Source documents": "Primary project-state inputs and reference notes.",
  };
  return purposes[label] || "Grouped by project use.";
}

function claimRiskLabel(claim) {
  const text = textFromHtml(`${claim.uncertainty || ""} ${claim.next || ""}`).toLowerCase();
  if (text.includes("governance") || text.includes("raw clinical")) return "governance";
  if (text.includes("smoke") || text.includes("not yet") || text.includes("over-abstain")) return "review";
  if (text.includes("regenerate") || text.includes("future")) return "watch";
  return "stable";
}

function activeViewLabel(view) {
  const entry = views.find(([id]) => id === view);
  return entry ? entry[1] : "Overview";
}

function emptyState(message) {
  return `<p class="empty-state">${message}</p>`;
}

function statusClass(status) {
  return `is-${String(status || "unknown").toLowerCase().replace(/[^a-z0-9]+/g, "-")}`;
}

function pad(value) {
  return String(value).padStart(2, "0");
}

function escapeAttr(value) {
  return String(value || "").replaceAll("&", "&amp;").replaceAll('"', "&quot;").replaceAll("<", "&lt;");
}

window.addEventListener("hashchange", () => {
  state.view = location.hash.replace("#", "") || "overview";
  render();
});

render();
