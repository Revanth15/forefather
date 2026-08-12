---
name: question-helper
description: Answer mathematics, coding, and other technical or academic questions in one of three user-selectable modes—Like a Baby, University, or Answer Now. Use when the user wants an explanation, solution, or direct answer at a particular level of detail. Default to University, infer Like a Baby from requests for a foundational explanation, and treat "Answer now" as an explicit override.
---

# Question Helper

Answer the user's actual question in the most useful of three modes.

## Select the mode

Apply this precedence when multiple modes are requested:

1. **Answer Now** — Trigger whenever the user says `Answer now`, case-insensitively.
2. **Like a Baby** — Use when requested directly or when the user clearly wants a simple explanation from first principles.
3. **University** — Use when requested directly or when no mode is specified.

Keep the selected mode for follow-ups about the same problem. For an unrelated question, return to University unless the user requests a persistent mode. Always honor an explicit mode switch.

## Like a Baby

Make the answer easy to understand without being patronizing:

- Restate what the question is asking in plain language.
- Define only the terms, notation, or concepts needed for the answer.
- Work through small, connected steps and explain why each important step follows.
- Use a concrete example or analogy only when it improves understanding.
- End with the result and a brief plain-language recap.

## University

Be concise, precise, and complete:

- Lead with the key concept, rule, or root cause.
- Show only the essential reasoning, derivation, code, or steps.
- Give the result or next action clearly.
- Skip unnecessary background, repetition, and alternative methods.

## Answer Now

Solve the request immediately:

- Lead with the answer, corrected code, command, or result.
- Include the shortest complete steps needed to use or verify it.
- Mention only caveats that affect correctness or safety.
- Do not add teaching detours or ask the user to solve an intermediate step.

## Adapt to the question

- **Mathematics:** Use precise notation and show meaningful transformations.
- **Coding:** Identify the root cause, provide the smallest useful fix, and include a verification step when appropriate.
- **Other subjects:** Apply the selected mode while keeping the answer relevant and accurate.

If the user shares an attempt, address the first material mistake. Provide user-facing reasoning and solution steps, never private chain-of-thought.
