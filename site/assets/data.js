window.__NOTEBOOK_DATA__ = {
  "generatedAt": "2026-04-26 08:20 UTC",
  "latestClaim": {
    "title": "Project Snapshot",
    "claim": "The repository is now in early Phase A of the dissertation: a local LLM runtime is live, the first single-prompt LLM harness exists, and the main blocker has shifted from runtime/schema setup to extraction reliability and abstention behaviour."
  },
  "activeMilestone": {
    "name": "M-A2 h003 single-prompt LLM smoke",
    "next": "Inspect the four <code>unknown</code> outputs, tune prompt/schema behavior, and rerun h003 on a 25-row slice.",
    "status": "In progress",
    "outcome": "<code>h003_single_prompt_llm</code> now exists and has produced a first local run record with JSON-schema validation, retries, latency, and token metadata.",
    "risk": "The first n=5 smoke has invalid-output rate 0.80 and mean latency about 52.9 seconds, so the prompt/schema path is not yet strong enough for a 25-50 row comparison.",
    "evidence": "<a href=\"../scripts/run_harness_experiment.py\">scripts/run_harness_experiment.py</a>, <a href=\"../src/epilepsy_agents/llm_pipeline.py\">src/epilepsy_agents/llm_pipeline.py</a>, <a href=\"../project_state/harnesses/README.md\">project_state/harnesses/README.md</a>, <a href=\"../project_state/runs/20260424T171400Z_h003_single_prompt_llm_n5.json\">20260424T171400Z_h003_single_prompt_llm_n5.json</a>"
  },
  "evaluationClaim": {
    "title": "Latest Evaluation Claim",
    "claim": "The latest completed evaluation work now has two layers: the deterministic paired 100-row smoke still defines the strongest baseline result, and the local <code>h003_single_prompt_llm</code> path now runs quickly enough for 25-row smoke testing but remains extraction-fragile.",
    "evidence": "<table><thead><tr><th>Harness</th><th>Run</th><th>Exact</th><th>Monthly 15 pct</th><th>Pragmatic micro-F1</th><th>Purist micro-F1</th></tr></thead><tbody><tr><td><code>h002_multi_agent_verify</code></td><td><a href=\"../project_state/runs/20260424T144559Z_h002_multi_agent_verify_n100.json\">20260424T144559Z_h002_multi_agent_verify_n100.json</a></td><td>0.31</td><td>0.48</td><td>0.55</td><td>0.53</td></tr><tr><td><code>h001_single_pass</code></td><td><a href=\"../project_state/runs/20260424T144606Z_h001_single_pass_n100.json\">20260424T144606Z_h001_single_pass_n100.json</a></td><td>0.25</td><td>0.43</td><td>0.50</td><td>0.48</td></tr></tbody></table><p>The manifest index is <a href=\"../project_state/experiments/manifest.csv\">project_state/experiments/manifest.csv</a>. Session log: <a href=\"run_logs/20260424T144639Z_seizure_free_detection_expansion.md\">20260424T144639Z_seizure_free_detection_expansion.md</a>.</p><p>Current LLM smoke:</p><table><thead><tr><th>Harness</th><th>Run</th><th>Exact</th><th>Monthly 15 pct</th><th>Pragmatic micro-F1</th><th>Purist micro-F1</th><th>Invalid-output rate</th><th>Mean latency</th></tr></thead><tbody><tr><td><code>h003_single_prompt_llm</code></td><td><a href=\"../project_state/runs/20260424T171400Z_h003_single_prompt_llm_n5.json\">20260424T171400Z_h003_single_prompt_llm_n5.json</a></td><td>0.20</td><td>0.20</td><td>0.20</td><td>0.20</td><td>0.80</td><td>52.9 s</td></tr><tr><td><code>h003_single_prompt_llm</code></td><td><a href=\"../project_state/runs/20260424T180607Z_h003_single_prompt_llm_n5.json\">20260424T180607Z_h003_single_prompt_llm_n5.json</a></td><td>0.40</td><td>0.40</td><td>0.40</td><td>0.40</td><td>0.40</td><td>0.95 s</td></tr><tr><td><code>h003_single_prompt_llm</code></td><td><a href=\"../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json\">20260424T180629Z_h003_single_prompt_llm_n25.json</a></td><td>0.20</td><td>0.28</td><td>0.36</td><td>0.32</td><td>0.28</td><td>1.29 s</td></tr></tbody></table>",
    "uncertainty": "<p>The deterministic 100-row comparison is still a smoke test. The new <code>h003</code> 25-row result is a usable local-model smoke, but it is not yet a credible comparison baseline because <code>unknown</code> and <code>no seizure frequency reference</code> predictions dominate.</p>",
    "next": "<p>The 25-row <code>h003</code> abstentions are classified into seven families in <a href=\"run_logs/20260425T081533Z_h003_abstention_classification.md\">run_logs/20260425T081533Z_h003_abstention_classification.md</a>: 9 of 15 real abstention-errors are window/aggregation, 4 are cluster-shape, 2 are NS-vs-no-reference, and 2 are qualitative-frequency phrasings. Intervention 1 (six worked label exemplars in <code>system_prompt()</code>) is now landed; the next LLM-runtime session should rerun <code>h003</code> on the same 25-row slice and re-classify the remaining abstentions before considering intervention 2.</p>"
  },
  "reviewRisks": [
    {
      "title": "Evaluation confidence limit",
      "detail": "The deterministic 100-row comparison is still a smoke test. The new <code>h003</code> 25-row result is a usable local-model smoke, but it is not yet a credible comparison baseline because <code>unknown</code> and <code>no seizure frequency reference</code> predictions dominate.",
      "tone": "warning"
    },
    {
      "title": "Current delivery risk",
      "detail": "The first n=5 smoke has invalid-output rate 0.80 and mean latency about 52.9 seconds, so the prompt/schema path is not yet strong enough for a 25-50 row comparison.",
      "tone": "review-needed"
    },
    {
      "title": "Governance boundary",
      "detail": "Maintain the no-raw-real-text rule for logs, prompts, screenshots, run records, and dashboard artifacts.",
      "tone": "info"
    }
  ],
  "stats": [
    {
      "label": "Claims",
      "value": 5
    },
    {
      "label": "Milestones",
      "value": 25
    },
    {
      "label": "Sessions",
      "value": 6
    },
    {
      "label": "Threads",
      "value": 5
    },
    {
      "label": "Artifacts",
      "value": 32
    },
    {
      "label": "Decisions",
      "value": 7
    }
  ],
  "sources": [
    {
      "label": "current_state.md",
      "href": "current_state.md"
    },
    {
      "label": "milestones.md",
      "href": "milestones.md"
    },
    {
      "label": "active_threads.md",
      "href": "active_threads.md"
    },
    {
      "label": "artifact_registry.md",
      "href": "artifact_registry.md"
    },
    {
      "label": "decisions.md",
      "href": "decisions.md"
    }
  ],
  "sourceFreshness": [
    {
      "label": "current_state.md",
      "updated": "2026-04-26"
    },
    {
      "label": "milestones.md",
      "updated": "2026-04-24"
    },
    {
      "label": "active_threads.md",
      "updated": "2026-04-26"
    },
    {
      "label": "artifact_registry.md",
      "updated": "2026-04-24"
    },
    {
      "label": "decisions.md",
      "updated": "2026-04-24"
    }
  ],
  "claims": [
    {
      "title": "Project Snapshot",
      "claim": "The repository is now in early Phase A of the dissertation: a local LLM runtime is live, the first single-prompt LLM harness exists, and the main blocker has shifted from runtime/schema setup to extraction reliability and abstention behaviour.",
      "evidence": "<ul><li>Project question and objectives are defined in <a href=\"project_specification.md\">project_specification.md</a>.</li><li>The operating research posture is defined in <a href=\"research_program.md\">research_program.md</a>.</li><li>Deterministic <code>single</code> and <code>multi</code> harnesses are registered in <a href=\"../project_state/harnesses/README.md\">project_state/harnesses/README.md</a>.</li><li>A first 25-row LLM-backed smoke run now exists at <a href=\"../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json\">20260424T180629Z_h003_single_prompt_llm_n25.json</a>.</li><li>The Evidence Notebook direction for project visibility is selected in <a href=\"agent_visibility_plan.md\">agent_visibility_plan.md</a>.</li><li>Phase 1 project-state pages and the Phase 2 session logging convention now exist under <code>docs/</code> and <code>docs/run_logs/</code>.</li></ul>",
      "uncertainty": "<p>The current LLM path is only at smoke-test maturity. Ollama/Qwen now returns fast structured or schema-near outputs, but <code>h003</code> still over-abstains on many rows and remains below the deterministic baselines.</p>",
      "next": "<p>Keep iteration narrow: reduce <code>h003</code> over-abstention on cluster, seizure-free, and windowed frequency cases before starting <code>h004</code>. Intervention 1 from <a href=\"run_logs/20260425T081533Z_h003_abstention_classification.md\">run_logs/20260425T081533Z_h003_abstention_classification.md</a> is now landed in <code>system_prompt()</code> (see <a href=\"run_logs/20260426T081829Z_h003_system_prompt_exemplars.md\">run_logs/20260426T081829Z_h003_system_prompt_exemplars.md</a>) but was not measured in-sandbox because no Ollama runtime was reachable. The next LLM-runtime session should rerun <code>h003_single_prompt_llm</code> on the same 25-row slice and re-classify any remaining abstentions before deciding whether to proceed to intervention 2.</p>"
    },
    {
      "title": "Visibility Claim",
      "claim": "The Evidence Notebook layer now has canonical state pages, a repeatable session logging convention, a generated local dashboard, and backfilled session coverage for the pre-visibility foundation work.",
      "evidence": "<ul><li>Canonical state pages: <a href=\"milestones.md\">milestones.md</a>, <a href=\"active_threads.md\">active_threads.md</a>, <a href=\"decisions.md\">decisions.md</a>, and <a href=\"artifact_registry.md\">artifact_registry.md</a>.</li><li>Session logging convention: <a href=\"run_logs/README.md\">run_logs/README.md</a>.</li><li>Session log template: <a href=\"run_logs/session_log_template.md\">run_logs/session_log_template.md</a>.</li><li>Optional companion schema and template: <a href=\"run_logs/session_log_companion_schema.json\">session_log_companion_schema.json</a>, <a href=\"run_logs/session_log_companion_template.json\">session_log_companion_template.json</a>.</li><li>Backfilled historical logs: <a href=\"run_logs/20260424T075111Z_initial_scaffold.md\">20260424T075111Z_initial_scaffold.md</a>, <a href=\"run_logs/20260424T084000Z_harness_protocol_and_smoke_runs.md\">20260424T084000Z_harness_protocol_and_smoke_runs.md</a>, <a href=\"run_logs/20260424T085900Z_candidate_retrieval_iteration.md\">20260424T085900Z_candidate_retrieval_iteration.md</a>.</li><li>Deployable notebook site: <a href=\"../site/index.html\">site/index.html</a> with static assets at <a href=\"../site/assets/\">site/assets/</a>.</li><li>Dashboard generator: <a href=\"../src/epilepsy_agents/visibility/\">src/epilepsy_agents/visibility/</a>.</li></ul>",
      "uncertainty": "<p>The dashboard is a static generated artifact. The new historical logs are reconstructed from repo evidence rather than written contemporaneously, so they are faithful summaries but not verbatim session notes.</p>",
      "next": "<p>Regenerate the dashboard after substantial updates to project-state docs or session logs, then proceed to the first curated Phase 4 visual artifact.</p>"
    },
    {
      "title": "Latest Evaluation Claim",
      "claim": "The latest completed evaluation work now has two layers: the deterministic paired 100-row smoke still defines the strongest baseline result, and the local <code>h003_single_prompt_llm</code> path now runs quickly enough for 25-row smoke testing but remains extraction-fragile.",
      "evidence": "<table><thead><tr><th>Harness</th><th>Run</th><th>Exact</th><th>Monthly 15 pct</th><th>Pragmatic micro-F1</th><th>Purist micro-F1</th></tr></thead><tbody><tr><td><code>h002_multi_agent_verify</code></td><td><a href=\"../project_state/runs/20260424T144559Z_h002_multi_agent_verify_n100.json\">20260424T144559Z_h002_multi_agent_verify_n100.json</a></td><td>0.31</td><td>0.48</td><td>0.55</td><td>0.53</td></tr><tr><td><code>h001_single_pass</code></td><td><a href=\"../project_state/runs/20260424T144606Z_h001_single_pass_n100.json\">20260424T144606Z_h001_single_pass_n100.json</a></td><td>0.25</td><td>0.43</td><td>0.50</td><td>0.48</td></tr></tbody></table><p>The manifest index is <a href=\"../project_state/experiments/manifest.csv\">project_state/experiments/manifest.csv</a>. Session log: <a href=\"run_logs/20260424T144639Z_seizure_free_detection_expansion.md\">20260424T144639Z_seizure_free_detection_expansion.md</a>.</p><p>Current LLM smoke:</p><table><thead><tr><th>Harness</th><th>Run</th><th>Exact</th><th>Monthly 15 pct</th><th>Pragmatic micro-F1</th><th>Purist micro-F1</th><th>Invalid-output rate</th><th>Mean latency</th></tr></thead><tbody><tr><td><code>h003_single_prompt_llm</code></td><td><a href=\"../project_state/runs/20260424T171400Z_h003_single_prompt_llm_n5.json\">20260424T171400Z_h003_single_prompt_llm_n5.json</a></td><td>0.20</td><td>0.20</td><td>0.20</td><td>0.20</td><td>0.80</td><td>52.9 s</td></tr><tr><td><code>h003_single_prompt_llm</code></td><td><a href=\"../project_state/runs/20260424T180607Z_h003_single_prompt_llm_n5.json\">20260424T180607Z_h003_single_prompt_llm_n5.json</a></td><td>0.40</td><td>0.40</td><td>0.40</td><td>0.40</td><td>0.40</td><td>0.95 s</td></tr><tr><td><code>h003_single_prompt_llm</code></td><td><a href=\"../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json\">20260424T180629Z_h003_single_prompt_llm_n25.json</a></td><td>0.20</td><td>0.28</td><td>0.36</td><td>0.32</td><td>0.28</td><td>1.29 s</td></tr></tbody></table>",
      "uncertainty": "<p>The deterministic 100-row comparison is still a smoke test. The new <code>h003</code> 25-row result is a usable local-model smoke, but it is not yet a credible comparison baseline because <code>unknown</code> and <code>no seizure frequency reference</code> predictions dominate.</p>",
      "next": "<p>The 25-row <code>h003</code> abstentions are classified into seven families in <a href=\"run_logs/20260425T081533Z_h003_abstention_classification.md\">run_logs/20260425T081533Z_h003_abstention_classification.md</a>: 9 of 15 real abstention-errors are window/aggregation, 4 are cluster-shape, 2 are NS-vs-no-reference, and 2 are qualitative-frequency phrasings. Intervention 1 (six worked label exemplars in <code>system_prompt()</code>) is now landed; the next LLM-runtime session should rerun <code>h003</code> on the same 25-row slice and re-classify the remaining abstentions before considering intervention 2.</p>"
    },
    {
      "title": "Data And Governance Claim",
      "claim": "The current development environment is safe for synthetic-data iteration, while real King&#x27;s College Hospital letters remain a later governed evaluation stage.",
      "evidence": "<ul><li>Synthetic subset details are in <a href=\"project_specification.md\">project_specification.md</a>.</li><li>Real-data export boundaries are documented in <a href=\"real_data_governance.md\">real_data_governance.md</a>.</li><li>Run records store aggregate metrics, row indexes, labels, and safe error categories rather than raw clinical text.</li></ul>",
      "uncertainty": "<p>The full synthetic dataset and any real-data access are not yet part of the current local evaluation loop.</p>",
      "next": "<p>Maintain the no-raw-real-text rule for logs, prompts, screenshots, run records, and dashboard artifacts.</p>"
    },
    {
      "title": "Implementation Claim",
      "claim": "The local codebase already has the scaffolding needed for deterministic evaluation and future provider-backed extraction.",
      "evidence": "<ul><li><code>src/epilepsy_agents</code> contains package code for agents, labels, metrics, providers, schema, and CLI behavior.</li><li>Local runtime feasibility and provider architecture notes are recorded in <a href=\"local_model_feasibility.md\">local_model_feasibility.md</a>.</li><li>The standard session workflow is documented in <a href=\"typical_session_workflow.md\">typical_session_workflow.md</a>.</li></ul>",
      "uncertainty": "<p>The local runtime now works through Ollama, and <code>think: false</code> plus a completion cap makes <code>qwen3.5:4b</code> fast enough for short smoke runs. The remaining issue is extraction reliability, not provider availability.</p>",
      "next": "<p>Improve <code>h003</code> abstention behaviour on <code>qwen3.5:4b</code>, then compare whether <code>qwen3.5:9b</code> improves validity enough to justify the extra latency.</p>"
    }
  ],
  "milestones": [
    {
      "title": "Source materials and project frame",
      "status": "Complete",
      "outcome": "Dissertation question, objectives, data plan, methods, metrics, and risks are defined.",
      "evidence": "<a href=\"project_specification.md\">project_specification.md</a>, <a href=\"literature_review_map.md\">literature_review_map.md</a>, <a href=\"dissertation_scaffold.md\">dissertation_scaffold.md</a>",
      "risk": "Scope may change if full synthetic or real-data access differs from assumptions.",
      "next": "Keep the research question stable while harnesses mature."
    },
    {
      "title": "Repository scaffold",
      "status": "Complete",
      "outcome": "Python package, deterministic agents, CLI, metrics, label parser, tests, and initial docs exist.",
      "evidence": "<a href=\"development_log.md\">development_log.md</a>, <a href=\"../pyproject.toml\">pyproject.toml</a>, <a href=\"../tests\">tests</a>",
      "risk": "Deterministic code is a baseline, not the final LLM-backed system.",
      "next": "Preserve deterministic comparability while adding providers."
    },
    {
      "title": "Synthetic subset loaded",
      "status": "Complete",
      "outcome": "The 1,500-row synthetic subset is available for local evaluation, with <code>row_ok</code> filtering used by default.",
      "evidence": "<a href=\"project_specification.md\">project_specification.md</a>, <a href=\"../synthetic_data_subset_1500.json\">synthetic_data_subset_1500.json</a>",
      "risk": "The full synthetic dataset is not yet integrated.",
      "next": "Keep data ingestion compatible with a future full-dataset drop-in."
    },
    {
      "title": "Evaluation harness",
      "status": "Complete",
      "outcome": "Metrics cover exact labels, monthly-rate tolerance, pragmatic classes, and purist classes.",
      "evidence": "<a href=\"evaluation_protocol.md\">evaluation_protocol.md</a>, <a href=\"../src/epilepsy_agents/metrics.py\">src/epilepsy_agents/metrics.py</a>",
      "risk": "Evidence support and invalid-output metrics need more importance once LLM output is active.",
      "next": "Add provider-backed output validation and evidence-support checks (see M-A2, M-B1)."
    },
    {
      "title": "Harness experiment protocol",
      "status": "Complete",
      "outcome": "Runs are recorded under <code>project_state/runs/</code> and indexed in a manifest.",
      "evidence": "<a href=\"harness_experiment_protocol.md\">harness_experiment_protocol.md</a>, <a href=\"../project_state/experiments/manifest.csv\">project_state/experiments/manifest.csv</a>",
      "risk": "Some run records are from smoke tests and should not be overinterpreted.",
      "next": "Continue fixed-budget paired comparisons."
    },
    {
      "title": "Initial paired smoke evaluations",
      "status": "Complete",
      "outcome": "<code>single</code> and <code>multi</code> deterministic baselines have 20-row and 100-row paired synthetic records.",
      "evidence": "<a href=\"../project_state/runs/20260424T144559Z_h002_multi_agent_verify_n100.json\">20260424T144559Z_h002_multi_agent_verify_n100.json</a>, <a href=\"../project_state/runs/20260424T144606Z_h001_single_pass_n100.json\">20260424T144606Z_h001_single_pass_n100.json</a>",
      "risk": "Deterministic results are the floor, not the study.",
      "next": "Freeze deterministic tuning (see <a href=\"decisions.md\">D007</a>) and move to Phase A."
    },
    {
      "title": "Seizure-free detection expansion",
      "status": "Complete",
      "outcome": "Deterministic extractor now covers numeric, qualitative, unit-only, and &quot;since&quot;/present-tense seizure-free phrasings; multi exact 0.20-&gt;0.31 and NS F1 0.26-&gt;0.82 on the paired 100-row smoke.",
      "evidence": "<a href=\"../src/epilepsy_agents/agents.py\">src/epilepsy_agents/agents.py</a>, <a href=\"../tests/test_agents.py\">tests/test_agents.py</a>, <a href=\"../project_state/runs/20260424T144559Z_h002_multi_agent_verify_n100.json\">20260424T144559Z_h002_multi_agent_verify_n100.json</a>, <a href=\"../project_state/runs/20260424T144606Z_h001_single_pass_n100.json\">20260424T144606Z_h001_single_pass_n100.json</a>, <a href=\"run_logs/20260424T144639Z_seizure_free_detection_expansion.md\">20260424T144639Z_seizure_free_detection_expansion.md</a>",
      "risk": "NS precision 0.73 on multi; residual regex-tuning has diminishing returns.",
      "next": "Do not pursue further deterministic regex expansion (see <a href=\"decisions.md\">D007</a>)."
    },
    {
      "title": "Local model feasibility",
      "status": "Complete",
      "outcome": "Hardware, runtime options, candidate model tiers, and provider requirements are documented.",
      "evidence": "<a href=\"local_model_feasibility.md\">local_model_feasibility.md</a>",
      "risk": "A working runtime still needs prompt and schema tuning before it becomes a useful baseline.",
      "next": "Use the live Ollama path to mature M-A2."
    },
    {
      "title": "Visibility Phase 1: project-state layer",
      "status": "Complete",
      "outcome": "Canonical Evidence Notebook pages exist for current state, milestones, active threads, decisions, and artifacts.",
      "evidence": "<a href=\"agent_visibility_plan.md\">agent_visibility_plan.md</a>, <a href=\"current_state.md\">current_state.md</a>, <a href=\"active_threads.md\">active_threads.md</a>, <a href=\"decisions.md\">decisions.md</a>, <a href=\"artifact_registry.md\">artifact_registry.md</a>",
      "risk": "Pages are manually maintained.",
      "next": "Update at the end of substantial sessions."
    },
    {
      "title": "Visibility Phase 2: session logging",
      "status": "Complete",
      "outcome": "Session logging has naming rules, required sections, status labels, evidence rules, privacy rules, a template, optional JSON companion files, and a first historical backfill.",
      "evidence": "<a href=\"run_logs/README.md\">run_logs/README.md</a>, <a href=\"run_logs/session_log_template.md\">session_log_template.md</a>, <a href=\"run_logs/session_log_companion_schema.json\">session_log_companion_schema.json</a>",
      "risk": "Backfilled notes are reconstructions.",
      "next": "Use the convention prospectively."
    },
    {
      "title": "Visibility Phase 3: local dashboard",
      "status": "Complete",
      "outcome": "A generated static Evidence Notebook dashboard renders current claims, milestones, recent sessions, active threads, artifacts, and decisions.",
      "evidence": "<a href=\"../site/index.html\">site/index.html</a>, <a href=\"../src/epilepsy_agents/visibility/\">src/epilepsy_agents/visibility/</a>, <a href=\"../tests/test_visibility.py\">tests/test_visibility.py</a>",
      "risk": "Dashboard regenerates manually.",
      "next": "Regenerate with <code>epilepsy-agents notebook</code> after substantial state updates."
    },
    {
      "title": "Historical notebook backfill",
      "status": "Complete",
      "outcome": "Reconstructed records exist for the initial scaffold, harness protocol and first paired smoke runs, and the candidate retrieval iteration.",
      "evidence": "<a href=\"run_logs/20260424T075111Z_initial_scaffold.md\">20260424T075111Z_initial_scaffold.md</a>, <a href=\"run_logs/20260424T084000Z_harness_protocol_and_smoke_runs.md\">20260424T084000Z_harness_protocol_and_smoke_runs.md</a>, <a href=\"run_logs/20260424T085900Z_candidate_retrieval_iteration.md\">20260424T085900Z_candidate_retrieval_iteration.md</a>",
      "risk": "Backfills are reconstructions, not contemporaneous notes.",
      "next": "Keep future session logs contemporaneous."
    },
    {
      "title": "M-A1 Local runtime live",
      "status": "Complete",
      "outcome": "A local Ollama server is running and responds through <code>src/epilepsy_agents/providers.py</code>; <code>provider-smoke</code> succeeds end to end against <code>qwen3.5:4b</code>.",
      "evidence": "<a href=\"local_model_feasibility.md\">local_model_feasibility.md</a>, <a href=\"../src/epilepsy_agents/providers.py\">src/epilepsy_agents/providers.py</a>, <a href=\"../src/epilepsy_agents/cli.py\">src/epilepsy_agents/cli.py</a>, <a href=\"run_logs/20260424T160537Z_local_provider_smoke_path.md\">20260424T160537Z_local_provider_smoke_path.md</a>",
      "risk": "The successful runtime is currently Ollama-specific rather than a broader runtime bake-off, and latency may still constrain larger-slice experiments.",
      "next": "Use the live Ollama path as the default Phase A runtime and focus on h003 output quality."
    },
    {
      "title": "M-A2 h003 single-prompt LLM smoke",
      "status": "In progress",
      "outcome": "<code>h003_single_prompt_llm</code> now exists and has produced a first local run record with JSON-schema validation, retries, latency, and token metadata.",
      "evidence": "<a href=\"../scripts/run_harness_experiment.py\">scripts/run_harness_experiment.py</a>, <a href=\"../src/epilepsy_agents/llm_pipeline.py\">src/epilepsy_agents/llm_pipeline.py</a>, <a href=\"../project_state/harnesses/README.md\">project_state/harnesses/README.md</a>, <a href=\"../project_state/runs/20260424T171400Z_h003_single_prompt_llm_n5.json\">20260424T171400Z_h003_single_prompt_llm_n5.json</a>",
      "risk": "The first n=5 smoke has invalid-output rate 0.80 and mean latency about 52.9 seconds, so the prompt/schema path is not yet strong enough for a 25-50 row comparison.",
      "next": "Inspect the four <code>unknown</code> outputs, tune prompt/schema behavior, and rerun h003 on a 25-row slice."
    },
    {
      "title": "M-A3 h004 multi-agent LLM pipeline",
      "status": "Planned",
      "outcome": "Role-separated LLM pipeline mirroring deterministic <code>multi</code>: section/timeline, extractor, verifier, aggregator, each with its own prompt and schema. Produce first paired <code>h003</code> vs <code>h004</code> n=100 synthetic record at matched budgets.",
      "evidence": "<a href=\"../prompts/agent_roles.md\">prompts/agent_roles.md</a>, <a href=\"../project_state/harnesses/README.md\">project_state/harnesses/README.md</a>",
      "risk": "Token/call budget parity must be measured, not assumed.",
      "next": "Build h004 on top of h003 provider plumbing and run first paired n=100 smoke."
    },
    {
      "title": "M-B1 Verification with evidence requirement",
      "status": "Planned",
      "outcome": "Verifier rejects extractor outputs lacking evidence-span support. Measure change in pragmatic micro-F1, purist micro-F1, evidence support rate, and invalid-output rate vs. h004 without verification.",
      "evidence": "<a href=\"project_specification.md\">project_specification.md</a>, <a href=\"evaluation_protocol.md\">evaluation_protocol.md</a>",
      "risk": "Strict verification can over-abstain; tradeoff must be read on the Pareto frontier (<a href=\"decisions.md\">D003</a>).",
      "next": "Add verifier prompt once h004 is stable."
    },
    {
      "title": "M-B2 h005 self-consistency",
      "status": "Planned",
      "outcome": "Sample k=3 then k=5, aggregate by agreement. Compare at matched call budget and matched token budget against h003 and against h004 without self-consistency.",
      "evidence": "<a href=\"harness_experiment_protocol.md\">harness_experiment_protocol.md</a>, <a href=\"research_program.md\">research_program.md</a>",
      "risk": "Cost scaling with k; sampling variance on small synthetic slices.",
      "next": "Add sampling controller to the provider adapter after M-B1."
    },
    {
      "title": "M-B3 Evidence-required vs answer-only ablation",
      "status": "Planned",
      "outcome": "Fixed paired comparison of h004 with evidence-required schema versus answer-only schema. Report evidence support, invalid-output rate, and class F1.",
      "evidence": "<a href=\"evaluation_protocol.md\">evaluation_protocol.md</a>",
      "risk": "Schema changes touch both prompt and metrics code.",
      "next": "Run after M-B2 on the same synthetic slice."
    },
    {
      "title": "M-C1 Full synthetic corpus run",
      "status": "Planned",
      "outcome": "Rerun the Pareto comparison on the full synthetic dataset once released, with confidence intervals.",
      "evidence": "<a href=\"project_specification.md\">project_specification.md</a>",
      "risk": "Dataset release timing is outside our control.",
      "next": "Keep the loader drop-in compatible; ingest when Gan et al. publish the full set."
    },
    {
      "title": "M-C2 Gan et al. fine-tuned baseline comparison",
      "status": "Planned",
      "outcome": "On the same synthetic slice, compare our best Pareto candidate against the published fine-tuned baseline (reported numbers or released model outputs).",
      "evidence": "<a href=\"project_specification.md\">project_specification.md</a>, <a href=\"literature_review_map.md\">literature_review_map.md</a>",
      "risk": "Evaluation setup must be comparable; metric cuts may differ.",
      "next": "Request or reproduce baseline numbers after Phase B."
    },
    {
      "title": "M-C3 Budget-matched closed-provider comparison",
      "status": "Planned",
      "outcome": "Matched call/token budgets across one local model and one closed provider, synthetic-only per <a href=\"decisions.md\">D004</a>.",
      "evidence": "<a href=\"real_data_governance.md\">real_data_governance.md</a>, <a href=\"decisions.md\">decisions.md</a>",
      "risk": "Cost; provider variance; no real data.",
      "next": "After Phase B, decide if an external reference point materially strengthens the dissertation."
    },
    {
      "title": "M-D1 Real KCH evaluation inside approved environment",
      "status": "Blocked by governance",
      "outcome": "Evaluate best Pareto candidate on real KCH letters inside the approved environment; export only aggregate metrics and de-identified error-category counts.",
      "evidence": "<a href=\"real_data_governance.md\">real_data_governance.md</a>, <a href=\"decisions.md\">decisions.md</a>",
      "risk": "Governance approval, environment availability, time budget; strict no-raw-text export.",
      "next": "Revisit only when Phase B/C synthetic results and governance both support it."
    },
    {
      "title": "M-E1 First dissertation draft",
      "status": "Planned",
      "outcome": "Methods, synthetic results, error taxonomy, and discussion fitted to the 8-page conference template (~5,000 words).",
      "evidence": "<a href=\"dissertation_scaffold.md\">dissertation_scaffold.md</a>, <a href=\"../README.md\">README.md</a>",
      "risk": "Results from Phase B must exist before drafting results.",
      "next": "Begin outlining methods and results as Phase B produces numbers."
    },
    {
      "title": "M-E2 Curated visual artifacts",
      "status": "Planned",
      "outcome": "Architecture poster, dataset/evaluation diagram, agent-role diagram, milestone timeline, local-first hospital deployment diagram, evidence-grounding figure.",
      "evidence": "<a href=\"visual_artifacts_direction.md\">visual_artifacts_direction.md</a>, <a href=\"artifact_registry.md\">artifact_registry.md</a>",
      "risk": "Visuals risk being decorative if unmoored from results.",
      "next": "Generate the first architecture poster and a phase-aware milestone timeline."
    },
    {
      "title": "M-E3 Final paper and reproducibility guide",
      "status": "Planned",
      "outcome": "Submit-ready dissertation, commands-to-reproduce section, and a reproducible run export.",
      "evidence": "<a href=\"../README.md\">README.md</a>, <a href=\"evaluation_protocol.md\">evaluation_protocol.md</a>",
      "risk": "Scope creep if Phase D is attempted too late.",
      "next": "Enter after M-E1 draft cycle."
    }
  ],
  "sessions": [
    {
      "title": "Session Log: h003 system prompt worked exemplars (intervention 1)",
      "date": "2026-04-26",
      "objective": "Apply intervention 1 from the 2026-04-25 abstention classification (six worked label exemplars in <code>system_prompt()</code>) so the next available LLM-runtime session can rerun <code>h003</code> on the 25-row slice for a paired comparison.",
      "outcome": "<p><code>system_prompt()</code> in <a href=\"../../src/epilepsy_agents/structured_schema.py\">structured_schema.py</a> now appends six worked phrasing -&gt; label exemplars covering each abstention failure family identified on 2026-04-25:</p><ul><li>explicit rate (<code>&#x27;two events each week&#x27; -&gt; &#x27;2 per week&#x27;</code>),</li><li>multi-month window (<code>&#x27;six episodes over the past seven months&#x27; -&gt; &#x27;6 per 7 month&#x27;</code>),</li><li>single-interval window (<code>&#x27;roughly one seizure every six weeks&#x27; -&gt; &#x27;1 per 6 week&#x27;</code>),</li><li>cluster days plus per-cluster (<code>&#x27;two cluster days per month, around six seizures per cluster&#x27; -&gt; &#x27;2 cluster per month, 6 per cluster&#x27;</code>),</li><li>seizure-free (<code>&#x27;seizure free for several months since the last review&#x27; -&gt; &#x27;seizure free for multiple month&#x27;</code>),</li><li>qualitative high-frequency (<code>&#x27;multiple seizures per week, exact count not given&#x27; -&gt; &#x27;multiple per week&#x27;</code>).</li></ul><p>Phrasings on the left of each <code>-&gt;</code> are synthetic-style paraphrases authored for the prompt rather than copied from any letter. The prompt still starts with <code>/no_think</code> and still requires schema-conformant JSON-only output supported by quoted evidence, so the existing <code>test_system_prompt_disables_qwen_thinking_mode</code> and the surrounding <code>SinglePromptLLMPipelineTests</code> checks continue to pass.</p><p>The change only affects the <code>h003_single_prompt_llm</code> pipeline path; the deterministic <code>h001_single_pass</code> and <code>h002_multi_agent_verify</code> harnesses do not use <code>system_prompt()</code> and so are unchanged. No run records, manifest rows, or schema fields were modified, and no new experiment was added to <a href=\"../../project_state/experiments/manifest.csv\">project_state/experiments/manifest.csv</a>.</p><p>The empirical paired rerun on the 25-row slice could not be executed in this session because no Ollama runtime is available in the current sandbox (<code>curl http://localhost:11434/api/tags</code> returns connection refused, and <code>ollama</code> is not on <code>$PATH</code>). The change is therefore landed but unmeasured; the next LLM-runtime session should run the paired comparison.</p><p>### Pre-change parser round-trip check</p><p>Per the 2026-04-25 handoff step 1, the five labels named in the next-action list, plus the <code>2 per week</code> and <code>6 per 7 month</code> exemplars, all round-trip cleanly through <code>parse_label</code> in <a href=\"../../src/epilepsy_agents/labels.py\">labels.py</a>:</p><table><thead><tr><th>Label</th><th>monthly_rate</th><th>pragmatic</th><th>purist</th><th>kind</th></tr></thead><tbody><tr><td><code>multiple per week</code></td><td>13.04</td><td>frequent</td><td>(1/W,1/D)</td><td>rate</td></tr><tr><td><code>multiple per day</code></td><td>91.31</td><td>frequent</td><td>&gt;=1/D</td><td>rate</td></tr><tr><td><code>1 per 4 day</code></td><td>7.61</td><td>frequent</td><td>(1/W,1/D)</td><td>rate</td></tr><tr><td><code>1 per 6 week</code></td><td>0.72</td><td>infrequent</td><td>(1/6M,1/M)</td><td>rate</td></tr><tr><td><code>2 cluster per month, 6 per cluster</code></td><td>12.00</td><td>frequent</td><td>(1/W,1/D)</td><td>cluster</td></tr><tr><td><code>6 per 7 month</code></td><td>0.86</td><td>infrequent</td><td>(1/6M,1/M)</td><td>rate</td></tr><tr><td><code>2 per week</code></td><td>8.70</td><td>frequent</td><td>(1/W,1/D)</td><td>rate</td></tr><tr><td><code>seizure free for multiple month</code></td><td>0.00</td><td>NS</td><td>NS</td><td>seizure_free</td></tr></tbody></table><p>This means none of the new exemplar labels would silently fall through to <code>unknown</code> if a model emits them verbatim.</p>",
      "outcomePlain": "system_prompt() in structured_schema.py now appends six worked phrasing -> label exemplars covering each abstention failure family identified on 2026-04-25: - explicit rate ('two events each week' -> '2 per week'), - multi-month window ('six episodes over the past seven months' -> '6 per 7 month'), - single-interval window ('roughly one seizure every six weeks' -> '1 per 6 week'), - cluster days plus per-cluster ('two cluster days per month, around six seizures per cluster' -> '2 cluster per month, 6 per cluster'), - seizure-free ('seizure free for several months since the last review' -> 'seizure free for multiple month'), - qualitative high-frequency ('multiple seizures per week, exact count not given' -> 'multiple per week'). Phrasings on the left of each -> are synthetic-style paraphrases authored for the prompt rather than copied from any letter. The prompt still starts with /no_think and still requires schema-conformant JSON-only output supported by quoted evidence, so the existing test_system_prompt_disables_qwen_thinking_mode and the surrounding SinglePromptLLMPipelineTests checks continue to pass. The change only affects the h003_single_prompt_llm pipeline path; the deterministic h001_single_pass and h002_multi_agent_verify harnesses do not use system_prompt() and so are unchanged. No run records, manifest rows, or schema fields were modified, and no new experiment was added to project_state/experiments/manifest.csv. The empirical paired rerun on the 25-row slice could not be executed in this session because no Ollama runtime is available in the current sandbox (curl http://localhost:11434/api/tags returns connection refused, and ollama is not on $PATH). The change is therefore landed but unmeasured; the next LLM-runtime session should run the paired comparison. ### Pre-change parser round-trip check Per the 2026-04-25 handoff step 1, the five labels named in the next-action list, plus the 2 per week and 6 per 7 month exemplars, all round-trip cleanly through parse_label in labels.py: | Label | monthly_rate | pragmatic | purist | kind | | --- | ---: | --- | --- | --- | | multiple per week | 13.04 | frequent | (1/W,1/D) | rate | | multiple per day | 91.31 | frequent | >=1/D | rate | | 1 per 4 day | 7.61 | frequent | (1/W,1/D) | rate | | 1 per 6 week | 0.72 | infrequent | (1/6M,1/M) | rate | | 2 cluster per month, 6 per cluster | 12.00 | frequent | (1/W,1/D) | cluster | | 6 per 7 month | 0.86 | infrequent | (1/6M,1/M) | rate | | 2 per week | 8.70 | frequent | (1/W,1/D) | rate | | seizure free for multiple month | 0.00 | NS | NS | seizure_free | This means none of the new exemplar labels would silently fall through to unknown if a model emits them verbatim.",
      "evidence": "<ul><li>Files changed: <a href=\"../../src/epilepsy_agents/structured_schema.py\">src/epilepsy_agents/structured_schema.py</a> (only <code>system_prompt()</code>); this session log.</li><li>Run records consulted:</li><li><a href=\"../../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json\">project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json</a> (the n=25 baseline this intervention targets).</li><li><a href=\"20260425T081533Z_h003_abstention_classification.md\">run_logs/20260425T081533Z_h003_abstention_classification.md</a> (defines intervention 1).</li><li>Tests or checks: <code>PYTHONPATH=src python -m unittest discover -s tests</code> -&gt; 38/38 pass on the post-edit working tree.</li><li>Generated artifacts: this session log only; no machine-readable companion.</li><li>Runtime probe: <code>curl -s -m 3 http://localhost:11434/api/tags</code> returns connection refused (exit 7); <code>ollama</code> not on <code>$PATH</code>. The LLM rerun is therefore deferred.</li></ul>",
      "uncertainty": "<ul><li>The expected lifts on window, cluster, and qualitative cases are reasoned from the 2026-04-25 family breakdown, not measured. Until a paired rerun on the same 25-row slice exists, the intervention&#x27;s effect on invalid-output rate, abstention count, and pragmatic micro-F1 remains a hypothesis.</li><li>The new exemplars may interact with <code>qwen3.5:4b</code>&#x27;s tendency toward verbatim copying. If the model starts echoing the exemplar phrasings into the <code>evidence</code> field, that would be a privacy-safe artefact (the phrasings are synthetic) but would inflate evidence-support metrics; the next session should spot-check evidence spans against letter text.</li><li>No deterministic paired smoke was rerun because the change does not touch <code>h001</code>/<code>h002</code> behaviour; the existing 100-row results in <a href=\"../../project_state/experiments/manifest.csv\">manifest.csv</a> remain the deterministic baseline.</li></ul>",
      "handoff": "<p>The next LLM-runtime session should:</p><p>1. Bring up Ollama with <code>qwen3.5:4b</code> (and <code>think: false</code> already wired into the pipeline). 2. Rerun <code>h003_single_prompt_llm</code> on the same 25-row <code>row_ok</code> slice used in <a href=\"../../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json\">20260424T180629Z_h003_single_prompt_llm_n25.json</a>, using <code>python scripts/run_harness_experiment.py --harness single_llm --limit 25 --description &quot;h003 worked-exemplar intervention 1 rerun&quot;</code> (or the equivalent LLM-harness invocation registered in <code>run_harness_experiment.py</code>). 3. Compare invalid-output rate, abstention count, and pragmatic micro-F1 against the 2026-04-24 baseline; classify any remaining abstentions back into the seven 2026-04-25 families. 4. Only if window and cluster cases improve but NS or qualitative cases remain, apply intervention 2 (NS-vs-no-reference rule in the user prompt in <code>llm_pipeline.py</code>) in a separate paired run.</p>",
      "decision": "blocked by local model/runtime setup.\n\nThe intervention is implemented and unit tests pass, but the paired empirical rerun that would justify a <code>keep this harness variant</code> or <code>reject this variant</code> decision requires a local Ollama runtime that is not present in this sandbox.",
      "href": "run_logs/20260426T081829Z_h003_system_prompt_exemplars.md",
      "tags": [
        "1 files changed",
        "tests run",
        "artifacts updated",
        "blocked by local model/runtime setup.\n\nThe intervention is implemented and unit tests pass, but the paired empirical rerun that would justify a `keep this harness variant` or `reject this variant` decision requires a local Ollama runtime that is not present in this sandbox."
      ],
      "filesChangedCount": 1,
      "checksRunCount": 1,
      "artifactsUpdatedCount": 1,
      "runEvidenceCount": 0,
      "hasDecision": true
    },
    {
      "title": "Session Log: h003 25-row abstention classification",
      "date": "2026-04-25",
      "objective": "Classify the 17 abstentions in the latest <code>h003_single_prompt_llm</code> 25-row smoke into the project error taxonomy and produce a narrow, ordered intervention list for the next LLM-iteration session.",
      "outcome": "<p>The 17 abstentions in <a href=\"../../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json\">20260424T180629Z_h003_single_prompt_llm_n25.json</a> now have a structured failure-family breakdown, and there is an ordered list of three narrow interventions to try in the next LLM-iteration session. Two of the 17 abstentions are revealed to be correct (gold also <code>unknown</code>), so the practical abstention-error count is 15.</p><p>No code, prompts, schema, or run records changed in this session. The unit-test suite still passes (38/38).</p><p>### Failure-family breakdown of the 17 abstentions</p><table><thead><tr><th>Family</th><th>Count</th><th>Predicted</th><th>Notes</th></tr></thead><tbody><tr><td><code>cluster</code></td><td>4</td><td>3x <code>unknown</code>, plus 1 partial</td><td>2 rows have explicit cluster-day counts (gold like <code>2 cluster per month, 6 per cluster</code>); 2 rows have <code>unknown, X per cluster</code> gold where pragmatic UNK was technically matched but the cluster annotation was lost.</td></tr><tr><td><code>window_month</code></td><td>4</td><td>2x <code>unknown</code>, 2x <code>no seizure frequency reference</code></td><td>Gold labels of the form <code>X per N month</code> with <code>N&gt;1</code>; letters describe seizures across multiple named months and require aggregation across the visible window.</td></tr><tr><td><code>seizure_free</code></td><td>2</td><td>2x <code>no seizure frequency reference</code></td><td>Gold is <code>seizure free for multiple month</code>; model collapses NS into &quot;no reference&quot;. This is the same failure mode the deterministic baselines fixed in the 2026-04-24 seizure-free expansion.</td></tr><tr><td><code>qualitative_multiple</code></td><td>2</td><td>2x <code>unknown</code></td><td>Letter says <code>several episodes per week</code> / <code>multiple seizures in past day</code>; gold is <code>multiple per week</code> / <code>multiple per day</code>. The schema permits these labels but the prompt does not surface them.</td></tr><tr><td><code>true_unknown</code></td><td>2</td><td>2x <code>unknown</code></td><td>Gold is also <code>unknown</code>; not actually errors. Pragmatic-class match was correct on both.</td></tr><tr><td><code>window_week</code></td><td>1</td><td>1x <code>unknown</code></td><td><code>Median inter-seizure interval ~ six weeks</code> -&gt; <code>1 per 6 week</code>.</td></tr><tr><td><code>window_day</code></td><td>1</td><td>1x <code>unknown</code></td><td><code>clusters every 4 days</code> -&gt; <code>1 per 4 day</code>.</td></tr><tr><td><code>other</code></td><td>1</td><td>1x <code>unknown</code></td><td><code>abs *monthly</code> (abbreviation) -&gt; <code>1 per month</code>.</td></tr></tbody></table><p>So of 15 real abstention-errors:</p><ul><li>9 (60 percent) are window/aggregation problems (4 multi-month windows, 2 cluster-day windows that need aggregation, 2 single-interval windows, 1 abbreviated monthly).</li><li>4 (27 percent) are cluster-shape problems (need to emit the <code>N cluster per month, M per cluster</code> form or its <code>unknown, M per cluster</code> partial variant).</li><li>2 (13 percent) are NS vs no-reference confusion (the seizure-free family).</li><li>2 (13 percent) are qualitative-frequency phrasings the prompt does not exemplify.</li></ul><p>(Counts overlap because cluster cases also need windowing.)</p><p>### Ordered intervention list for the next session</p><p>These are listed one-change-at-a-time per <a href=\"../research_program.md\">research_program.md</a>. The next LLM-iteration session should pick exactly one and rerun on the same 25-row slice for paired comparison.</p><p>1. **Add 6 worked label exemplars to <code>system_prompt()</code> in <a href=\"../../src/epilepsy_agents/structured_schema.py#L47-L58\">structured_schema.py</a>**, one per family above, all derived from synthetic-style phrasings rather than copied from the dataset:</p><ul><li>explicit rate (<code>2 per week</code>),</li><li>multi-month window (<code>6 per 7 month</code>),</li><li>single-interval window (<code>1 per 6 week</code>),</li><li>cluster days plus per-cluster (<code>2 cluster per month, 6 per cluster</code>),</li><li>seizure-free (<code>seizure free for multiple month</code>),</li><li>qualitative high-frequency (<code>multiple per week</code>).</li></ul><p>Expected effect: lifts the 9 window cases, the 4 cluster cases, and the 2 qualitative cases. Lowest-risk single change.</p><p>2. **Add an explicit NS-vs-no-reference rule to the user prompt in <a href=\"../../src/epilepsy_agents/llm_pipeline.py#L80-L93\">llm_pipeline.py</a>**: &quot;Use <code>seizure free for multiple month</code> when the letter states the patient is currently seizure-free; reserve <code>no seizure frequency reference</code> for letters with no seizure-related content at all.&quot; Expected effect: lifts the 2 NS cases and may reduce false <code>no seizure frequency reference</code> outputs more broadly. Hold this back until intervention 1 is measured, so the variables stay separated.</p><p>3. **Surface a candidate-span pre-filter** by re-using the deterministic <code>multi</code>-pipeline section/timeline retriever in <a href=\"../../src/epilepsy_agents/agents.py\">agents.py</a> to prepend a <code>Candidate spans:</code> block to the user prompt. This is more architectural and risks crossing into the planned <code>h004_multi_agent_llm</code> design boundary, so it should not be combined with intervention 1 or 2 in a single run.</p>",
      "outcomePlain": "The 17 abstentions in 20260424T180629Z_h003_single_prompt_llm_n25.json now have a structured failure-family breakdown, and there is an ordered list of three narrow interventions to try in the next LLM-iteration session. Two of the 17 abstentions are revealed to be correct (gold also unknown), so the practical abstention-error count is 15. No code, prompts, schema, or run records changed in this session. The unit-test suite still passes (38/38). ### Failure-family breakdown of the 17 abstentions | Family | Count | Predicted | Notes | | --- | ---: | --- | --- | | cluster | 4 | 3x unknown, plus 1 partial | 2 rows have explicit cluster-day counts (gold like 2 cluster per month, 6 per cluster); 2 rows have unknown, X per cluster gold where pragmatic UNK was technically matched but the cluster annotation was lost. | | window_month | 4 | 2x unknown, 2x no seizure frequency reference | Gold labels of the form X per N month with N>1; letters describe seizures across multiple named months and require aggregation across the visible window. | | seizure_free | 2 | 2x no seizure frequency reference | Gold is seizure free for multiple month; model collapses NS into \"no reference\". This is the same failure mode the deterministic baselines fixed in the 2026-04-24 seizure-free expansion. | | qualitative_multiple | 2 | 2x unknown | Letter says several episodes per week / multiple seizures in past day; gold is multiple per week / multiple per day. The schema permits these labels but the prompt does not surface them. | | true_unknown | 2 | 2x unknown | Gold is also unknown; not actually errors. Pragmatic-class match was correct on both. | | window_week | 1 | 1x unknown | Median inter-seizure interval ~ six weeks -> 1 per 6 week. | | window_day | 1 | 1x unknown | clusters every 4 days -> 1 per 4 day. | | other | 1 | 1x unknown | abs *monthly (abbreviation) -> 1 per month. | So of 15 real abstention-errors: - 9 (60 percent) are window/aggregation problems (4 multi-month windows, 2 cluster-day windows that need aggregation, 2 single-interval windows, 1 abbreviated monthly). - 4 (27 percent) are cluster-shape problems (need to emit the N cluster per month, M per cluster form or its unknown, M per cluster partial variant). - 2 (13 percent) are NS vs no-reference confusion (the seizure-free family). - 2 (13 percent) are qualitative-frequency phrasings the prompt does not exemplify. (Counts overlap because cluster cases also need windowing.) ### Ordered intervention list for the next session These are listed one-change-at-a-time per research_program.md. The next LLM-iteration session should pick exactly one and rerun on the same 25-row slice for paired comparison. 1. **Add 6 worked label exemplars to system_prompt() in structured_schema.py**, one per family above, all derived from synthetic-style phrasings rather than copied from the dataset: - explicit rate (2 per week), - multi-month window (6 per 7 month), - single-interval window (1 per 6 week), - cluster days plus per-cluster (2 cluster per month, 6 per cluster), - seizure-free (seizure free for multiple month), - qualitative high-frequency (multiple per week). Expected effect: lifts the 9 window cases, the 4 cluster cases, and the 2 qualitative cases. Lowest-risk single change. 2. **Add an explicit NS-vs-no-reference rule to the user prompt in llm_pipeline.py**: \"Use seizure free for multiple month when the letter states the patient is currently seizure-free; reserve no seizure frequency reference for letters with no seizure-related content at all.\" Expected effect: lifts the 2 NS cases and may reduce false no seizure frequency reference outputs more broadly. Hold this back until intervention 1 is measured, so the variables stay separated. 3. **Surface a candidate-span pre-filter** by re-using the deterministic multi-pipeline section/timeline retriever in agents.py to prepend a Candidate spans: block to the user prompt. This is more architectural and risks crossing into the planned h004_multi_agent_llm design boundary, so it should not be combined with intervention 1 or 2 in a single run.",
      "evidence": "<ul><li>Files changed: this session log only (no code, prompts, schema, manifest, or run records changed).</li><li>Run records consulted:</li><li><a href=\"../../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json\">project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json</a> (the n=25 smoke being analyzed).</li><li><a href=\"../../project_state/experiments/manifest.csv\">project_state/experiments/manifest.csv</a> for paired-baseline context.</li><li>Tests or checks: <code>PYTHONPATH=src python -m unittest discover -s tests</code> -&gt; 38/38 pass on commit b126cbe.</li><li>Generated artifacts: this session log only; no machine-readable companion.</li><li>Source-of-truth files for the proposal: <a href=\"../../src/epilepsy_agents/structured_schema.py\">structured_schema.py</a>, <a href=\"../../src/epilepsy_agents/llm_pipeline.py\">llm_pipeline.py</a>, <a href=\"../../src/epilepsy_agents/agents.py\">agents.py</a>.</li></ul>",
      "uncertainty": "<ul><li>The classification was done from gold labels and the dataset&#x27;s own <code>reference</code> field, not from the actual LLM completion text (which the run record deliberately does not store). It is possible some of the multi-month-window failures are caused by JSON-format issues rather than reasoning issues, but the same run had only 0.28 invalid-output rate so most of these abstentions were schema-valid <code>unknown</code>/<code>no seizure frequency reference</code> outputs.</li><li>This sandbox has no Ollama runtime, so the proposed prompt change cannot be measured here. The expected lifts above are reasoned, not empirical.</li><li>The <code>qualitative_multiple</code> and <code>window_day</code> interventions assume the parser in <a href=\"../../src/epilepsy_agents/labels.py\">labels.py</a> already accepts <code>multiple per week</code>, <code>multiple per day</code>, and <code>1 per 4 day</code>. This was not verified in this session and should be checked before the next LLM rerun.</li></ul>",
      "handoff": "<p>The next LLM-iteration session should:</p><p>1. Confirm <code>multiple per week</code>, <code>multiple per day</code>, <code>1 per 4 day</code>, <code>1 per 6 week</code>, and <code>2 cluster per month, 6 per cluster</code> round-trip cleanly through <code>parse_label</code>. 2. Apply intervention 1 above (6 worked exemplars in <code>system_prompt()</code>). 3. Rerun <code>h003_single_prompt_llm</code> on the same 25-row slice and compare invalid-output rate, abstention count, and pragmatic micro-F1 against the 2026-04-24 baseline. 4. Only if intervention 1 helps but NS and qualitative cases remain, add intervention 2 in a separate paired run.</p>",
      "decision": "documentation/visibility updated, no metric decision needed.",
      "href": "run_logs/20260425T081533Z_h003_abstention_classification.md",
      "tags": [
        "files changed",
        "tests run",
        "artifacts updated",
        "documentation/visibility updated, no metric decision needed."
      ],
      "filesChangedCount": 1,
      "checksRunCount": 1,
      "artifactsUpdatedCount": 1,
      "runEvidenceCount": 0,
      "hasDecision": true
    },
    {
      "title": "Evidence Notebook Design Generator Session",
      "date": "2026-04-24",
      "objective": "Port the Evidence Notebook design evolution sprint into the static dashboard generator so the upgraded interface survives regeneration.",
      "outcome": "<p>The Evidence Notebook design sprint is now generator-backed. The static dashboard generator renders compact inner headers, the four-part claim dossier, phase-aware timeline treatment, and a grouped artifact shelf with purpose, status, path, and intended use. The dashboard was regenerated from the updated generator.</p>",
      "outcomePlain": "The Evidence Notebook design sprint is now generator-backed. The static dashboard generator renders compact inner headers, the four-part claim dossier, phase-aware timeline treatment, and a grouped artifact shelf with purpose, status, path, and intended use. The dashboard was regenerated from the updated generator.",
      "evidence": "<ul><li>Files changed:</li><li><code>src/epilepsy_agents/visibility.py</code></li><li><code>docs/evidence_notebook.html</code></li><li><code>docs/run_logs/20260424T201418Z_evidence_notebook_design_generator.md</code></li><li>Run records: none; this was a visibility/dashboard design session.</li><li>Tests or checks:</li><li><code>python -m py_compile src\\epilepsy_agents\\visibility.py</code></li><li><code>$env:PYTHONPATH=&#x27;src&#x27;; python -m epilepsy_agents.cli notebook --out docs\\evidence_notebook.html --session-limit 6</code></li><li><code>$env:PYTHONPATH=&#x27;src&#x27;; python -c &quot;from pathlib import Path; from epilepsy_agents.visibility import build_dashboard; html = build_dashboard(Path(&#x27;.&#x27;), session_limit=6); assert &#x27;dossier-grid&#x27; in html and &#x27;artifact-shelf-item&#x27; in html and &#x27;timeline-next&#x27; in html and &#x27;viewMeta&#x27; in html; print(&#x27;build_dashboard generated upgraded notebook structures&#x27;)&quot;</code></li><li><code>node -e &quot;const fs=require(&#x27;fs&#x27;); const html=fs.readFileSync(&#x27;docs/evidence_notebook.html&#x27;,&#x27;utf8&#x27;); const scripts=[...html.matchAll(/&lt;script(?![^&gt;]*application\\/json)[^&gt;]*&gt;([\\s\\S]*?)&lt;\\/script&gt;/g)].map(m=&gt;m[1]); new Function(scripts.join(&#x27;\\n&#x27;)); console.log(&#x27;inline scripts parse ok&#x27;);&quot;</code></li><li>Generated artifacts:</li><li><code>docs/evidence_notebook.html</code></li></ul>",
      "uncertainty": "<p><code>uv run pytest tests\\test_visibility.py</code> could not be completed because the sandboxed <code>uv</code> run could not access its user Python cache, and the escalated retry was rejected by the approval system. The generator import/build checks and inline JavaScript parse passed, but the pytest suite should be rerun when the environment permits.</p>",
      "handoff": "<p>The next useful design pass is the Sessions and Decisions slice: make sessions a stronger expandable research ledger and make decisions more ADR-like with rationale, consequence, evidence, and governance markers visible in the first scan.</p>",
      "decision": "documentation/visibility updated, no metric decision needed.",
      "href": "run_logs/20260424T201418Z_evidence_notebook_design_generator.md",
      "tags": [
        "files changed",
        "tests run",
        "artifacts updated",
        "run evidence"
      ],
      "filesChangedCount": 4,
      "checksRunCount": 4,
      "artifactsUpdatedCount": 1,
      "runEvidenceCount": 1,
      "hasDecision": true
    },
    {
      "title": "Project Phase Re-scope",
      "date": "2026-04-24",
      "objective": "Restructure the core project-state documentation into explicit Phase A-E milestones so the dissertation&#x27;s critical path is visible at the top of every future session.",
      "outcome": "<p>The core project-state documentation now names five research phases with stable milestone IDs:</p><ul><li>Phase A: Stand up the LLM path (M-A1 Complete, M-A2 In progress, M-A3 Planned).</li><li>Phase B: Reliability interventions (M-B1 evidence-requiring verification, M-B2 self-consistency, M-B3 evidence-required vs answer-only ablation).</li><li>Phase C: Scale and external baselines (M-C1 full synthetic corpus, M-C2 Gan et al. fine-tuned baseline comparison, M-C3 optional budget-matched closed-provider comparison on synthetic).</li><li>Phase D: Locked-down real-data evaluation (M-D1, governance-gated and optional).</li><li>Phase E: Dissertation and packaging (M-E1 draft, M-E2 curated visuals, M-E3 final paper and reproducibility guide).</li></ul><p>Deterministic regex expansion is frozen per <a href=\"../decisions.md\">D007</a>; the deterministic harnesses stay as the reproducible offline floor per <a href=\"../decisions.md\">D002</a> but are no longer an active development target. The dissertation&#x27;s central question is answered primarily by Phase A-C work, not by further rule-based tuning.</p>",
      "outcomePlain": "The core project-state documentation now names five research phases with stable milestone IDs: - Phase A: Stand up the LLM path (M-A1 Complete, M-A2 In progress, M-A3 Planned). - Phase B: Reliability interventions (M-B1 evidence-requiring verification, M-B2 self-consistency, M-B3 evidence-required vs answer-only ablation). - Phase C: Scale and external baselines (M-C1 full synthetic corpus, M-C2 Gan et al. fine-tuned baseline comparison, M-C3 optional budget-matched closed-provider comparison on synthetic). - Phase D: Locked-down real-data evaluation (M-D1, governance-gated and optional). - Phase E: Dissertation and packaging (M-E1 draft, M-E2 curated visuals, M-E3 final paper and reproducibility guide). Deterministic regex expansion is frozen per D007; the deterministic harnesses stay as the reproducible offline floor per D002 but are no longer an active development target. The dissertation's central question is answered primarily by Phase A-C work, not by further rule-based tuning.",
      "evidence": "<ul><li>Milestones restructured into Delivered Infrastructure plus Phases A-E in <a href=\"../milestones.md\">milestones.md</a>.</li><li>Current Phase A progress (M-A1 Complete on Ollama <code>qwen3.5:4b</code>; M-A2 In progress with three h003 records) reflected in <a href=\"../current_state.md\">current_state.md</a> and <a href=\"../active_threads.md\">active_threads.md</a>.</li><li><a href=\"../decisions.md\">D007</a> Freeze Further Deterministic Regex Expansion recorded.</li><li>Project Phases section added to <a href=\"../research_program.md\">research_program.md</a> mapping harness IDs to milestones.</li><li>Phase A kickoff and project re-scope entries added to <a href=\"../development_log.md\">development_log.md</a>.</li><li>No code or test changes in this session; no new run records produced.</li></ul>",
      "uncertainty": "<p>Phase D may never happen — it is fully governance-gated and optional. Phase E visual artifacts are still &quot;Planned&quot; and should later be cross-linked with <a href=\"../visual_artifacts_direction.md\">visual_artifacts_direction.md</a>. The new phase vocabulary is retrofitted onto earlier session logs, so cross-references to pre-phase work are necessarily loose. The harnesses registry still lists <code>h004</code> and <code>h005</code> as &quot;pending&quot; rather than phase-tagged; that is fine for now and can be tightened when each becomes a serious comparison target.</p>",
      "handoff": "<p>Next useful action is M-A2 continuation: classify the <code>h003_single_prompt_llm</code> abstentions on <a href=\"20260424T180629Z_h003_single_prompt_llm_n25.json\">20260424T180629Z_h003_single_prompt_llm_n25.json</a>, add one narrow intervention (prompt or candidate-span aid) for cluster, window, and seizure-free cases, and rerun h003 on the same 25-row slice. Only then consider M-A3 (<code>h004_multi_agent_llm</code>). Do not return to deterministic regex expansion — see <a href=\"../decisions.md\">D007</a>.</p>",
      "decision": "documentation/visibility updated, no metric decision needed",
      "href": "run_logs/20260424T185000Z_project_phase_rescope.md",
      "tags": [
        "documentation/visibility updated, no metric decision needed"
      ],
      "filesChangedCount": 0,
      "checksRunCount": 0,
      "artifactsUpdatedCount": 5,
      "runEvidenceCount": 0,
      "hasDecision": true
    },
    {
      "title": "h003 Ollama Think-Disabled Smoke",
      "date": "2026-04-24",
      "objective": "Make the local <code>h003_single_prompt_llm</code> path usable enough for a 25-row smoke evaluation.",
      "outcome": "<p><code>h003_single_prompt_llm</code> now disables Ollama thinking mode, caps local completions, recovers JSON from common local-model wrappers, and tolerates schema-near evidence strings. The local <code>qwen3.5:4b</code> path moved from timeout-heavy plumbing validation to a fast 25-row smoke, but extraction quality remains weak because the model over-abstains.</p>",
      "outcomePlain": "h003_single_prompt_llm now disables Ollama thinking mode, caps local completions, recovers JSON from common local-model wrappers, and tolerates schema-near evidence strings. The local qwen3.5:4b path moved from timeout-heavy plumbing validation to a fast 25-row smoke, but extraction quality remains weak because the model over-abstains.",
      "evidence": "<ul><li>Files changed: <a href=\"../../src/epilepsy_agents/llm_pipeline.py\">llm_pipeline.py</a>, <a href=\"../../src/epilepsy_agents/providers.py\">providers.py</a>, <a href=\"../../src/epilepsy_agents/structured_schema.py\">structured_schema.py</a>, <a href=\"../../tests/test_llm_pipeline.py\">test_llm_pipeline.py</a>, <a href=\"../../tests/test_cli.py\">test_cli.py</a>, <a href=\"../current_state.md\">current_state.md</a>, <a href=\"../active_threads.md\">active_threads.md</a>.</li><li>Run records: <a href=\"../../project_state/runs/20260424T171400Z_h003_single_prompt_llm_n5.json\">original h003 n5</a>, <a href=\"../../project_state/runs/20260424T180607Z_h003_single_prompt_llm_n5.json\">updated h003 n5</a>, <a href=\"../../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json\">updated h003 n25</a>.</li><li>Manifest: <a href=\"../../project_state/experiments/manifest.csv\">manifest.csv</a> now includes the new n1, n5, and n25 <code>h003</code> smoke records from this session.</li><li>Tests or checks: <code>python -m unittest discover -s tests</code> passed with 37 tests.</li></ul><p>Key metric movement:</p><table><thead><tr><th>Run</th><th>n</th><th>Exact</th><th>Monthly 15 pct</th><th>Pragmatic micro-F1</th><th>Purist micro-F1</th><th>Invalid-output rate</th><th>Mean latency</th></tr></thead><tbody><tr><td><code>20260424T171400Z_h003_single_prompt_llm_n5</code></td><td>5</td><td>0.20</td><td>0.20</td><td>0.20</td><td>0.20</td><td>0.80</td><td>52.9 s</td></tr><tr><td><code>20260424T180607Z_h003_single_prompt_llm_n5</code></td><td>5</td><td>0.40</td><td>0.40</td><td>0.40</td><td>0.40</td><td>0.40</td><td>0.95 s</td></tr><tr><td><code>20260424T180629Z_h003_single_prompt_llm_n25</code></td><td>25</td><td>0.20</td><td>0.28</td><td>0.36</td><td>0.32</td><td>0.28</td><td>1.29 s</td></tr></tbody></table>",
      "uncertainty": "<p>The 25-row result is still too small and too abstention-heavy to compare against deterministic baselines. The run has many <code>unknown</code> or <code>no seizure frequency reference</code> predictions, especially where the gold label is frequent or infrequent. The parser now accepts schema-near output, so future work should separate true model extraction failure from output-format failure more carefully.</p>",
      "handoff": "<p>Next, classify the 25-row <code>h003</code> abstentions by gold family and add one targeted intervention for cluster, windowed-rate, or seizure-free phrasing. Rerun the same 25-row slice before comparing <code>qwen3.5:9b</code> or starting <code>h004_multi_agent_llm</code>.</p>",
      "decision": "implementation works but needs full synthetic evaluation",
      "href": "run_logs/20260424T180900Z_h003_ollama_think_disabled_smoke.md",
      "tags": [
        "7 files changed",
        "tests run",
        "run evidence"
      ],
      "filesChangedCount": 1,
      "checksRunCount": 1,
      "artifactsUpdatedCount": 1,
      "runEvidenceCount": 1,
      "hasDecision": true
    },
    {
      "title": "h003 Local Ollama Smoke",
      "date": "2026-04-24",
      "objective": "Verify a live local runtime and record the first <code>h003_single_prompt_llm</code> smoke run.",
      "outcome": "<p>The local Ollama runtime is now confirmed live for Phase A work. <code>provider-smoke</code> succeeded against local <code>qwen3.5:4b</code>, and the repository produced its first <code>h003_single_prompt_llm</code> run record on a 5-row synthetic slice. The blocker has moved from runtime setup to prompt and schema robustness: the first <code>h003</code> smoke returned <code>unknown</code> on four of five rows and recorded an invalid-output rate of 0.80.</p>",
      "outcomePlain": "The local Ollama runtime is now confirmed live for Phase A work. provider-smoke succeeded against local qwen3.5:4b, and the repository produced its first h003_single_prompt_llm run record on a 5-row synthetic slice. The blocker has moved from runtime setup to prompt and schema robustness: the first h003 smoke returned unknown on four of five rows and recorded an invalid-output rate of 0.80.",
      "evidence": "<ul><li>Files changed:</li><li><a href=\"/C:/Users/cbrow/Code/dissertation/src/epilepsy_agents/llm_pipeline.py\">src/epilepsy_agents/llm_pipeline.py</a></li><li><a href=\"/C:/Users/cbrow/Code/dissertation/scripts/run_harness_experiment.py\">scripts/run_harness_experiment.py</a></li><li><a href=\"/C:/Users/cbrow/Code/dissertation/tests/test_llm_pipeline.py\">tests/test_llm_pipeline.py</a></li><li><a href=\"/C:/Users/cbrow/Code/dissertation/src/epilepsy_agents/cli.py\">src/epilepsy_agents/cli.py</a></li><li><a href=\"/C:/Users/cbrow/Code/dissertation/src/epilepsy_agents/providers.py\">src/epilepsy_agents/providers.py</a></li><li>Run records:</li><li><a href=\"/C:/Users/cbrow/Code/dissertation/project_state/runs/20260424T171400Z_h003_single_prompt_llm_n5.json\">20260424T171400Z_h003_single_prompt_llm_n5.json</a></li><li>Tests or checks:</li><li><code>PYTHONPATH=src python -m unittest discover -s tests</code> -&gt; 32 tests passed.</li><li><code>PYTHONPATH=src python -m epilepsy_agents.cli provider-smoke --provider ollama --model qwen3.5:4b --timeout-seconds 60</code> -&gt; probe and schema-constrained chat succeeded.</li><li><code>PYTHONPATH=src python scripts\\run_harness_experiment.py --harness single_llm --provider ollama --model qwen3.5:4b --limit 5 --timeout-seconds 60</code> -&gt; first <code>h003</code> run recorded.</li><li>Generated artifacts:</li><li>Manifest entry added under <a href=\"/C:/Users/cbrow/Code/dissertation/project_state/experiments/manifest.csv\">project_state/experiments/manifest.csv</a>.</li></ul>",
      "uncertainty": "<p>The first <code>h003</code> smoke is only five rows and is not yet a meaningful baseline comparison. Mean latency was about 52.9 seconds per row, so larger slices will be slow unless validity improves enough to justify them. The initial prompt and schema path likely needs targeted tuning for explicit frequency extraction and cluster handling.</p>",
      "handoff": "<p>Inspect the four <code>unknown</code> outputs in <a href=\"/C:/Users/cbrow/Code/dissertation/project_state/runs/20260424T171400Z_h003_single_prompt_llm_n5.json\">20260424T171400Z_h003_single_prompt_llm_n5.json</a>, tighten the prompt and schema handling, then rerun <code>h003_single_prompt_llm</code> on 25 rows. If <code>qwen3.5:4b</code> remains too abstention-heavy, compare against local <code>qwen3.5:9b</code>.</p>",
      "decision": "implementation works but needs full synthetic evaluation",
      "href": "run_logs/20260424T171400Z_h003_local_ollama_smoke.md",
      "tags": [
        "1 files changed",
        "tests run",
        "artifacts updated",
        "run evidence"
      ],
      "filesChangedCount": 5,
      "checksRunCount": 3,
      "artifactsUpdatedCount": 1,
      "runEvidenceCount": 1,
      "hasDecision": true
    }
  ],
  "workstreams": [
    {
      "name": "Harness Reliability",
      "question": "How can the deterministic and future LLM-backed harnesses reduce seizure-frequency extraction errors while preserving evidence support and auditability?",
      "evidence": "<ul><li>Latest paired 100-row synthetic smoke runs (after seizure-free detection expansion):</li><li><code>h002_multi_agent_verify</code>: exact 0.31, monthly 0.48, pragmatic micro-F1 0.55, purist micro-F1 0.53, NS F1 0.82.</li><li><code>h001_single_pass</code>: exact 0.25, monthly 0.43, pragmatic micro-F1 0.50, purist micro-F1 0.48, NS F1 0.73.</li><li>First local LLM smoke run:</li><li><code>h003_single_prompt_llm</code>: exact 0.20, monthly 0.20, pragmatic micro-F1 0.20, purist micro-F1 0.20, invalid-output rate 0.80, mean latency about 52.9 s on <code>ollama</code> with <code>qwen3.5:4b</code>.</li><li>Updated local LLM smoke after disabling Ollama thinking and tolerating schema-near JSON:</li><li><code>h003_single_prompt_llm</code> n5: exact 0.40, monthly 0.40, pragmatic micro-F1 0.40, purist micro-F1 0.40, invalid-output rate 0.40, mean latency about 0.95 s.</li><li><code>h003_single_prompt_llm</code> n25: exact 0.20, monthly 0.28, pragmatic micro-F1 0.36, purist micro-F1 0.32, invalid-output rate 0.28, mean latency about 1.29 s.</li><li><code>seizure_free_error</code> dropped from 18 to 9 on multi and from 19 to 13 on single; <code>correct</code> rose from 20 to 31 on multi.</li><li>Run records: <a href=\"../project_state/runs/20260424T144559Z_h002_multi_agent_verify_n100.json\">multi n100</a>, <a href=\"../project_state/runs/20260424T144606Z_h001_single_pass_n100.json\">single n100</a>, <a href=\"../project_state/runs/20260424T171400Z_h003_single_prompt_llm_n5.json\">h003 original n5</a>, <a href=\"../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json\">h003 updated n25</a>.</li><li>The 17 abstentions in the latest <code>h003</code> 25-row smoke are now classified into seven failure families (9 window/aggregation, 4 cluster-shape, 2 NS-vs-no-reference, 2 qualitative, 2 actually-correct true-unknowns); see <a href=\"run_logs/20260425T081533Z_h003_abstention_classification.md\">run_logs/20260425T081533Z_h003_abstention_classification.md</a> for the per-row breakdown and an ordered three-step intervention list.</li><li>Intervention 1 (six worked phrasing -&gt; label exemplars in <code>system_prompt()</code>) is now landed in <a href=\"../src/epilepsy_agents/structured_schema.py\">structured_schema.py</a>; the unit-test suite still passes (38/38). The empirical paired rerun on the 25-row slice is deferred because no Ollama runtime is reachable in the current sandbox; see <a href=\"run_logs/20260426T081829Z_h003_system_prompt_exemplars.md\">run_logs/20260426T081829Z_h003_system_prompt_exemplars.md</a>.</li><li>Session logs: <a href=\"run_logs/20260424T144639Z_seizure_free_detection_expansion.md\">20260424T144639Z_seizure_free_detection_expansion.md</a>, <a href=\"run_logs/20260425T081533Z_h003_abstention_classification.md\">20260425T081533Z_h003_abstention_classification.md</a>, <a href=\"run_logs/20260426T081829Z_h003_system_prompt_exemplars.md\">20260426T081829Z_h003_system_prompt_exemplars.md</a>.</li></ul>",
      "evidencePlain": "- Latest paired 100-row synthetic smoke runs (after seizure-free detection expansion): - h002_multi_agent_verify: exact 0.31, monthly 0.48, pragmatic micro-F1 0.55, purist micro-F1 0.53, NS F1 0.82. - h001_single_pass: exact 0.25, monthly 0.43, pragmatic micro-F1 0.50, purist micro-F1 0.48, NS F1 0.73. - First local LLM smoke run: - h003_single_prompt_llm: exact 0.20, monthly 0.20, pragmatic micro-F1 0.20, purist micro-F1 0.20, invalid-output rate 0.80, mean latency about 52.9 s on ollama with qwen3.5:4b. - Updated local LLM smoke after disabling Ollama thinking and tolerating schema-near JSON: - h003_single_prompt_llm n5: exact 0.40, monthly 0.40, pragmatic micro-F1 0.40, purist micro-F1 0.40, invalid-output rate 0.40, mean latency about 0.95 s. - h003_single_prompt_llm n25: exact 0.20, monthly 0.28, pragmatic micro-F1 0.36, purist micro-F1 0.32, invalid-output rate 0.28, mean latency about 1.29 s. - seizure_free_error dropped from 18 to 9 on multi and from 19 to 13 on single; correct rose from 20 to 31 on multi. - Run records: multi n100, single n100, h003 original n5, h003 updated n25. - The 17 abstentions in the latest h003 25-row smoke are now classified into seven failure families (9 window/aggregation, 4 cluster-shape, 2 NS-vs-no-reference, 2 qualitative, 2 actually-correct true-unknowns); see run_logs/20260425T081533Z_h003_abstention_classification.md for the per-row breakdown and an ordered three-step intervention list. - Intervention 1 (six worked phrasing -> label exemplars in system_prompt()) is now landed in structured_schema.py; the unit-test suite still passes (38/38). The empirical paired rerun on the 25-row slice is deferred because no Ollama runtime is reachable in the current sandbox; see run_logs/20260426T081829Z_h003_system_prompt_exemplars.md. - Session logs: 20260424T144639Z_seizure_free_detection_expansion.md, 20260425T081533Z_h003_abstention_classification.md, 20260426T081829Z_h003_system_prompt_exemplars.md.",
      "risk": "<p>The deterministic baseline still has residual seizure-free and cluster-family errors. On the LLM side, intervention 1 is implemented but unmeasured: the paired empirical rerun that would justify keep/reject for the new system prompt requires a local Ollama runtime that is not present in the current sandbox.</p>",
      "riskPlain": "The deterministic baseline still has residual seizure-free and cluster-family errors. On the LLM side, intervention 1 is implemented but unmeasured: the paired empirical rerun that would justify keep/reject for the new system prompt requires a local Ollama runtime that is not present in the current sandbox.",
      "next": "<p>Steps 1 (parser round-trip check) and 2 (apply intervention 1 to <code>system_prompt()</code>) from the 2026-04-25 ordered list are done; see <a href=\"run_logs/20260426T081829Z_h003_system_prompt_exemplars.md\">20260426T081829Z_h003_system_prompt_exemplars.md</a>. The next LLM-runtime session should: (a) bring up Ollama with <code>qwen3.5:4b</code>; (b) rerun <code>h003_single_prompt_llm</code> on the same 25-row <code>row_ok</code> slice as <a href=\"../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json\">20260424T180629Z_h003_single_prompt_llm_n25.json</a>; (c) compare invalid-output rate, abstention count, and pragmatic micro-F1 against the 2026-04-24 baseline and re-classify any remaining abstentions; (d) only if window and cluster cases improve but NS or qualitative cases remain, apply intervention 2 (NS-vs-no-reference rule in the user prompt) in a separate paired run.</p>",
      "nextPlain": "Steps 1 (parser round-trip check) and 2 (apply intervention 1 to system_prompt()) from the 2026-04-25 ordered list are done; see 20260426T081829Z_h003_system_prompt_exemplars.md. The next LLM-runtime session should: (a) bring up Ollama with qwen3.5:4b; (b) rerun h003_single_prompt_llm on the same 25-row row_ok slice as 20260424T180629Z_h003_single_prompt_llm_n25.json; (c) compare invalid-output rate, abstention count, and pragmatic micro-F1 against the 2026-04-24 baseline and re-classify any remaining abstentions; (d) only if window and cluster cases improve but NS or qualitative cases remain, apply intervention 2 (NS-vs-no-reference rule in the user prompt) in a separate paired run.",
      "priority": "watch"
    },
    {
      "name": "Provider And Local Model Setup",
      "question": "Which local runtime and first model should be used for schema-constrained extraction smoke tests?",
      "evidence": "<ul><li>The laptop has an RTX 4070 Laptop GPU with 8 GB VRAM and enough disk for quantized local inference.</li><li>Ollama is installed locally and its API is responding at <code>http://localhost:11434/api</code>.</li><li>Local models currently visible through Ollama include <code>qwen3.5:4b</code>, <code>qwen3.5:9b</code>, <code>qwen3.5:35b-a3b</code>, and <code>llama3.1:latest</code>.</li><li><code>provider-smoke</code> succeeded end to end against local <code>qwen3.5:4b</code>.</li><li><code>h003</code> now sends <code>think: false</code> with a capped Ollama completion budget, avoiding the earlier timeout caused by model reasoning traces.</li><li>Candidate model tiers are documented in <a href=\"local_model_feasibility.md\">local_model_feasibility.md</a>.</li></ul>",
      "evidencePlain": "- The laptop has an RTX 4070 Laptop GPU with 8 GB VRAM and enough disk for quantized local inference. - Ollama is installed locally and its API is responding at http://localhost:11434/api. - Local models currently visible through Ollama include qwen3.5:4b, qwen3.5:9b, qwen3.5:35b-a3b, and llama3.1:latest. - provider-smoke succeeded end to end against local qwen3.5:4b. - h003 now sends think: false with a capped Ollama completion budget, avoiding the earlier timeout caused by model reasoning traces. - Candidate model tiers are documented in local_model_feasibility.md.",
      "risk": "<p>Local runtime installation is no longer the blocker. The active risk is whether the first chosen model plus prompt/schema setup can avoid excessive abstention while preserving evidence support.</p>",
      "riskPlain": "Local runtime installation is no longer the blocker. The active risk is whether the first chosen model plus prompt/schema setup can avoid excessive abstention while preserving evidence support.",
      "next": "<p>Keep Ollama as the active runtime, improve <code>h003</code> extraction validity on <code>qwen3.5:4b</code>, and compare against <code>qwen3.5:9b</code> if the smaller model stays too abstention-heavy.</p>",
      "nextPlain": "Keep Ollama as the active runtime, improve h003 extraction validity on qwen3.5:4b, and compare against qwen3.5:9b if the smaller model stays too abstention-heavy.",
      "priority": "blocked"
    },
    {
      "name": "Evidence Notebook Visibility",
      "question": "How should project state stay legible across long agent-assisted development sessions?",
      "evidence": "<ul><li>The chosen visibility direction is Evidence Notebook.</li><li>Phase 1 markdown pages now exist: <a href=\"current_state.md\">current_state.md</a>, <a href=\"milestones.md\">milestones.md</a>, <a href=\"active_threads.md\">active_threads.md</a>, <a href=\"decisions.md\">decisions.md</a>, and <a href=\"artifact_registry.md\">artifact_registry.md</a>.</li><li>Phase 2 session logging convention exists at <a href=\"run_logs/README.md\">run_logs/README.md</a>, with a template and optional JSON companion files.</li><li>The notebook archive now includes backfilled pre-visibility session logs for the initial scaffold, harness protocol, and retrieval iteration.</li><li>Phase 3 dashboard exists at <a href=\"../site/index.html\">site/index.html</a> with CSS/JS in <a href=\"../site/assets/\">site/assets/</a>, generated by <a href=\"../src/epilepsy_agents/visibility/\">src/epilepsy_agents/visibility/</a>.</li></ul>",
      "evidencePlain": "- The chosen visibility direction is Evidence Notebook. - Phase 1 markdown pages now exist: current_state.md, milestones.md, active_threads.md, decisions.md, and artifact_registry.md. - Phase 2 session logging convention exists at run_logs/README.md, with a template and optional JSON companion files. - The notebook archive now includes backfilled pre-visibility session logs for the initial scaffold, harness protocol, and retrieval iteration. - Phase 3 dashboard exists at site/index.html with CSS/JS in site/assets/, generated by src/epilepsy_agents/visibility/.",
      "risk": "<p>The source markdown layer is still hand-maintained, the dashboard can drift unless future sessions regenerate it after state updates, and the historical backfill is only as good as the surviving repo evidence behind it.</p>",
      "riskPlain": "The source markdown layer is still hand-maintained, the dashboard can drift unless future sessions regenerate it after state updates, and the historical backfill is only as good as the surviving repo evidence behind it.",
      "next": "<p>Use the dashboard for quick review, keep new session logs contemporaneous, regenerate after substantial closeouts, and proceed to the first curated Phase 4 visual artifact.</p>",
      "nextPlain": "Use the dashboard for quick review, keep new session logs contemporaneous, regenerate after substantial closeouts, and proceed to the first curated Phase 4 visual artifact.",
      "priority": "watch"
    },
    {
      "name": "Visual And Dissertation Artifacts",
      "question": "Which explanatory visuals should be produced first for README, dissertation, and supervisor review?",
      "evidence": "<ul><li>The shared Clinical Blueprint + Evidence Highlighter visual language is defined in <a href=\"visual_artifacts_direction.md\">visual_artifacts_direction.md</a>.</li><li>The first target set includes architecture, deployment, dataset/evaluation, agent roles, milestones, local model feasibility, evidence grounding, and final packaging.</li></ul>",
      "evidencePlain": "- The shared Clinical Blueprint + Evidence Highlighter visual language is defined in visual_artifacts_direction.md. - The first target set includes architecture, deployment, dataset/evaluation, agent roles, milestones, local model feasibility, evidence grounding, and final packaging.",
      "risk": "<p>Generated visuals can become decorative if not tied to evidence and current project state.</p>",
      "riskPlain": "Generated visuals can become decorative if not tied to evidence and current project state.",
      "next": "<p>Create the Project Architecture Poster first, using only synthetic/anonymised-looking text and sparse labels.</p>",
      "nextPlain": "Create the Project Architecture Poster first, using only synthetic/anonymised-looking text and sparse labels.",
      "priority": "active"
    },
    {
      "name": "Real-Data Governance",
      "question": "How should the project prepare for possible real King&#x27;s College Hospital evaluation without leaking raw clinical content?",
      "evidence": "<ul><li>Governance rules are documented in <a href=\"real_data_governance.md\">real_data_governance.md</a>.</li><li>The research program explicitly prohibits autonomous loops on real clinical text and raw-text exports.</li></ul>",
      "evidencePlain": "- Governance rules are documented in real_data_governance.md. - The research program explicitly prohibits autonomous loops on real clinical text and raw-text exports.",
      "risk": "<p>Any future real-data stage must happen inside the approved environment and may restrict providers, telemetry, examples, traces, screenshots, and artifacts.</p>",
      "riskPlain": "Any future real-data stage must happen inside the approved environment and may restrict providers, telemetry, examples, traces, screenshots, and artifacts.",
      "next": "<p>Keep real-data support as an architecture constraint, not an active local-data workflow.</p>",
      "nextPlain": "Keep real-data support as an architecture constraint, not an active local-data workflow.",
      "priority": "watch"
    }
  ],
  "artifacts": [
    {
      "name": "Project specification",
      "purpose": "Define dissertation question, objectives, methods, data, metrics, and risks.",
      "status": "Current",
      "path": "<a href=\"project_specification.md\">project_specification.md</a>",
      "use": "Dissertation and orientation."
    },
    {
      "name": "Research program",
      "purpose": "Operating brief for future agent-assisted work.",
      "status": "Current",
      "path": "<a href=\"research_program.md\">research_program.md</a>",
      "use": "Session orientation and scope control."
    },
    {
      "name": "Evaluation protocol",
      "purpose": "Define metrics, baselines, controls, and standard commands.",
      "status": "Current",
      "path": "<a href=\"evaluation_protocol.md\">evaluation_protocol.md</a>",
      "use": "Experiment design and reporting."
    },
    {
      "name": "Harness experiment protocol",
      "purpose": "Define reproducible run records and manifest conventions.",
      "status": "Current",
      "path": "<a href=\"harness_experiment_protocol.md\">harness_experiment_protocol.md</a>",
      "use": "Run logging and auditability."
    },
    {
      "name": "Run manifest",
      "purpose": "Compact index of fixed-budget harness experiments.",
      "status": "Active",
      "path": "<a href=\"../project_state/experiments/manifest.csv\">manifest.csv</a>",
      "use": "Experiment lookup and dashboard source."
    },
    {
      "name": "Run records",
      "purpose": "Structured per-run metrics, metadata, and safe error categories.",
      "status": "Active",
      "path": "<a href=\"../project_state/runs\">project_state/runs</a>",
      "use": "Evidence Notebook session feed and metric comparisons."
    },
    {
      "name": "Harness registry",
      "purpose": "Stable IDs and status for extraction harness variants.",
      "status": "Active",
      "path": "<a href=\"../project_state/harnesses/README.md\">project_state/harnesses/README.md</a>",
      "use": "Variant tracking."
    },
    {
      "name": "Local model feasibility report",
      "purpose": "Explain hardware, runtime options, model tiers, and provider architecture.",
      "status": "Current",
      "path": "<a href=\"local_model_feasibility.md\">local_model_feasibility.md</a>",
      "use": "Local runtime planning and dissertation methods."
    },
    {
      "name": "Real-data governance note",
      "purpose": "Define privacy boundaries for later real clinical evaluation.",
      "status": "Current",
      "path": "<a href=\"real_data_governance.md\">real_data_governance.md</a>",
      "use": "Risk control and future secure-environment work."
    },
    {
      "name": "Visual artifacts direction",
      "purpose": "Define project visual language and first artifact set.",
      "status": "Current",
      "path": "<a href=\"visual_artifacts_direction.md\">visual_artifacts_direction.md</a>",
      "use": "README, dissertation, and presentation visuals."
    },
    {
      "name": "Agent visibility plan",
      "purpose": "Define visibility stack and Evidence Notebook direction.",
      "status": "Current",
      "path": "<a href=\"agent_visibility_plan.md\">agent_visibility_plan.md</a>",
      "use": "Visibility roadmap."
    },
    {
      "name": "Agent visibility UI mockups",
      "purpose": "Explore Live Mission Control, Evidence Notebook, and Project Atlas directions.",
      "status": "Reference",
      "path": "<a href=\"agent_visibility_ui_mockups.html\">agent_visibility_ui_mockups.html</a>",
      "use": "Future dashboard design reference."
    },
    {
      "name": "Evidence Notebook project-state pages",
      "purpose": "Provide source-backed current state, milestones, active threads, decisions, and artifact index.",
      "status": "Active",
      "path": "<a href=\"current_state.md\">current_state.md</a>, <a href=\"milestones.md\">milestones.md</a>, <a href=\"active_threads.md\">active_threads.md</a>, <a href=\"decisions.md\">decisions.md</a>, <a href=\"artifact_registry.md\">artifact_registry.md</a>",
      "use": "Human oversight and future dashboard source."
    },
    {
      "name": "Session logging convention",
      "purpose": "Define when to write logs, naming rules, status labels, evidence rules, optional JSON companions, and closeout checklist.",
      "status": "Active",
      "path": "<a href=\"run_logs/README.md\">run_logs/README.md</a>",
      "use": "Session audit trail and dashboard source."
    },
    {
      "name": "Session-log template",
      "purpose": "Standardize session outcome, evidence, uncertainty, and handoff.",
      "status": "Active",
      "path": "<a href=\"run_logs/session_log_template.md\">run_logs/session_log_template.md</a>",
      "use": "Future session closeouts."
    },
    {
      "name": "Session-log companion schema",
      "purpose": "Define optional machine-readable session-log metadata for future dashboard ingestion.",
      "status": "Active",
      "path": "<a href=\"run_logs/session_log_companion_schema.json\">session_log_companion_schema.json</a>",
      "use": "Future dashboard or generated index."
    },
    {
      "name": "Session-log companion template",
      "purpose": "Provide a valid JSON starting point for optional session companions.",
      "status": "Active",
      "path": "<a href=\"run_logs/session_log_companion_template.json\">session_log_companion_template.json</a>",
      "use": "Future dashboard or generated index."
    },
    {
      "name": "Initial scaffold session log",
      "purpose": "Reconstruct the repository bootstrap into notebook-native session history.",
      "status": "Current",
      "path": "<a href=\"run_logs/20260424T075111Z_initial_scaffold.md\">20260424T075111Z_initial_scaffold.md</a>",
      "use": "Historical continuity and supervisor review."
    },
    {
      "name": "Harness protocol and smoke runs session log",
      "purpose": "Reconstruct the transition from ad hoc work to named harness experiments and paired run records.",
      "status": "Current",
      "path": "<a href=\"run_logs/20260424T084000Z_harness_protocol_and_smoke_runs.md\">20260424T084000Z_harness_protocol_and_smoke_runs.md</a>",
      "use": "Historical continuity and audit trail."
    },
    {
      "name": "Candidate retrieval iteration session log",
      "purpose": "Reconstruct the deterministic retrieval expansion and the paired 100-row smoke reruns that preceded the visibility sessions.",
      "status": "Current",
      "path": "<a href=\"run_logs/20260424T085900Z_candidate_retrieval_iteration.md\">20260424T085900Z_candidate_retrieval_iteration.md</a>",
      "use": "Historical continuity and audit trail."
    },
    {
      "name": "Visibility Phase 1 session log",
      "purpose": "Record the first implementation pass for the Evidence Notebook layer.",
      "status": "Current",
      "path": "<a href=\"run_logs/20260424T090341Z_visibility_phase1.md\">20260424T090341Z_visibility_phase1.md</a>",
      "use": "Handoff and audit trail."
    },
    {
      "name": "Visibility Phase 2 session log",
      "purpose": "Record the implementation pass for the session logging convention.",
      "status": "Current",
      "path": "<a href=\"run_logs/20260424T092054Z_visibility_phase2.md\">20260424T092054Z_visibility_phase2.md</a>",
      "use": "Handoff and audit trail."
    },
    {
      "name": "Evidence Notebook dashboard",
      "purpose": "Provide a deployable visual dashboard over current claims, milestones, recent sessions, workstreams, artifacts, and decisions.",
      "status": "Active",
      "path": "<a href=\"../site/index.html\">site/index.html</a>",
      "use": "Supervisor review, session orientation, and Vercel deploy."
    },
    {
      "name": "Evidence Notebook generator",
      "purpose": "Regenerate the dashboard&#x27;s <code>data.js</code> payload from markdown source files without a frontend dependency stack.",
      "status": "Active",
      "path": "<a href=\"../src/epilepsy_agents/visibility/\">src/epilepsy_agents/visibility/</a>",
      "use": "Dashboard maintenance and future ingestion work."
    },
    {
      "name": "Visibility Phase 3 session log",
      "purpose": "Record the implementation pass for the local Evidence Notebook dashboard.",
      "status": "Current",
      "path": "<a href=\"run_logs/20260424T093100Z_visibility_phase3.md\">20260424T093100Z_visibility_phase3.md</a>",
      "use": "Handoff and audit trail."
    },
    {
      "name": "Seizure-free detection expansion session log",
      "purpose": "Record the deterministic seizure-free detection broadening and paired 100-row smoke results.",
      "status": "Current",
      "path": "<a href=\"run_logs/20260424T144639Z_seizure_free_detection_expansion.md\">20260424T144639Z_seizure_free_detection_expansion.md</a>",
      "use": "Handoff and audit trail."
    },
    {
      "name": "h003 Ollama think-disabled smoke session log",
      "purpose": "Record the local LLM runtime fix, schema-near parsing tolerance, and 25-row <code>h003</code> smoke result.",
      "status": "Current",
      "path": "<a href=\"run_logs/20260424T180900Z_h003_ollama_think_disabled_smoke.md\">20260424T180900Z_h003_ollama_think_disabled_smoke.md</a>",
      "use": "Handoff and audit trail."
    },
    {
      "name": "Agent Role Cards",
      "purpose": "Reusable visual cards for the four conceptual agents: section/timeline, field extraction, verification, and aggregation.",
      "status": "Current",
      "path": "<a href=\"../output/agent-role-cards.png\">agent-role-cards.png</a>, <a href=\"../output/agent-role-cards\">individual cards</a>",
      "use": "README, dissertation figures, presentation support, and agent-role explanation."
    },
    {
      "name": "Project Architecture Poster",
      "purpose": "Explain the multi-agent extraction pipeline visually with a sparse Clinical Blueprint identity.",
      "status": "Current",
      "path": "<a href=\"../output/visual-artifacts/project-architecture-poster.png\">project-architecture-poster.png</a>",
      "use": "README, dissertation figure, supervisor review."
    },
    {
      "name": "Milestone Timeline",
      "purpose": "Show progress, current h003 focus, and next dissertation stages as a phase map.",
      "status": "Current",
      "path": "<a href=\"../output/visual-artifacts/milestone-timeline.png\">milestone-timeline.png</a>",
      "use": "Dissertation and presentation support."
    },
    {
      "name": "Local-First Hospital Deployment Diagram",
      "purpose": "Explain why real clinical text stays local.",
      "status": "Planned",
      "path": "To be generated.",
      "use": "Governance explanation."
    },
    {
      "name": "Dataset and Evaluation Overview",
      "purpose": "Explain seizure-frequency labels and metric bundle.",
      "status": "Planned",
      "path": "To be generated.",
      "use": "Methods section and supervisor review."
    }
  ],
  "decisions": [
    {
      "id": "D001",
      "title": "Treat The Project As A Harness-Reliability Study",
      "decision": "The central research posture is harness reliability, not a simple model leaderboard.",
      "rationale": "<p>The dissertation question is whether constrained, evidence-grounded extraction improves seizure-frequency reliability under matched budgets.</p>",
      "consequence": "<p>Each meaningful change should alter one harness, prompt, provider, verification rule, or visibility artifact, then be evaluated through a fixed metric bundle.</p>",
      "evidence": "<a href=\"research_program.md\">research_program.md</a>, <a href=\"harness_experiment_protocol.md\">harness_experiment_protocol.md</a>.",
      "markers": [
        "evaluation protocol",
        "runtime architecture"
      ]
    },
    {
      "id": "D002",
      "title": "Keep Deterministic Baselines Before LLM Expansion",
      "decision": "The repository starts with deterministic <code>single</code> and <code>multi</code> harnesses that mirror planned role boundaries.",
      "rationale": "<p>This gives a reproducible offline baseline before provider variance, cost, latency, and schema failures enter the study.</p>",
      "consequence": "<p>Deterministic metrics provide the first comparison floor, but the system must not claim final LLM or clinical performance from them.</p>",
      "evidence": "<a href=\"project_specification.md\">project_specification.md</a>, <a href=\"../project_state/harnesses/README.md\">project_state/harnesses/README.md</a>, <a href=\"../project_state/experiments/manifest.csv\">project_state/experiments/manifest.csv</a>.",
      "markers": [
        "real-data governance",
        "evaluation protocol",
        "runtime architecture"
      ]
    },
    {
      "id": "D003",
      "title": "Use The Pareto Frontier Rule For Harness Selection",
      "decision": "Keep candidate harnesses that are non-dominated across reliability, evidence support, invalid-output behavior, and cost/runtime rather than forcing a single early winner.",
      "rationale": "<p>Clinical extraction quality is multi-dimensional. A slightly better F1 score may not be worth unsupported claims or poor abstention behavior.</p>",
      "consequence": "<p>Run records must retain enough information to compare class F1, monthly-rate accuracy, exact label accuracy, safe error categories, and later provider/runtime metadata.</p>",
      "evidence": "<a href=\"harness_experiment_protocol.md\">harness_experiment_protocol.md</a>, <a href=\"evaluation_protocol.md\">evaluation_protocol.md</a>.",
      "markers": [
        "real-data governance",
        "evaluation protocol",
        "runtime architecture"
      ]
    },
    {
      "id": "D004",
      "title": "Keep Closed Providers Synthetic-Only Unless Governance Changes",
      "decision": "Closed-provider experiments are acceptable only for synthetic data in the current repository context.",
      "rationale": "<p>Real clinical text must not leave the approved environment or enter external logs, traces, prompts, screenshots, or artifacts without explicit governance approval.</p>",
      "consequence": "<p>Provider adapters must make data-governance boundaries explicit, and real-data evaluation outputs must be aggregate and de-identified.</p>",
      "evidence": "<a href=\"real_data_governance.md\">real_data_governance.md</a>, <a href=\"local_model_feasibility.md\">local_model_feasibility.md</a>.",
      "markers": [
        "governs future work",
        "real-data governance",
        "evaluation protocol"
      ]
    },
    {
      "id": "D005",
      "title": "Prefer A Local Runtime For Real-Data Readiness",
      "decision": "The first local inference path should use an OpenAI-compatible local server such as LM Studio, Ollama, or llama.cpp server.",
      "rationale": "<p>The real-data stage needs a plausible local/offline pathway. A server interface also keeps orchestration separated from model runtime.</p>",
      "consequence": "<p>Provider code should stay modular and record runtime/model metadata for reproducibility.</p>",
      "evidence": "<a href=\"local_model_feasibility.md\">local_model_feasibility.md</a>, <a href=\"../src/epilepsy_agents/providers.py\">src/epilepsy_agents/providers.py</a>.",
      "markers": [
        "real-data governance",
        "runtime architecture",
        "governs future work"
      ]
    },
    {
      "id": "D006",
      "title": "Use Evidence Notebook As The Visibility Direction",
      "decision": "The visual orchestration layer should use the Evidence Notebook direction.",
      "rationale": "<p>The project needs source-backed, supervisor-reviewable claims rather than a generic operational dashboard.</p>",
      "consequence": "<p>Project-state files should be written as claim, evidence, uncertainty, and next-action entries that can later render into a local dashboard.</p>",
      "evidence": "<a href=\"agent_visibility_plan.md\">agent_visibility_plan.md</a>, <a href=\"agent_visibility_ui_mockups.html\">agent_visibility_ui_mockups.html</a>.",
      "markers": []
    },
    {
      "id": "D007",
      "title": "Freeze Further Deterministic Regex Expansion",
      "decision": "Do not continue broadening the deterministic regex extractor after the seizure-free detection expansion; use it as a comparison floor and move effort to the LLM-backed Phase A path.",
      "rationale": "<p>The deterministic baseline has already served its purpose: it gives a reproducible, offline floor for paired comparisons. Further regex tuning would improve the scaffold but would not answer the dissertation&#x27;s central question about evidence-grounded LLM harness reliability.</p>",
      "consequence": "<p>Future work should preserve deterministic comparability, but the next useful research action is to reduce <code>h003</code> abstention and then build the role-separated LLM harness.</p>",
      "evidence": "<a href=\"milestones.md\">milestones.md</a>, <a href=\"active_threads.md\">active_threads.md</a>, <a href=\"run_logs/20260424T144639Z_seizure_free_detection_expansion.md\">run_logs/20260424T144639Z_seizure_free_detection_expansion.md</a>.",
      "markers": [
        "governs future work",
        "evaluation protocol"
      ]
    }
  ]
};
