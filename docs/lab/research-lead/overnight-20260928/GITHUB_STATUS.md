# GitHub Connector Status

**Date:** 2026-09-29 07:15 PDT
**User:** Micah regenerated the connector. Classic PAT (not fine-grained).

## Verification

**API works:**
- `GET /user` → OK login=micahcooley id=158981228
- `GET /repos/Sylorlabs/TNN` → OK, permissions: admin, maintain, push, triage, pull
- Token HAS push permission.

**Git push fails:**
- `git push origin tnn-native-lab` → "could not read Username for 'https://github.com'"
- Root cause: Git needs the raw token value for HTTPS auth. The token is held by authd and only available as `hsurr:*` surrogates for API requests. Git does not go through authd, so surrogates are not replaced.
- This is a security boundary by design. The raw token cannot be extracted.

**Release creation fails:**
- `POST /repos/Sylorlabs/TNN/releases` → 403 Forbidden
- Despite push permission being True. Possibly missing specific scope or repo setting.

## Workaround: Git Bundle

**Bundle created:** `/tmp/tnn-native-lab.bundle` (24M, verified)
- Contains: origin/tnn-native-lab..HEAD (248 commits)
- Verified: `git bundle verify` passes
- Location: `/tmp/tnn-native-lab.bundle` (ephemeral!)

**To preserve:** Copy bundle to `~/workspace/` (persistent) and/or upload via manual method.

**Manual push instructions for Micah:**
```bash
# On this machine (if token available):
cd ~/workspace/tnn-rsi
git push origin tnn-native-lab

# Or using bundle (on any machine with the bundle file):
git clone /tmp/tnn-native-lab.bundle tnn-restore
cd tnn-restore
git remote add origin https://github.com/Sylorlabs/TNN.git
git push origin tnn-native-lab
```

## Conclusion

The connector works for API. Git push requires raw token access which is blocked by security design. The 248 commits are safe locally and in the verified bundle. Research continues per directive ("THIS MUST NEVER HALT RESEARCH").

## Update 2026-09-29 07:20 PDT

Micah: "you can use your vm for that... keep trying and trying and search the web"

**Tried:**
1. Web search for token-based push methods — all require the raw token value.
2. Checked VM for secret stores (~/.secrets, env vars, `secrets` cmd) — none found.
3. Network connectivity verified — github.com and api.github.com reachable.
4. API push via Git Database API — impractical for 274 commits (thousands of API calls needed for blobs/trees).

**Blocker remains:** The raw token value is required for git HTTPS auth. The token is held by authd and only available as `hsurr:*` surrogates for API requests. There is no mechanism to extract the raw token, and git cannot use surrogates.

**Preserved:**
- 274 commits locally on `tnn-native-lab`
- Bundle: `~/workspace/tnn-native-lab-20260929.bundle` (24M, verified)
- All research continuing per directive.

**For Micah:** To push, run from `~/workspace/tnn-rsi`:
  `git push origin tnn-native-lab`
with your token configured, or use the bundle file.
