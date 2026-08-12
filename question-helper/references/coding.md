# Coding guidance

Use this reference for programming and software-engineering questions.

## Like a Baby mode

Assume the user may not yet understand the underlying programming concept.

1. Explain what the program or code is trying to do.
2. Define the important programming concepts involved.
3. Identify the relevant line, expression, component, or error.
4. Explain what the current code actually does.
5. Explain why that causes the problem.
6. Show the fix in a small, focused snippet or diff.
7. Walk through the corrected code in plain language.
8. Explain how to verify that it works.

When introducing syntax such as a function call, optional, closure, promise, async task, loop, generic, protocol/interface, pointer/reference, query, or state binding, define it briefly before relying on it.

Prefer concrete examples over abstract descriptions when the concept is unfamiliar.

## University mode

Start with the root cause or governing concept.

Possible failure classes include:

- syntax or type error,
- incorrect state or data flow,
- async/concurrency issue,
- API contract mismatch,
- algorithm/data-structure issue,
- lifecycle/framework misuse,
- environment/build/configuration issue.

Then:

1. Point to the smallest relevant code area or error message.
2. State the cause concisely.
3. Give the smallest useful code change, command, or diagnostic step.
4. Add one short explanation of why the fix works when needed.

Prefer a minimal diff or focused snippet over rewriting an entire file.

Preserve the user's existing architecture, naming, and conventions when they are not part of the problem.

## Answer Now mode

Provide the direct implementation or fix immediately:

- briefly state the cause when useful,
- give the exact code, command, or configuration change,
- include only the steps required to apply it,
- mention an important caveat or verification command when needed.

If several files must change, organize the solution by file.

## Debugging priorities

- Use exact compiler/runtime error text when available.
- Distinguish the root cause from secondary errors.
- Do not invent APIs, package names, methods, or configuration keys.
- For version-sensitive frameworks or libraries, verify current documentation with available tools when necessary.
- For destructive commands or migrations, state the risk before the command and provide a safer option when practical.
