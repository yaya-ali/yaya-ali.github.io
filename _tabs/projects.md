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

### LLM Model Router with Budget Controls

`Next.js` `OpenAI API` `Anthropic API` `Redis (Upstash)` `Supabase` `Grafana`

An API gateway that classifies queries as easy/medium/hard and routes to the cheapest capable model — serving **80% of traffic on lower-cost tiers** with no quality drop. Atomic Redis spend cap fires Slack alerts at 90% budget and shuts off expensive routes automatically.

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
