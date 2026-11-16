# Checkpoint session study

Work isolated on **topic/checkpoint-session-20261116**. Existing topic/checkpoint, main and the stable OTA channel are unchanged.

[App and branch instructions](app/README.md) · [Service changes and limits](app/docs/SESSION-BRANCH.md) · [Windows review builds](https://github.com/AnujR17/Chatgpt-Environment/actions/workflows/checkpoint-session-review.yml)

The branch adds a quieter session interface, CMA-informed reset/focus choices, dismissal for the rest of a session, optional reset feedback and an action-aware CMA report. It preserves the existing local face tracker, overlay and phone pairing. No new emotion-detection accuracy is claimed.

Windows packages are provided as workflow artifacts for review, with no OTA publication.
