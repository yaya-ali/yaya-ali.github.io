---
title: "Building a Multi-Agent Content Pipeline with LangGraph"
date: 2025-05-10 10:00:00 +0200
categories: [AI, Projects]
tags: [langgraph, openai, multi-agent, next.js, supabase]
---

## The Problem

Producing high-quality written content consistently is slow and expensive when done manually. I wanted to explore whether a chain of specialized AI agents — each responsible for one part of the process — could reliably produce publish-ready articles from just a topic brief.

## Architecture

The pipeline runs four agents in sequence, with an automatic retry loop:

```
Topic Brief
    │
    ▼
┌─────────────┐
│  Researcher │  ── gathers facts, sources, context
└──────┬──────┘
       ▼
┌─────────────┐
│   Writer    │  ── drafts structured article
└──────┬──────┘
       ▼
┌─────────────────┐
│  Fact-Checker   │  ── verifies claims, flags issues
└──────┬──────────┘
       │  ❌ Issues found?
       │  └──► back to Writer with feedback
       │  ✅ Clean?
       ▼
┌─────────────┐
│   Polisher  │  ── refines tone, clarity, style
└──────┬──────┘
       ▼
  Final Article
```

The key insight is **LangGraph's conditional routing** — when the Fact-Checker flags an issue, the graph re-routes to the Writer node with the specific feedback attached, rather than failing or requiring human intervention.

## Self-Correction in Practice

```python
def should_retry(state: PipelineState) -> str:
    if state["fact_check_issues"] and state["retry_count"] < 3:
        return "writer"   # loop back
    return "polisher"     # proceed
```

This keeps hallucination rates low without a human reviewer in the loop.

## Observability

Every run logs to Supabase: token usage, cost, fact-check failure rate, quality rubric scores. A Grafana dashboard surfaces these in real time so you can spot regressions immediately.

## Results

- ~92% of runs pass fact-check on the first attempt
- Average cost per article: $0.04–0.08 (GPT-4o-mini)
- End-to-end time: ~45 seconds

## Source

[↗ github.com/yaya-ali/multi-agent-content-pipeline](https://github.com/yaya-ali/multi-agent-content-pipeline)
