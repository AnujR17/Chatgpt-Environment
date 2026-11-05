# Checkpoint with Nori — current Windows build

[Download the Windows ZIP](https://github.com/AnujR17/Chatgpt-Environment/releases/download/checkpoint-v0.2.0-pip-preview.1/Checkpoint-Windows-Preview.zip). Extract it into a new folder and run **Start Checkpoint.cmd**. Python and native runtime libraries are included.

1. Tick **Track face and hands**, then **Start camera**. Default facial-movement mapping drives Nori directly.
2. Click **Show Nori** for the transparent, frameless, click-through desktop buddy.
3. Click **Phone dashboard**, scan its QR on the same trusted Wi-Fi, and keep Checkpoint open. The phone view runs in its browser and receives derived state, not images.
4. **Settings** offers optional HSEmotion categories, movement strength, Getting Over It observation, game-focused input timing and quiet nudges. **Set my neutral face** is optional, in-memory relaxed calibration.
5. **Report** on the laptop or **Download session report** on the phone exports the source-labelled timeline. Download before closing the app to retain it.

[Full controls and limits](PIP-COMPANION.md) · [Video list, actual training and model comparison](VIDEO-AND-MODEL-RESEARCH.md) · [Release verification](../../RELEASE-VERIFICATION.json).

No posed personal emotion-photo collection is required. The categorical model improved on the matched acted-video comparison, but personal webcam/gamer affect accuracy remains unverified. Neutral fallback is a visual appearance, not a claim that an unobserved person feels neutral. Actual device/game performance, physical phone networking and user benefit still need testing.

Camera will not start, or the phone QR link will not load? See [camera and phone troubleshooting](CAMERA-AND-PHONE-TROUBLESHOOTING.md). The updated build tries DirectShow first and lets you choose another camera. The pairing dialog includes adapter names, a laptop link test and an explicit Windows Private-network firewall helper.
