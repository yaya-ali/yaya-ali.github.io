---
layout: page
title: Projects
icon: fas fa-code
order: 2
---

## AI & LLM Systems

---

### Multi-Agent Content Generation Pipeline
**[↗ GitHub](https://github.com/yaya-ali/multi-agent-content-pipeline)**

`Next.js` `LangGraph` `OpenAI GPT-4` `Supabase` `Grafana`

A four-agent LLM pipeline — **Researcher → Writer → Fact-Checker → Polisher** — that takes a product brief and produces a publish-ready article with zero human steps. Built-in self-correction via LangGraph re-routes failed fact-checks back to the writer automatically. Live Grafana dashboard tracks token cost, failure rate, and quality scores per run.

---

### RouteIQ — LLM Cost Router & Observability Gateway
**[↗ GitHub](https://github.com/yaya-ali/routeiq)**

`Python` `FastAPI` `Redis` `Prometheus` `Grafana` `Docker` `NVIDIA NIM`

An API gateway that routes every LLM request to the cheapest model that can handle it. A complexity classifier picks between a small and a large model per request; atomic Redis date-keyed counters enforce per-team daily budgets (HTTP 429 when exhausted, auto-reset at midnight UTC); every token, dollar, and millisecond lands on an auto-provisioned Grafana dashboard. **Measured 10.2% cost saving with 0% quality drop** on a reasoning-heavy eval set — eval-gated in CI so cost optimization can never silently degrade quality. Ships with a minimal chat UI and a quiz-generator demo as consumer apps.

---

### Drift-Aware AI Retraining System

`Python` `Supabase (pgvector)` `EvidentlyAI` `Prometheus` `Grafana` `OpenAI Fine-Tune API`

Monitors model knowledge staleness by tracking query embedding shifts in a vector database. When drift is detected, the system automatically triggers knowledge base re-indexing or an OpenAI fine-tuning job — **fully self-healing, no engineer required**.

---

### Guardrail & Red-Team Test Harness

`Python` `OpenAI Moderation API` `Supabase` `GitHub Actions`

50+ adversarial prompts (jailbreaks, prompt injections, PII extraction) through a three-layer defence. Nightly GitHub Actions regression tests reduced jailbreak success rate **from 18% to under 4%** across three improvement cycles.

---

### Evaluation-as-a-Service (EaaS) Platform

`Next.js` `Python` `Supabase` `GPT-4-as-Judge` `Vercel` `GitHub Actions`

Teams upload model output CSVs, choose a grading method (exact-match / BLEU / GPT-4-as-Judge), and get scored results in minutes. A CI/CD deployment gate blocks any model version that scores below the configured quality threshold.

---

## Web Apps

---

### Medical AI Assistant

`Python` `FastAPI` `React`

Patient triage assistant deployed at a medical clinic. A preprocessing pipeline upstream of AI inference cut response time by ~40%. Adopted into daily workflow by 3 doctors.

---

### ChatGPT Clone
**[↗ GitHub](https://github.com/yaya-ali/chatgpt-clone)**

Full-stack ChatGPT-style interface with streaming responses, conversation history, and OpenAI API integration.
