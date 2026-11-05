# Camera startup and phone connection

The reported Windows 10 log contains `cap_msmf.cpp ... can't grab frame. Error: -2147483638`. The broken boundary is video capture through Media Foundation. MediaPipe's XNNPACK/feedback-tensor messages show that its graph loaded; they do not explain the camera frame failure. This evidence does not establish the underlying driver, permission or device-contention cause on the user's PC.

## Camera

1. Close every running Checkpoint/Check setup window. Extract the new release into a fresh folder and start **Start Checkpoint.cmd**.
2. In Windows Settings → Privacy (Windows 10), or Privacy & security (Windows 11) → Camera, enable camera access and **Let desktop apps access your camera**. Check the physical privacy shutter/keyboard camera switch. Close Teams, Zoom, OBS and other camera apps.
3. Leave **Track my face** off initially and click **Start camera**. This isolates capture from analysis. The app now tries DirectShow first, then Media Foundation and the Windows default for the selected device. It requires a real frame, retries warm-up reads and does not force an unsupported frame rate. Failed handles are released. It never silently tries another camera device.
4. If Camera 1 is wrong or unavailable, pause and choose Camera 2, then retry. The numbered choices are possible device indices, not a claim that ten cameras are installed. IR/virtual/integrated cameras may occupy different indices.
5. Once your own preview appears, enable **Track my face**. If the face engine fails, the preview stays on and the error appears separately. Pip returns to a neutral appearance and never invents an expression. Optional relaxed-face calibration is not required for capture.
6. If none of the choices work, try the Windows Camera app after closing Checkpoint. If Windows Camera also fails, check its Windows privacy/driver/device error first. If only Checkpoint fails, capture the message under Your camera and the Check setup console output; do not send personal camera frames.

The app sets `OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS=0` before importing OpenCV on Windows, only for its own process. This disables the optional hardware-transform path documented by [OpenCV](https://docs.opencv.org/5.0/main_modules/videoio_flags_base.html); it is not a guarantee that every driver will work. Provider-trained model bytes are unchanged; the MediaPipe task is loaded from a byte buffer so an install folder containing non-ASCII characters does not depend on its file-path handling.

## Phone link will not open

This is independent of camera capture. The dashboard must load even with the camera off. The phone displays derived results from the laptop; it does not run its own camera tracker.

1. Keep Checkpoint open. Connect both devices to the same trusted, non-guest Wi-Fi. In **Phone dashboard**, choose the actual **Wi-Fi** adapter/address, not vEthernet, WSL, a VPN or a disconnected adapter. Wired Ethernet also works if the router allows devices to communicate with Wi-Fi clients. The dialog now labels adapter names, prefers active Wi-Fi and reports when a dashboard connects. A laptop-only `127.0.0.1` address cannot connect a phone.
2. Use **Test this link on the laptop**. If it does not load there, stop sharing, restart Checkpoint and retry. If it loads there but not on the phone, check the selected IP, Windows Firewall, guest/client isolation or a VPN. The laptop test is not proof that the phone is reachable.
3. Keep the URL as **http://**, including its port. Use **Copy pairing link** to avoid a QR-reader issue. After stopping/restarting sharing, rescan the new QR; old tokens are revoked.
4. On a trusted home network, confirm the Windows network profile is **Private**. Click **Copy Private-network firewall fix**, open Windows Terminal as administrator, choose PowerShell, paste and run the copied command. It creates allow rules for the bundled `python.exe` and `pythonw.exe`, only the actual dashboard TCP port, **Private** profile and **LocalSubnet**. Both are covered because Check setup uses python.exe while the normal launcher uses pythonw.exe. The app does not execute this command, disable the firewall or open Public-network access. [Microsoft documents these rule scopes](https://learn.microsoft.com/en-us/powershell/module/netsecurity/new-netfirewallrule?view=win10-ps).
5. Rescan the QR. An explicit existing firewall block or an organisation-managed policy can override an allow rule; check Windows Firewall's allowed apps/rules if previously denied. Router guest/client isolation and VPN routing must be resolved on those devices/networks. Do not disable the whole firewall or forward the port to the internet.

## Verification limits

Camera fallbacks/warm-up/cancellation and tracking-failure isolation use explicit simulated device fixtures. Recorded-video face mapping and browser/native authenticated dashboard updates have separate real software checks. The Windows runner verifies launch, the MediaPipe graph with non-ASCII model-folder handling and generated PowerShell syntax. None of these tests establishes that the user's physical webcam, Wi-Fi, firewall or router now works; that final check must happen on the target PC and phone.
