---
title: "How I Cut LLM Costs by 80% with a Model Router"
date: 2025-04-20 10:00:00 +0200
categories: [AI, Engineering]
tags: [openai, anthropic, redis, cost-optimization, llm]
---

## The Problem

When you're calling GPT-4 for every request — including simple ones like "summarize this in one sentence" — you're burning money unnecessarily. Not every query needs the most powerful model.

## The Idea: Route by Complexity

Classify each incoming query into one of three tiers, then route to the appropriate model:

| Tier | Examples | Model |
|------|----------|-------|
| Easy | Formatting, simple Q&A, summarization | `gpt-4o-mini` |
| Medium | Analysis, code review, multi-step reasoning | `gpt-4o` |
| Hard | Complex research, long-form generation, nuanced judgment | `claude-opus` |

## How Classification Works

A lightweight classifier (itself a cheap model call) scores the query on:
- Length and complexity of the prompt
- Presence of code, math, or multi-step instructions
- Historical patterns for similar queries

```typescript
async function classifyQuery(prompt: string): Promise<"easy" | "medium" | "hard"> {
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: CLASSIFIER_PROMPT },
      { role: "user", content: prompt }
    ],
    max_tokens: 10,
  });
  return response.choices[0].message.content?.trim() as Tier;
}
```

## Budget Controls

The real risk with any routing system is unexpected cost spikes. I used **atomic Redis counters** to enforce hard limits:

```typescript
const current = await redis.incrbyfloat(`budget:${month}`, estimatedCost);
if (current > MONTHLY_CAP * 0.9) {
  await disableExpensiveRoutes();
  await sendSlackAlert(current, MONTHLY_CAP);
}
```

At 90% of the monthly budget, expensive routes shut off and a Slack alert fires. No surprise invoices.

## Results

After two weeks in production:
- **80% of traffic** handled by `gpt-4o-mini`
- **~68% reduction** in monthly API spend
- No measurable difference in user-reported quality

The classifier's own cost (gpt-4o-mini per query) is negligible vs. the savings from avoiding GPT-4 for simple tasks.
