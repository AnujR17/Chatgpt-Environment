# Checkpoint 0.6.1 — persistent updates and file-lock repair

Fixes the updater's whole-folder replacement during compatible app-only updates. A Windows sharing violation could abort the swap and reopen the previous 0.4 installation, making an update appear not to persist.

App-only updates now replace only the verified app components. The installation directory, runtime and model binaries stay in place. Temporary file locks are retried; another running copy of this installation is reported before downloading. The verified download is cached and reused on retry. Startup receipts are written atomically, and a real post-start version marker helps verify normal reopening. App updates shows the installation path and actual previous failure message. Failed startup restores the prior components; full-runtime updates keep their separate transactional fallback.

For a legacy 0.4 updater that is stuck on a folder lock, use the small Checkpoint-Updater-Repair.zip once. Extract it, run Repair Checkpoint update.cmd, choose your EXISTING Checkpoint-Windows folder and close Checkpoint/Check setup windows when prompted. The repair uses the existing runtime, verifies the current app-only release and runs the corrected helper. Future updates use Settings > Check for updates > Update and restart; no repeated full download is required. No administrator access, firewall or Windows execution-policy changes are made.

This release keeps the 0.6 character, expression estimates, game-window tracking and player-reported CMA unchanged. Recognition and real-game usefulness limits still apply.

Verification includes cached-download/source checks, component exclusion, blocked second copies, atomic acknowledgements, the existing native Windows restart/rollback tests, component rollback, a deliberately held-open installation directory, actual Qt startup and normal reopening of the updated version. Disposable fixtures do not modify a user's installation.
