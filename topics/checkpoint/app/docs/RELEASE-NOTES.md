# Checkpoint — Expressive Pip and in-app updates

Pip now shows smaller smiles and open smiles with gentle happy eyes and mouth movement. Drawn brows tilt inward correctly and read more firmly. Continuous camera changes no longer restart a slow animation, so brief expressions can appear without making the body shake. Neutral remains flat; missing tracking stays neutral-looking with explicit tracking status. Desktop and phone share the updated shapes and reduced-motion setting. These are physical-movement mappings, not new validated mood or laughter classes.

Install this release once, then use **Settings → Check for updates → Update and restart** for future releases. A small verified app package reuses compatible runtime/models; the full package is downloaded automatically when they change. Staging leaves the running app intact, preserves a backup and rolls back if the new app fails its startup acknowledgement. Saved check-ins remain in normal Windows app data. Updates stop capture and phone sharing for the restart; they do not run silently or change Windows Firewall.

Extract the full ZIP into a fresh folder and run **Start Checkpoint.cmd**. Select your camera, start its preview, then enable **Track my face**. Use **Show Pip** for the transparent click-through companion. **Phone dashboard** pairs on the same trusted local Wi-Fi. Windows DirectShow-first capture, alternative camera selection and Private-network phone troubleshooting remain included.

Provider-pretrained model bytes are unchanged. Native render previews use synthetic face signals; software checks are not proof of accuracy on a user's webcam, game or felt emotion. Current Getting Over It cues remain experimental. See the included expression, update and troubleshooting guides for behaviour and verification limits.

For an existing working 0.2.1 camera-fix installation, Checkpoint-App-Update.zip is a 256 KB bootstrap patch: close all Checkpoint/Check setup windows, extract and copy its contents into the existing Checkpoint-Windows folder, replacing files. Runtime/model dependencies are identical. Restart, then use Settings → Check for updates for later releases. Use the full ZIP for a fresh install or older builds.

To test another person’s recorded face, enable Track my face and choose Open video, then select a local MP4/MOV/AVI/MKV. One clear face and repeated neutral/smile/open-smile/brow movements are useful for checking the mapping. Audio is not analysed and this is not model training or proof of internal emotion.
