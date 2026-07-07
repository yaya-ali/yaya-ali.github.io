---
title: "Building an LLM Cost Router — and Measuring Whether It Actually Helps"
date: 2025-04-20 10:00:00 +0200
categories: [AI, Engineering]
tags: [llm, redis, cost-optimization, fastapi, observability]
---

Most teams call their strongest (most expensive) model for *every* request —
including "summarize this in one sentence." That's wasteful: simple queries don't
need the big model. So I built **RouteIQ**, an open gateway that routes each request
to the cheapest model that can handle it, and — this is the part that matters —
*measures* whether the routing actually saves money without hurting quality.

> Source + full write-up: [github.com/yaya-ali/routeiq](https://github.com/yaya-ali/routeiq)

## The idea: route by complexity

Every request hits a classifier that decides how hard it is, then routes accordingly:

| Tier | Examples | Model |
|------|----------|-------|
| Cheap | Formatting, simple Q&A, summarization | small model (Llama 3.1 8B) |
| Strong | Analysis, code, multi-step reasoning, long context | large model (Llama 3.3 70B) |

The v1 classifier is deliberately dumb — keyword and length heuristics, no ML:

```python
REASONING_HINTS = ("step by step", "analyze", "compare", "trade-off", "debug", ...)

def choose_model(prompt: str) -> tuple[str, str]:
    if len(prompt) > 2000:                       return STRONG, "long context"
    if any(h in prompt.lower() for h in REASONING_HINTS): return STRONG, "reasoning keywords"
    return CHEAP, "simple query"
```

Ship the dumb version first, measure it, *then* make it smarter. The response always
reports which model answered and why, so routing decisions are never a black box.

## Budget controls in Redis

The real risk with any routing system is a runaway bill. Each team gets a daily budget
enforced by an atomic, date-keyed Redis counter:

```python
key = f"spend:{team}:{today}"          # the date in the key IS the daily reset
spent = redis.incrbyfloat(key, cost)   # atomic — no races between requests
if spent > DAILY_BUDGET: raise HTTPException(429, "budget exhausted")
```

The date in the key resets the budget for free — tomorrow's requests hit a fresh key.
No cron job, no reset logic. Over budget → HTTP 429 before any money is spent.

## Measuring it — the part most write-ups skip

A cost claim means nothing without a quality check. An eval suite runs every prompt
through both the router and an always-strong baseline, comparing cost *and* answer
quality, and it's wired into CI so a routing change that trades away too much quality
fails the build.

On the current (deliberately reasoning-heavy) eval set:

- **10.2% cost reduction** vs. always using the strong model
- **0% quality drop** on keyword-coverage scoring

That's a modest, *honest* number — savings scale with the share of simple traffic, so a
production mix heavy on formatting and summarization would save far more. The point of
the project isn't the headline figure; it's that the figure is measured and defended,
not guessed.

## What's next

The heuristic classifier is the baseline to beat. The roadmap swaps it for a learned
classifier and proves the upgrade with the same eval harness — plus per-request
tracing and an LLM-as-judge scorer to replace keyword matching.
