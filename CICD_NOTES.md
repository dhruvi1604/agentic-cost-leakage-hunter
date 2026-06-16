# CI/CD Pipeline — My Study Notes & Demo Prep

> My project: Agentic Cost Leakage Hunter (Streamlit + Groq LLM app)
> GitHub: dhruvi1604/agentic-cost-leakage-hunter
> Docker Hub: dhruviparekhh/cost-leakage-hunter

---

## 1. The big picture — what is CI/CD?

**One line:** CI/CD = automatically **testing** and **shipping** my code every time I change it, so broken code never reaches production and shipping happens the same way every time.

- **CI = Continuous Integration** → the *testing* half. "Is the new code good?"
- **CD = Continuous Delivery** → the *shipping* half. "Build the image and push it."

**MLOps vs CI/CD:** CI/CD is ONE tool inside MLOps. MLOps is the whole factory (data → train → deploy → monitor → repeat). CI/CD is the build-test-ship machine inside that factory.

---

## 2. The Docker flow (the foundation)

```
1. Change code
2. docker build   ← make the image
3. docker push    ← upload to Docker Hub
4. docker pull    ← download on the server
5. docker run     ← run it
```

**Before the pipeline:** I did steps 2 & 3 BY HAND every time.
**After the pipeline:** GitHub does steps 2 & 3 automatically. I just `git push`.

Two different "pull"s (don't confuse them!):
- `docker pull` = DOWNLOAD a finished image.
- "pull request" = a PROPOSAL to add code into the project (nothing to do with downloading).

---

## 3. Why CI/CD matters (more than just automation)

1. **Quality gate (the real hero):** tests run BEFORE shipping. Test fails → no image built. Can't ship broken code.
2. **Consistency:** builds on a fresh identical machine every time. No "works on my machine."
3. **Teamwork at scale:** everyone just `git push`, pipeline enforces one tested process.
4. **History & rollback:** every image tagged with commit ID → roll back to any version.
5. **Speed + confidence:** ship more often with less fear.

---

## 4. What we built (the files)

| File | Purpose |
|---|---|
| `Dockerfile` | Packages the app into an image |
| `.dockerignore` | Keeps `.env`/junk out of the image |
| `tests/test_features_unit.py` | 2 tests on feature logic |
| `tests/test_llm_backends.py` | 2 tests on LLM fallback + key guard |
| `.github/workflows/ci-cd.yml` | THE PIPELINE |
| GitHub Secrets | DOCKERHUB_USERNAME + DOCKERHUB_TOKEN |

---

## 5. The YAML file — every part explained

Mental model: the YAML is a **note for a robot** that lives on GitHub. It does nothing until I push. Then it reads the note top-to-bottom and follows it.

Every CI/CD file answers 3 questions:
1. **WHEN** should it run? → `on:`
2. **WHAT** work happens? → `jobs:`
3. **HOW** is each piece done? → `steps:` (either `uses:` a ready-made tool, or `run:` a terminal command)

### The skeleton
```yaml
name: <title>          # nickname (cosmetic)
on: <events>           # WHEN to wake up
jobs:                  # WHAT to do
  <job-name>:
    runs-on: <machine> # WHERE (which computer)
    needs: <job>       # ORDER (wait for another job)
    if: <condition>    # only run if true
    steps:             # HOW — to-do list, runs top to bottom
      - uses: <tool>   # borrow a ready-made action
      - run: <command> # type a terminal command
```

### Block 1 — WHEN (the triggers)
```yaml
name: CI/CD
on:
  push:
    branches: [main]        # wake up when I push to main
  pull_request:
    branches: [main]        # also wake up when someone proposes a change to main
```

### Block 2 — JOB 1: test
```yaml
jobs:
  test:
    runs-on: ubuntu-latest          # fresh Ubuntu machine (can be windows-latest etc.)
    steps:
      - name: Checkout code
        uses: actions/checkout@v4   # download my code onto the empty machine (STEP ZERO)

      - name: Set up Python 3.10
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"    # 'with' = settings handed to the tool

      - name: Install dependencies
        run: |                      # run = terminal commands
          pip install -r requirements.txt
          pip install pytest

      - name: Run unit tests
        run: pytest tests/test_features_unit.py tests/test_llm_backends.py -v
```
Key idea: the robot starts on a BLANK machine, so checkout (download code) must come first.

### Block 3 — JOB 2: build-and-push
```yaml
  build-and-push:
    needs: test                     # THE GATE: only run if 'test' job passed
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'  # only on push to main
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4   # another fresh machine, so download code again

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}   # read secret from GitHub vault
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push image
        uses: docker/build-push-action@v6
        with:
          context: .                # build using files in this folder (has Dockerfile)
          push: true                # after building, also upload to Docker Hub
          tags: |                   # apply TWO labels to the image:
            ${{ secrets.DOCKERHUB_USERNAME }}/cost-leakage-hunter:latest
            ${{ secrets.DOCKERHUB_USERNAME }}/cost-leakage-hunter:${{ github.sha }}
```

### Why 2 tags? (the question that confused me)
- `:latest` → always points to the NEWEST build (moving pointer, convenient)
- `:<commit-id>` → permanent version stamp, NEVER moves → rollback point
Both labels point to the SAME image (same digest). One image, two names.

`${{ secrets.X }}` = "fetch secret X from the GitHub repo vault." Secrets live in
Settings → Secrets and variables → Actions. Never in the code.

---

## 6. The full story (say this out loud)

When I push to main → GitHub wakes up → runs JOB 1 (test) on a fresh Ubuntu machine:
download code → install Python → install deps → run tests. If any fail, STOP.
If pass → JOB 2 (build-and-push) on another fresh machine: log into Docker Hub →
build image → push with 2 tags. Result: a fresh, tested image on Docker Hub, fully automatic.

---

## 7. DEMO SCRIPT for tomorrow

1. Show the YAML: "Two jobs — test, then build-and-push."
2. "I'll change one line of code." (add a comment to any file)
3. Push it:
   ```
   git add .
   git commit -m "demo change"
   git push
   ```
   Say: "I'm NOT running docker build or docker push. I only pushed code."
4. Open GitHub → Actions tab → point at the new yellow run: "It's testing automatically."
5. Wait for green: "Tests passed, so it built and pushed the image. If a test failed, it would stop."
6. Open Docker Hub → Tags → point at the brand-new commit tag: "Fresh image, built automatically."

**Closing line:** "That's CI/CD — every change is tested and shipped the same way every time,
with version history to roll back, and no broken code can get through."

### Prep checklist
- [ ] Terminal open at project folder
- [ ] GitHub Actions tab open
- [ ] Docker Hub Tags tab open
- [ ] Internet working

### Curveball Q&A
- "What if a test fails?" → build job has `needs: test`, so it won't run. No broken image ships.
- "Why two tags?" → latest = newest; commit-id = permanent snapshot for rollback.
- "Where's the password?" → GitHub Secrets, encrypted, never in code. Pipeline reads at runtime.
- "What's checkout?" → each job runs on a blank machine, first step downloads my code onto it.
- "Can it run on Windows?" → yes, `runs-on: windows-latest`. Ubuntu is just cheap/common/matches servers.

---

## 8. What's next (after the demo)
1. docker-compose.yml (run config as code)
2. Auto-deploy (server pulls + restarts itself automatically)
3. Monitoring / LLMOps (track tokens, cost, latency, errors — fits the cost-leakage theme)
4. Real tests for business logic (leakage detection, savings math)
