# BACKLOG

Critical:
1. Keep ~/bmo-context as the canonical truth source.
2. Make the host bot read context files before answering setup questions.
3. Stop trusting stale NemoClaw registry state over openshell sandbox list.
4. Re-seed worker bootstrap when a new sandbox is created.
5. Keep host vs worker responsibilities explicit.
6. Implement restart recovery protocol: at session start, read host context first, check TASK_STATE.md and WORK_IN_PROGRESS.md, inspect git status before asking user to restate anything.

Important:
6. Add a one-command worker status check.
7. Add a one-command context reseed.
8. Clean up naming consistency.
9. Turn planning docs into implementation-ready tasks.
10. Reduce reply fragmentation.

Nice-to-have:
11. Easier worker auth for openclaw tui.
12. Add a project-state snapshot generator.
13. Preserve important docs in a real repo later.
