# Checkpoint 0.5 — responsive Nori reflection

The slow 20-second observation window and 30-second display lock are removed. Live reflection uses adaptive feature smoothing, short evidence dwell and a separate recent trend. Clean sustained signals changed poses in 0.5–0.9 seconds in deterministic replay; this excludes camera/model startup and is not a webcam latency guarantee. Manual check-ins no longer freeze the live character.

Camera preview and model inference run independently, with one latest pending frame and stale-result rejection. Live reflection, Movement test and My check-in are visible tabs. Start face tracking enables analysis and opens the selected camera in one deliberate action. Model failure leaves the preview available.

Pretrained scores now influence default recognition. Mouth width alone cannot be a smile; cheek/model support and conflicting signals are checked. Brow movement alone cannot establish anger. Authored Nori poses retain subtle laugh-like motion and visible-teeth variations. Ambiguity/occlusion returns to a flat neutral appearance with an explicit unclear label. This does not establish reliable eight-class recognition or 43 inferred emotions.

Two alternative internet models were actually compared on the same 208 acted clips: B2 tied the current B0 at 62.5% accuracy while slower; MobileFaceNet scored 60.58%. Existing weights remain selected. Sources, per-class results, limitations, alternatives and the plan are in docs/REBUILD-RESEARCH-AND-PLAN.md. Local video smoke checks still show misses and substantial uncertainty. No training or invented participant results are claimed.

CMA reports remain based on your own check-ins. Phone reflection/trend, PDF export, frameless dragging, Windows camera fallback and update/rollback behaviour are preserved. Use Settings → Check for updates → Update and restart. Compatible installations receive the small app package; full ZIP is for fresh installs or the automatic fallback. Runtime and bundled model weights are unchanged. Capture stays off after restart.
