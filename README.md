<p align="right"><strong>English</strong> | <a href="README_zh.md">中文</a></p>

# Flow Coding

> Closing the last mile of the inner development loop, on top of Vibe Coding.

Vibe Coding lets AI write code for you. Flow Coding lets AI write code for you, then automatically opens the browser, navigates to the right page, fills in test data, and compares screenshots — all you have to do is look at the result and say "correct" or "not correct."

Your attention never leaves the intent layer. This is flow.

---

## Table of Contents

- [1. The Problem: Vibe Coding's "Last Mile"](#1-the-problem-vibe-codings-last-mile)
- [2. Definition: What Is Flow Coding](#2-definition-what-is-flow-coding)
- [3. Paradigm Evolution: Three Stages of the Inner Development Loop](#3-paradigm-evolution-three-stages-of-the-inner-development-loop)
- [4. Core Principles](#4-core-principles)
- [5. Tech Stack](#5-tech-stack)
- [6. Hands-on Example](#6-hands-on-example-a-self-healing-loop-driven-by-a-ui-mockup)
- [7. Applicability Boundaries](#7-applicability-boundaries)
- [8. FAQ](#8-faq)
- [9. Related Concepts](#9-related-concepts)

---

## 1. The Problem: Vibe Coding's "Last Mile"

[Vibe Coding](https://karpathy.ai) (Andrej Karpathy, 2025) changed how code is produced:

```
Traditional:  Think → Hand-write code → Run → Debug → Repeat
Vibe:         Describe intent → AI generates code → Run → Debug → Repeat
```

Code production sped up by 5-10x. But a new bottleneck emerged: **the verification step is still manual.**

Every time the AI generates code, you still have to:

1. Open the browser
2. Log into the test account
3. Click through menus to navigate to the target page
4. Fill in test data
5. Eyeball whether the UI matches expectations
6. Switch back to the chat window and tell the AI what's wrong

These 6 steps repeat dozens of times a day. Code production takes 3 seconds; verification takes 30.

**Flow is broken at the verification step. Flow Coding solves exactly this problem.**

---

## 2. Definition: What Is Flow Coding

**Flow Coding** is a software development paradigm: on top of Vibe Coding (AI-assisted code generation), it fully automates the verification step as well — using browser automation tools (such as Playwright) — so that the developer's attention always stays at the level of "expressing intent" and "judgment," uninterrupted by any intermediate operation, thereby continuously remaining in the Flow State as defined by Mihaly Csikszentmihalyi.

### Naming Rationale: Why "Flow"

"Flow" (川流, "flowing river" in the original Chinese) fits this paradigm better than "Flow State (心流, the psychological state)." It carries two meanings:

1. **The river of process**: Development is no longer a stop-and-go sequence of "write code → stop to verify manually → write again," but a continuous, ever-forward process of "intent → generation → verification → fix" that flows like a river — *flowing without ceasing*.
2. **The confluence of two sources**: The production side (Vibe Coding) and the verification side (Dev Automation) — two automated tributaries — merge into a single mainstream, forming an end-to-end closed water system. As Confucius said by the river, "It flows on like this, never ceasing day or night"; the inner development loop keeps flowing, never stalling.

"Flow State" describes the developer's *psychological state* (the result); "flowing river" describes the *workflow form* (the means) that achieves it — using a continuous stream of automation to carry and sustain the developer's flow.

### The Formula

```
Flow Coding = Vibe Coding (production-side automation) + Dev Automation (verification-side automation)
```

### The Key Difference: The Feedback Mechanism

| Paradigm | Feedback Mechanism | Verification Scope | Feedback Speed | Flow Preservation |
|----------|--------------------|--------------------|----------------|-------------------|
| Vibe Coding | Unit Test | Unit-level (function/class) | Fast (ms) | Partial (still needs manual E2E verification) |
| Flow Coding | E2E Test | End-to-end (full user flow) | Medium (s) | Full (verification fully automated) |

Vibe Coding is based on unit-test feedback: AI generates code → run unit tests → adjust based on assertion failures → repeat. Feedback is fast but limited in scope; it cannot verify cross-component integration or real user scenarios.

Flow Coding is based on end-to-end test feedback: AI generates code → Playwright automatically navigates to the target page → fills in real data → compares via screenshots/assertions → adjusts based on the result → repeat. Feedback is slightly slower but covers the complete user path, verifying "what the user actually sees and experiences."

### The Developer Only Does Three Things

| Step | What You Do | What the System Does |
|------|-------------|----------------------|
| 1. Express intent | Describe the requirement in natural language | AI generates code |
| 2. Trigger verification | Say "run it" | Playwright auto-navigates, fills forms, screenshots, compares |
| 3. Judge | Look at the screenshot/report, say "correct" or "this part is wrong" | Records the result, waits for the next round of intent |

You never leave the chat window. Your hand never touches the mouse to poke at a test browser.

---

## 3. Paradigm Evolution: Three Stages of the Inner Development Loop

**Stage 1: Traditional Development — Fully Manual End-to-End**

```
[Hand-write code] → [Manually navigate browser] → [Eyeball verification] → [Change code]
       slow                    slow                       slow                  slow
——Attention repeatedly interrupted; effective coding < 4h/day——
```

**Stage 2: Vibe Coding — Only the Production Side Is Automated**

```
[Intent → AI generates code] → [Manually navigate browser] → [Eyeball verification] → [Change prompt]
          fast                        still slow                  new bottleneck          slow
——Flow is broken here——
```

**Stage 3: Flow Coding — Production + Verification Both Closed**

```
[Intent → AI generates code] → [Playwright one-click jump] → [Auto screenshot/compare] → [Change prompt]
          fast                          fast                          fast                     fast
——Flow uninterrupted; Flow State maintained all day——
```

---

## 4. Core Principles

### Principle 1: Verification-Side Automation Is the Ceiling of Vibe Coding

The core risk of Vibe Coding is the AI generating code that "looks right but is actually wrong." How broadly a team dares to use vibe coding depends on how strong its verification ability is.

**The more automated the verification, the larger the safe boundary of vibe coding.**

### Principle 2: Meta-Automation

Under the Flow Coding paradigm, the Playwright script itself can also be vibe coded:

```
Developer: "Write me a Playwright script: log into the test account, go to the inventory page, fill in three test records"
AI:        → Generates the Playwright script
Developer: "Run it"
System:    → Playwright executes the script → returns screenshots
```

This is using AI-generated automation scripts to automate the verification of AI-generated code — recursive productivity gains.

### The Self-Healing Loop: Verification Results Flow Directly Back to the Coding Agent

In the example above, the endpoint of "returns screenshots" is the developer — the developer looks at the screenshot, judges whether it's right, and tells the AI. But the real power of meta-automation is this: verification results don't need to pass through the developer; they can **flow directly back to the Coding Agent, which autonomously judges and fixes the problem.**

**Traditional Vibe Coding loop (human-in-the-loop judgment):**

```
Developer —(intent)→ AI generates code —(run)→ verification result —(screenshot)→ Developer —(judge)→ AI fixes
                                                                                       ↑
                                                                       ——attention must intervene——
```

**Flow Coding self-healing loop (human only at start and end):**

```
Developer —(intent)→ AI generates code —(run)→ verification result —(screenshot/error)→ AI analyzes autonomously
                                                                                              ↓
                                                                  locate problem → fix code → re-verify
                                                                                              ↓
                                                                                          passed?
                                                                                        no ↙    ↘ yes
                                                                              continue fix loop    → Developer —(see final result)→ "OK"
           ↑
——developer's attention only at the intent layer and the final judgment layer——
```

This means Flow Coding has two operating modes:

| Mode | Human Involvement | Use Case | Loop Speed |
|------|-------------------|----------|------------|
| Human-judgment mode | Developer confirms every verification round | Low-trust layer (core algorithms / security paths) | Limited by human response speed |
| Self-healing mode | Only the starting intent + final confirmation | High-trust layer (CRUD/UI/boilerplate) | Limited only by agent reasoning speed |

In self-healing mode, after the Coding Agent gets the Playwright screenshot, it can:

1. Visual comparison: pixel-diff against the design mockup or the previous round's screenshot to locate rendering deviations.
2. Error parsing: read console error / network error / assertion failure to locate the root cause.
3. Autonomous fixing: modify code based on diff + errors, then re-trigger verification.
4. Convergence judgment: when the screenshot matches the baseline and all assertions pass, report "done" to the developer.

The developer's attention shifts from "needing to confirm every round" to "only looking at the last round" — attention conservation upgrades from "reducing switches" to "eliminating the attention cost of intermediate rounds."

#### Scope of Self-Healing: End-to-End, Not Just the Frontend

Self-healing is **not limited to modifying frontend code**. Flow Coding verifies **end-to-end product feature integrity**, so when a problem is encountered it must:

1. **Locate the source first**: based on console error / network error / assertion failure / API response, decide whether the root cause lies in the frontend, backend, data layer, or API contract.
2. **Fix at the correct location**: both frontend and backend code may be modified, following "minimal upstream fix over downstream workaround" — fix the root cause rather than mask the symptom.

#### Boundary of Self-Healing: The 3 × 3 Rule (Preventing Infinite Iteration)

The self-healing loop **forbids unbounded iteration**. It uses a 3 × 3 convergence strategy:

- **Max 3 attempts per direction**: along the same fix direction (same root-cause hypothesis), iterate at most 3 corrective attempts.
- **Max 3 direction switches**: if one direction still fails after 3 attempts, the hypothesis is judged wrong — switch to a new direction (new root-cause hypothesis); at most 3 direction switches.
- **Stop at the ceiling and report back**: when the 3 × 3 limit (max 9 attempts) is reached without convergence, halt the auto loop, summarize each direction's attempts and failure evidence, and hand back to the developer.

```
Direction A: attempt 1 → attempt 2 → attempt 3   (unresolved, switch direction)
Direction B: attempt 1 → attempt 2 → attempt 3   (unresolved, switch direction)
Direction C: attempt 1 → attempt 2 → attempt 3   (still unresolved → stop, report to developer)
```

This ensures self-healing converges efficiently at the high-trust layer while not falling into pointless "repeated trial and error."

### Principle 3: Attention Conservation

A developer's attention is a scarce resource. Every switch from "chat window" to "browser" and back carries a ~15-second context-switching cost (called Attention Residue in cognitive psychology, Sophie Leroy, 2009). The goal of Flow Coding is to drive the number of switches to zero.

This principle is not just a time-management slogan — it has a solid neuroscientific basis.

#### The Prefrontal Cortex: The Command Center of Attention

The **Prefrontal Cortex (PFC)** is the core of the brain's executive control system, responsible for three key functions:

| PFC Function | Manifestation in Development | Cost on Multitask Switching |
|--------------|------------------------------|------------------------------|
| Working memory (Dorsolateral PFC) | Holding the current function's context, variable dependency chain, call stack | Each switch must clear and rebuild working-memory content |
| Inhibitory control (Right Inferior PFC) | Suppressing irrelevant thoughts, focusing on the current intent | After switching, must re-suppress residual thoughts from the previous task |
| Task-set reconfiguration (Medial PFC / ACC) | Switching from "write code" mode to "verify UI" mode | Must load an entirely new rule set and goal hierarchy |

The metabolic characteristics of the PFC make it the most "expensive" brain region: it relies on slow glutamatergic signaling, and its glucose consumption rate is 2-3x that of the motor cortex. This means the PFC's resources are hard-limited — not "allocate more if you just try harder," but a physiological ceiling.

#### Multitask Switching: Functional Prefrontal Impairment

Neuroscience holds a sobering finding: **the impact of frequent task switching on the prefrontal cortex resembles mild prefrontal impairment.**

| Typical Symptoms of Prefrontal-Damage Patients | Cognitive Performance of Frequent Multitaskers |
|------------------------------------------------|------------------------------------------------|
| ✗ Reduced working-memory capacity | ← After switching, must reload context, losing the "flowing" task state |
| ✗ Weakened ability to inhibit irrelevant stimuli | ← Attention Residue: the previous task's thoughts "linger" into the current one |
| ✗ Increased task-startup latency | ← Each switch incurs a 200-500ms "task-set reconfiguration" delay (Rubinstein et al., 2001) |
| ✗ Rising error rates | ← Rule confusion: carrying task A's assumptions into task B |
| ✗ Distorted time estimation | ← Subjectively feels like "just a glance" but actually took 45 seconds |

This is not a metaphor. The classic experiment by Rubinstein, Meyer & Evans (2001) showed that even in a controlled lab doing simple classification-task switching, subjects' reaction times increased by 200-500ms and error rates rose — and these subjects' prefrontal cortices were perfectly healthy. Multitask switching makes a healthy brain temporarily exhibit the characteristics of a damaged one.

For developers, the consequences of this "functional impairment" are more severe, because software development demands far more of working memory and inhibitory control than a lab classification task: you must simultaneously hold the dependencies of 5-10 variables, an implicit state machine, and the intent of "what behavior the user expects" — all residing in PFC working memory. Every switch clears it all.

#### Why "Just a Glance" Is Not Zero-Cost

Developers often have an illusion: switching to the browser "just for a glance" takes only 2 seconds. But cognitive science data tells us otherwise:

**Breaking Down the Real Cost of "Just a Glance"**

```
0.0s   Press Alt+Tab
0.2s   Visual adaptation to the browser screen
0.3s   PFC begins loading the "verification mode" task set
0.3s   Attention Residue: the prior context is still active, occupying working-memory slots
5-30s  Process verification information (look at UI / read errors)
0.5s   Switch back to the IDE
0.3s   PFC reloads the "coding mode" task set
——10-15s of brain-network context rebuilding: which variables was I just using? what were they called?——

Total: 30-78 seconds of cognitive overhead, most of it unconscious
```

Key insight: **the cost is not the switching action itself (under 0.5s), but the unloading and reloading of the PFC task set — like restarting a server that loaded 10GB of data: the restart takes 30 seconds, but reloading the data takes 5 minutes.**

#### The Neuroscientific Argument for Flow Coding

```
Traditional development (frequent switching):
PFC state:     [coding mode] → [load] → [verify mode] → [load] → [coding mode] → [load] → ...
Working memory: load → clear → rebuild → clear → rebuild → ...
Total attention cost: high (continuous prefrontal drain)

Flow Coding (zero switching):
PFC state:     [coding mode] ——sustained → sustained → ... (only once, until the task is done)
Working memory: load once, use continuously (accumulating, not repeatedly clearing)
Total attention cost: low (only the intent layer and the final judgment layer)
```

---

## 5. Tech Stack

Flow Coding does not depend on any specific tool, but the following is the most mature combination today:

### Production Side (Vibe Coding)

| Component | Recommended Tool | Notes |
|-----------|------------------|-------|
| AI code generation | Windsurf Cascade / Cursor / GitHub Copilot | In-IDE conversational code generation |
| Context management | Project-level Rules / AGENTS.md | Let the AI understand project conventions |
| Prompt assets | Team Prompt Library (Wiki / Git) | Accumulate efficient prompt templates |

### Verification Side (Dev Automation)

| Component | Recommended Tool | Notes |
|-----------|------------------|-------|
| Browser automation | Playwright (Python / Node) | Cross-browser, auto-wait, multi-context isolation |
| State jump | Playwright script + Mock Token | One-click jump to the page state to be verified |
| Visual regression | `page.screenshot()` + pixelmatch | Pixel-level UI comparison |
| E2E assertions | Playwright Test Assertions | Functional correctness verification |
| Component isolation | Playwright Component Testing | Lightweight UI verification without a backend |

### Connection Layer

| Component | Implementation | Notes |
|-----------|----------------|-------|
| One-click trigger | IDE Task / npm script / Makefile | The developer triggers it just by saying "run it" in the chat window |
| Result return | Screenshot files + JSON report | The AI can read screenshots and reports to enter the next iteration |

### Reusable Template: Playwright (TS) Verification-Side Scaffold

Below is an out-of-the-box Playwright TS template. Convention: **the verification side uses only Playwright TS scripts, with no Python test scripts**, at a uniform resolution of 1920×1080. Place the two files in a standalone `test/e2e/` directory to form a self-contained verification project.

**`test/e2e/package.json`**

```json
{
  "name": "<project>-e2e-tests",
  "private": true,
  "description": "E2E tests (Playwright)",
  "scripts": {
    "test": "npx playwright test",
    "test:headed": "npx playwright test --headed",
    "report": "npx playwright show-report"
  },
  "devDependencies": {
    "@playwright/test": "^1.60.0"
  }
}
```

**`test/e2e/playwright.config.ts`**

```ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: ".",
  timeout: 150_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  retries: 1, // Phase 4: Self-healing - retry once on failure
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: process.env.FRONTEND_URL || "http://localhost:3000",
    trace: "on-first-retry",
    video: "on-first-retry",
    screenshot: "on",
    headless: false, // Show browser window for visual confirmation
    launchOptions: {
      slowMo: 500, // Slow down operations for better visibility
    },
  },
  projects: [
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 1920, height: 1080 }, // Flow Coding standard resolution
      },
    },
  ],
});
```

**Initialization and Running**

```bash
cd test/e2e
npm install
npx playwright install chromium
npx playwright test               # run all specs
npx playwright test <spec>.spec.ts  # run a single spec
```

**Template Conventions**

- **TS only**: all verification logic (including API assertions) is written in `*.spec.ts`, calling the backend directly via `page.request`, with no Python scripts.
- **Fixed resolution**: viewport unified at 1920×1080 to ensure the screenshot baseline is reproducible across machines.
- **Self-healing friendly**: `retries: 1` + `trace/video/screenshot` make it easy for the AI to read failure context and auto-fix.
- **Visual confirmation**: `headless: false` + `slowMo` make it easy for the human to judge at the endpoint.

---

## 6. Hands-on Example: A Self-Healing Loop Driven by a UI Mockup

A complete example that ties together Principles 1-4: verification-side automation (Principle 1), meta-automation + self-healing loop (Principle 2), attention conservation (Principle 3), and layered trust (Principle 4).

Scenario: an SCM inventory-alert dashboard page — a fully automated loop from UI design mockup to code implementation.

### Step 1: Design the UI Mockup

The developer uploads a Figma screenshot or hand-drawn wireframe in the chat window:

```
Developer: [uploads inventory_alerts_mockup.png]
           "This is the design mockup for the inventory-alert dashboard. Implement the /inventory/alerts page."
```

The developer did only one thing: express intent + provide a visual anchor. From here the self-healing loop begins, and the developer's attention no longer intervenes.

### Step 2: AI Understands the Mockup → Compares with the Current State → Generates an Improvement Plan

```
AI:   → Read the mockup screenshot, parse the layout structure:
        - Top: SKU table (out-of-stock rows highlighted red)
        - Bottom: Export CSV button
      → Playwright captures a screenshot of the /inventory/alerts page
      → Compare mockup vs. current state region by region, generate a diff list
```

**Diff Report**

```
1. Filter: mockup places it above the table; current state in the left sidebar
2. Out-of-stock highlight: mockup uses #FF4444 light red; current uses #BB0000
3. Export button: mockup has it; current state is missing it
4. Table column order: mockup [SKU|Stock|Safety Line|Status]
                       current [SKU|Stock|Warehouse|Status]
```

→ Output an improvement plan (4 changes, ordered by dependency)

### Step 3: AI Generates the E2E Playwright Verification Script

The AI generates a Playwright script based on the mockup — this is meta-automation (Principle 2): using AI to write the verification script that automates the verification of AI-generated code.

```
AI:   → Generate the Playwright E2E script inventory_alerts_e2e.spec.ts:
        - Navigate to /inventory/alerts
        - Inject mock data (3 warehouses, 20 SKUs, 5 out of stock)
        - Assert the filter position (above the table)
        - Assert out-of-stock row background color = #FF4444
        - Assert the Export CSV button exists and is clickable
        - Assert the table column order
        - Save the screenshot as the verification baseline
```

### Hands-on Example 2: Visual Self-Healing for Non-Browser UI (PPT Generation)

Flow Coding is not limited to web development. When handling document-generation tasks (such as PPTX/PDF) with invisible UI, the flow can still be closed via "screenshot self-inspection."

**Scenario**: Automatically generate a hand-drawn-style PPT of the 24 solar terms from video content, ensuring the illustrations are full and well-proportioned.

**Process**:
1. **Intent expression**: The developer asks to convert a video into a PPT, requiring the original UI's hand-drawn component style to be preserved.
2. **Production side**: The AI uses `python-pptx` to draw geometric shapes (cow, person, cloud, tree).
3. **Verification-side automation (core step)**: The AI writes `pptx_preview_spire.py`, which calls a component library to automatically render every page of the generated PPT into a PNG image.
4. **Visual analysis**: The AI reads these images via `read_file` and uses its visual ability to spot layout problems like "text overflow" and "components too small."
5. **Self-healing loop**:
    - **Discover**: The "Jingzhe" title on Slide 1 is too close to the edge, and the cow is too small.
    - **Fix**: Automatically modify the `scale` parameter and `top_pad` offset in the code.
    - **Re-verify**: Regenerate the PPT → re-screenshot → confirm the proportions are perfect.

**Value**: The developer doesn't need to repeatedly "generate → find the folder → open the PPT → flip through pages by eye → close → change code." Attention always stays at the intent layer in the IDE.

### Step 4: The Self-Healing Loop — AI Modifies Code → Runs the Script → Reads Feedback → Corrects → Loops

```
——Self-healing loop starts——

Iteration 1:
AI → Modify component code (all 4 improvements implemented in parallel)
System → Execute the Playwright E2E script
Result → 2 pass / 2 fail
  ✗ Filter positioned too far left (CSS flex not taking effect)
  ✗ Out-of-stock color #FF4444 displays as #FF3333
    (color-space conversion error in the test)
AI → Read console log + screenshot + assertion-failure info

Iteration 2:
AI → Fix CSS flex layout + adjust color to an sRGB-safe value
System → Re-execute the Playwright E2E script
Result → 4 pass / 0 fail
Screenshot → pixel diff against the mockup < 2% (acceptable threshold)

✅ Self-healing loop complete, report to the developer

——Self-healing loop ends——

Developer: (looks at the final screenshot + diff report) "OK, ship it."
```

### Full-Flow Attention Cost Analysis

```
Traditional development (manual verification):
Developer-involved steps: write code → open browser → navigate → eyeball compare → switch back to IDE → change code → repeat
Number of attention switches: ~10 (2 switches per change point)
Total attention cost: ~10 × 45s = 7.5 minutes

Flow Coding (self-healing loop):
Developer-involved steps: upload mockup + say "implement it" → final report says "OK"
Number of attention switches: 0
Total attention cost: ~30 seconds (only the starting intent layer + the final judgment)

Attention saved: 93%
```

### Principle Traceback

| Principle | How It Appears in This Example |
|-----------|-------------------------------|
| Principle 1: Verification-side automation | The Playwright E2E script replaces manual navigation + eyeball comparison |
| Principle 2: Meta-automation + self-healing | The AI generates the verification script that flows back to the AI, with no developer intervention in intermediate rounds |
| Principle 3: Attention conservation | The developer participates only at the start and end; the 2 intermediate self-healing rounds cost zero attention |
| Principle 4: Layered trust | Inventory alerts belong to the high-trust layer (CRUD + UI), allowing full automation; if permission logic were involved, it would trigger a prompt |

---

## 7. Applicability Boundaries

(To be added)

---

## 8. FAQ

(To be added)

---

## 9. Related Concepts

(To be added)

---

## 10. Triple Feedback: Frontend + Backend + Playwright

The reason Flow Coding's self-healing loop can converge reliably is fundamentally that the AI receives not a single signal, but **three mutually independent, cross-verifiable real-time feedback streams**.

### Why a Single Feedback Stream Is Not Enough

Looking only at Playwright screenshots/assertions tells you "the result is wrong" but not "why it's wrong":

```
With only Playwright:
Assertion failed: page shows "0 skills"
  → Did the frontend not render? Did the backend return empty? Or was the request never sent?
  → No way to tell — can only guess → falling into "repeated trial and error"
```

This is the enemy of attention conservation (Principle 3) and 3 × 3 convergence (Principle 2): **insufficient information leads to wrong directional hypotheses, wasting the iteration budget.**

### The Division of Labor Among the Three Feedback Streams

| Feedback Source | Signal Carrier | Question It Answers | Observation Layer |
|-----------------|----------------|---------------------|-------------------|
| ① Behavior feedback | Playwright screenshot + assertions | What did the user **see/experience**? | Presentation layer (end-to-end result) |
| ② Frontend feedback | `logs/ui.log` (frontend stdout + request status codes + SSR errors) | What did the frontend **do**, and was the request **sent**? | Frontend runtime layer |
| ③ Backend feedback | `logs/server.log` + `logs/access.log` (app logs + server + every HTTP request) | Did the backend **receive** the request, what did it **return**, did it **error**? | Backend runtime layer |

Together the three cover the **complete causal chain** of a single user action:

```
User action → [② frontend sends request] → [③ backend processes and responds] → [② frontend receives and renders] → [① user sees result]
               ui.log                        access.log/server.log                 ui.log                             Playwright screenshot
```

### Triangulation: Cross-Verification Pinpoints the Root Cause

When all three signals are readable in real time simultaneously (`tail -f`), the AI no longer "guesses the direction" but **cross-compares** to directly pinpoint the root-cause layer:

```
Symptom (①): Playwright assertion failed — page shows "0 skills"

Cross-comparison:
  ② ui.log:      POST /api/skills 200 in 16ms      ← frontend request sent and succeeded
  ③ access.log:  GET /skills HTTP/1.1 200 OK        ← backend received and returned 200
  ③ server.log:  Found 58 skills ... ls: Directory not found  ← backend logic anomaly!

Conclusion: the request chain is fully connected (② ③ status codes both 200), but server.log
            reveals the backend is doing `ls` on a non-existent path → root cause is in the backend,
            and it's a path-resolution problem. Pinpointed in one shot, no trial and error needed.
```

Reference table (pinpoint the root-cause layer at a glance):

| ① Behavior | ② Frontend (ui.log) | ③ Backend (access/server) | Root-Cause Layer |
|------------|---------------------|----------------------------|------------------|
| Wrong result | No request logged | No request logged | Frontend: event/state never triggered the request |
| Wrong result | Request 4xx/5xx | Has error stack | Backend: logic/data anomaly |
| Wrong result | Request 200 | 200 + normal logs | Frontend: got correct data but rendering/state is wrong |
| Wrong result | Request 200 | server.log has anomaly but still returns 200 | Backend: swallowed the exception, returned wrong content |
| Wrong result | Request timeout | No access record | API contract: URL/port/proxy misconfigured |

### Relationship to the Self-Healing Loop

Triple feedback is the **input fuel** for the self-healing loop (Principle 2) — the more complete and real-time the feedback, the more accurate the directional hypothesis, and the less of the 3 × 3 budget is consumed:

```
Playwright fails
   ↓
AI simultaneously reads ① screenshot + ② ui.log + ③ server.log/access.log
   ↓
Triangulation → pinpoint the root-cause layer (frontend/backend/data/contract)
   ↓
Fix at the correct location (minimal upstream fix)
   ↓
Re-run Playwright → re-compare all three signals → converge or switch direction (subject to 3 × 3 constraints)
```

### Engineering Prerequisite: All Three Logs Must Be Real-Time and Tailable

The hard prerequisite for triple feedback is that **all stdout is persisted to disk in real time and is `tail -f`-able**, regardless of how the service is started (script / IDE debug / manual):

- **Backend**: at the application entry, tee `stdout`/`stderr` to `logs/server.log`; write the server access log separately to `logs/access.log`.
- **Frontend**: the `dev` script tees the frontend dev-server output to `logs/ui.log`.
- **Unified monitoring**: `tail -f logs/server.log logs/access.log logs/ui.log`.

> If any feedback stream is missing (e.g., the backend only outputs to the IDE console and isn't persisted), triangulation degrades into single-point guessing, and the convergence of the self-healing loop drops accordingly. **Ensuring all three feedback streams are readable in real time is Flow Coding's infrastructure.**

---

## Algorithm / Step-by-Step Process

When assigned a complex UI, component, API, or system refactoring task, follow this 5-phase algorithm:

### PHASE 1: ESTABLISH THE VERIFICATION BASELINE

Before making any edits, find or create the automated test representing the current feature state.

- **Frontend**: If a Playwright E2E spec exists, run it to confirm a 100% passing baseline.
- **Backend**: If a test endpoint or integration test exists, `curl` it to capture the current response shape.
- **Rule**: This baseline is your "safety guardrail" — any change must converge back to green.

### PHASE 2: INTENT EXPRESSION & CODE GENERATION (VIBE)

Express your architectural design and change requirements.

- **Action**: Perform edits on components, endpoints, or data models.
- **Standard**: Always make changes clean, compile-safe, and immediately runnable.
- **Pattern**: Prefer minimal upstream fixes over downstream workarounds. Identify root cause before implementing.

### PHASE 3: TEST SPEC ADAPTATION (META-AUTOMATION)

When major structural shifts occur, the selectors/assertions in existing tests will break. You must adapt the tests as part of the refactoring process.

- **Frontend**: Adjust locators, click targets, and state assertions in Playwright specs.
- **Backend**: Update expected response shapes, add new assertion fields, or create verification scripts.
- **Rule**: If features are intentionally removed, simplify or update corresponding assertions rather than letting stale tests break the build.

### PHASE 4: SELF-HEALING LOOP (AUTOMATED RUN & FIX)

Run the tests and feed failures back into the development engine. The goal is **end-to-end product integrity**, not just frontend correctness.

1. Run the test suite.
2. Capture any failures (locators missing, timing races, async state mismatches, wrong response shapes).
3. **Locate the source first**: Use console error / network error / assertion failure / API response shape to decide whether the root cause lives in the **frontend, backend, data layer, or API contract**. Do not assume it is always a frontend issue.
4. **Fix at the correct location**: Edit frontend **and/or** backend code as needed. Prefer minimal upstream fixes over downstream workarounds; fix the root cause, never mask the symptom.
5. **Bounded iteration — the 3 × 3 rule** (no infinite loops):
   - **Max 3 attempts per direction**: Iterate up to 3 fixes along the same root-cause hypothesis.
   - **Max 3 direction switches**: If 3 attempts fail, the hypothesis is likely wrong — switch to a new direction (new root-cause hypothesis), up to 3 switches.
   - **Stop at the ceiling**: If the 3 × 3 limit (max 9 attempts) is reached without convergence, halt the loop, summarize each direction's attempts and failure evidence, and hand back to the developer.
6. **Repeat**: Re-run and fix within the 3 × 3 budget until 100% of the tests pass.

### PHASE 5: FINAL CONVERGENCE & CONFIRMATION

Once the test suite passes completely (all green), take final screenshots or recordings of the UI, or capture the final API response, and present the verified, completed state to the user.
