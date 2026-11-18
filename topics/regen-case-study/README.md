# Regen case-study website

**[Open the interactive case study](https://regen-case-study-q23s64yln-anujrai1701-gmailcoms-projects.vercel.app)**

Live Vercel preview. Sign in with your Vercel account if prompted.

The interactive case study is available as a standalone static website on this branch. It needs no account, camera, native runtime, package installation or database. Vercel preview access follows the existing project’s authentication settings.

Branch: `topic/regen-case-study-site`.

`site/` contains the website and readable research, context and feasibility pages. It is generated from the reviewed case study by running:

```bash
python topics/regen-case-study/sync.py
```

To preview locally from the repository root:

```bash
python -m http.server 8123 --bind 127.0.0.1 --directory topics/regen-case-study/site
```

Vercel uses a separate `regen-case-study` project linked to this repository. Its repository-root configuration selects the static `topics/regen-case-study/site` output. No install or build command is needed. Only the website branch should deploy in this project; the shared job-search production project remains separate.

The root `vercel.json` also supports repository-root static deployment when the hosting project has no nested Root Directory set. It cannot override a Root Directory configured in Vercel Project Settings.

The existing native app and OTA release are unaffected. The demonstration uses authored check-ins and fictional persona scenarios.
