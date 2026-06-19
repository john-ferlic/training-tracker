# Cloud routine setup — hands-off daily coach you can chat with

Runs the daily briefing in Anthropic's cloud so it fires even when your Mac is off, pushes you
a coaching summary, and leaves a session you can open and chat into all day.

> Your Strava/Oura tokens never go to GitHub — `.env` and `data/` are gitignored, so GitHub only
> ever holds your code. The tokens go into the routine's **secrets** (step 4), held by Anthropic
> outside the sandbox.

The code side is already cloud-ready (committed). The steps below are the account-side wiring
only you can do.

## 1. Put this repo on GitHub (PRIVATE)

```bash
brew install gh                 # if you don't have the GitHub CLI
gh auth login                   # GitHub.com → HTTPS → log in via browser
gh repo create training-tracker --private --source . --push
```

Or, manually: create an empty **private** repo on github.com, then:
```bash
git remote add origin https://github.com/<you>/training-tracker.git
git push -u origin main
```

## 2. Connect GitHub to Claude

In the Claude app (or claude.ai/code), connect your GitHub account and grant access to the
`training-tracker` repo.

## 3. Create the routine

At **claude.ai/code/routines** (or `/schedule` in the Claude Code CLI):
- **Repo:** `training-tracker`
- **Schedule:** daily, **6:30 AM**, timezone **America/Chicago**
- **Prompt:** paste the full contents of [`cloud/routine-prompt.md`](routine-prompt.md)

## 4. Add your tokens as routine secrets (environment variables)

Copy the values straight from your local `.env`:
- `STRAVA_CLIENT_ID`
- `STRAVA_CLIENT_SECRET`
- `STRAVA_REFRESH_TOKEN`
- `OURA_ACCESS_TOKEN`

You do **not** need `ANTHROPIC_API_KEY` here — the routine *is* Claude, so it writes the
coaching reasoning itself.

## 5. Allow the network the routine needs

The cloud sandbox blocks outbound traffic by default. Add these to the routine's allowed hosts
(without them, `fetch`/`pip` fail silently):
- `www.strava.com` — Strava API
- `api.ouraring.com` — Oura API
- `pypi.org` and `files.pythonhosted.org` — pip install

## 6. Test it

Trigger the routine once manually from the Routines panel. You should get the coaching summary;
open that run as a session and try a follow-up ("why modify?", "pull my last ride"). It will
re-provision the sandbox and answer.

---

### Notes
- **Freshness:** each run re-fetches your last 56 days, so trends/CTL stay current.
- **Long baseline (optional):** to keep history older than 56 days in the cloud, un-gitignore
  `data/workout_history.json` and have the routine commit it each run so it accumulates.
- **After an FTP retest:** update `ftp` in `config/athlete.yaml`, commit, and push — the routine
  picks it up on the next run.
- The routine reuses everything local: same package, same analysis, same plan.
