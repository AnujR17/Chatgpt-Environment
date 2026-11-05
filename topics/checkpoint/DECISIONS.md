# Checkpoint decisions

- 2026-11-05: User chose AnujR17/Chatgpt-Environment and explicitly required all work in a branch. Use topic/checkpoint; preserve main.
- Keep app source in topics/checkpoint/app and use a GitHub Release asset for the 165 MB portable Windows package rather than checking a large runtime ZIP into Git.
- Native PySide6 UI; 43 poster-inspired illustrated vocabulary cards, eight common choices first. CMA is independent self-report, never inferred from a card illustration or expression.
- Keep expression inference opt-in and experimental. The existing classifier is not a validated mood/frustration estimator and failed production release gates.
- The local GitHub upload service rejected credentials. Use the branch workflow to rebuild from the exact reviewed vendor hashes and publish via its GitHub token. Native Windows launch subsequently passed. Physical camera and target-device checks remain unverified. All code/docs stay in topic/checkpoint; main is unchanged.
