---
name: seams-test
description: Use this skill BEFORE refactoring, extracting, or touching ANY existing code that lacks test coverage, regardless of language, framework, or architecture (Laravel, .NET, Java, Python, Node, COBOL, whatever). Provides the underlying, technology-agnostic theory, decision tree for finding seams, and tactics like Approval Testing, Sprout/Wrap, and manual Mutation Testing. Trigger this whenever the user mentions "legacy code", "brownfield", "no tests for this", "before I refactor", "safety net", "seams", "characterization tests", "golden master", or asks how to safely change code with no coverage, in ANY stack. This is the base/conceptual skill — if a more specific skill exists for the user's exact stack, prefer that one for syntax, but the reasoning and decision tree are universal.
---

# Seams and Characterization Testing — universal techniques

These techniques come from Michael Feathers' work (*Working Effectively with Legacy Code*) and are independent of language, framework, and architecture. The only thing that changes between stacks is the syntax to implement them — the decision logic is always the same.

## The problem they solve

You cannot refactor code without tests with confidence. But you also cannot write tests easily if the code is tangled — to do that you need to break dependencies first, without changing behavior. That break is a **seam**.

> **Definition of seam (Feathers):** a place in the code where you can alter behavior without editing that code in that place.

A seam always has an **enabling point** (the place where you decide which behavior to use — real or double). Identifying the enabling point is 80% of the work.

## Before you start: Scratch Refactoring (Exploration Refactor)
Sometimes the codebase is so opaque that you cannot even see where to insert a seam. Before trying to test, use this reconnaissance tactic:
1. Create a temporary branch (`git checkout -b scratch`).
2. Tear the code apart: move variables, extract raw methods, delete entire logical blocks, and rename mercilessly. The only goal is to understand how data flows and find the injection points.
3. **Strict rule:** Once the seam is found, you MUST `git reset --hard` (or discard the branch) and go back to the original code to apply the seam for real, now with the test safety net in place.

## Golden rule, holds in any stack

**Never fix a bug detected during this process.** The characterization test documents the actual behavior, bugs included. Fixing bugs is a behavior change — and the goal of this phase is exactly the opposite: zero-change behavior, coverage first. Mark findings with `// BUG:` or equivalent and continue.

## Safe addition strategies (Sprout & Wrap)
If your goal is to *add* a new feature and untangling dependencies to do a full refactor is prohibitive time-wise, use these tactics to avoid touching the legacy logic:

- **Sprout Method/Class:** Instead of injecting new logic in the middle of a huge function, create the new validation or calculation in a separate function (with its own tests). In the legacy code, you only add the call to that "sprout".
- **Wrap Method/Class:** If the legacy function is untouchable, rename the original (e.g. from `process` to `process_core`). Create a new `process` function that runs the new logic and then delegates to `process_core`. The external caller never knows.

## Types of seam (from cheapest to most invasive)

### 1. Object seam
Exists in any object-oriented language or one with function composition. The enabling point is where the concrete implementation is decided: constructor, function parameter, public property, factory.

- **If it already exists** (the dependency comes in via constructor/parameter): free, you don't touch production, you just pass a double in the test.
- **If it does not exist** (the dependency is created inline with `new`, `require`, direct `import` of a singleton, etc.): create it by adding a new entry point that preserves the default behavior for existing callers. The universal pattern is: *constructor/function with a default value that delegates to the original constructor/function*.

### 2. Wrapper seam (for statics, globals, and singletons)
When the dependency is a static, a singleton, or something injectable from the runtime (clock, file system, HTTP context), wrap it in your own minimal interface/abstraction, and THAT wrapper is what gets injected as an object seam. Rule: only wrap external effects (IO, time, network, mutable global state).

### 3. Extract seam (extract method/function)
When a block of code mixes too many responsibilities and there is no natural boundary. Watch out: this is not a refactor yet, it is just giving a name and a boundary to something anonymous so that in the next step (object seam) you have something concrete to substitute.

### 4. Preprocessor / link / module seam
The most invasive: compiler directives, module substitution at load time, monkey-patching. It leaves traces (e.g. `#if TEST`) and is always documented as technical debt. Use only as an absolute last resort.

## How to choose: universal decision tree

1. Does the dependency already come in via parameter/constructor? → object seam, free.
2. Is it created inline but is a normal class/function? → object seam, adding an entry point with a default that preserves behavior.
3. Is it a static/singleton/runtime resource? → wrapper seam, then inject the wrapper.
4. Does the block mix too much and there is no clear boundary? → extract seam first, then apply 1-3.
5. Is none of the above viable? → preprocessor/link seam, documented as debt.

## Pinch points: when NOT to isolate dependency by dependency

If a method has 20 dependencies, do not isolate all 20. Look for the **pinch point**: the highest point in the call chain where everything converges before fanning out (e.g. the base data access method). Placing the seam there covers more surface with less effort.

## Characterization tests: universal rules

A characterization test (golden master test) does not validate what the code *should* do — it validates what it *does* today.

**Preferred tactic:** Use **Approval Testing (Snapshotting)**. Instead of writing dozens of manual `asserts` guessing results, the test should run the code, capture the full final state (a DB dump, a huge output JSON, or rendered HTML) and save it as a baseline text file. Future runs only validate a *diff* against that snapshot.

Universal checklist:
- [ ] The test name indicates it describes current behavior (`_CurrentBehavior`, `_golden`).
- [ ] All non-determinism is frozen (time, random, generated identifiers, collection ordering) — but only the part that is *freezable*. See "What to freeze, and what not to" below.
- [ ] **Transactional isolation:** If the DB could not be mocked, the entire test MUST run inside a transaction that forces a `ROLLBACK` in `teardown`, guaranteeing a constant clean state.
- [ ] Every decision path and every side effect (persistence, fired events) is covered.
- [ ] Bugs found are commented with `// BUG:`, not fixed.
- [ ] Every uncovered decision path was reviewed and either exercised and frozen, or proven unreachable and documented — not merely left in the report.

## What to freeze, and what not to

A golden master freezes **content**, not the incidental shape of the data. Two failure modes come from freezing too much, and both produce a test that breaks for reasons that have nothing to do with the code.

**Do not freeze an order that nothing guarantees.** If a collection comes back in an order the code never promises — no explicit sort key in the query, or a view whose plan is free to change — that order is an artifact of storage layout and query planning, not behavior. It flips after any write to the underlying tables, a reindex, or a different execution plan, and it can flip *because another test wrote a row and rolled back*. Freeze such a collection sorted by a key that is stable and unique, and leave collections whose order *is* guaranteed exactly as they arrive. When adding a test, run the **whole suite**, not only your own file: the order in which tests execute changes the state the others observe, and a fragile snapshot usually passes alone and breaks in the suite.

**Do not freeze identifiers the environment assigns.** When the code resolves something by a human-meaningful name — an entity, a role, a group, a type — freeze the **name**, not the surrogate key the store handed out. A surrogate key belongs to the row, not to the behavior: it changes when the row is recreated and it differs between environments, so freezing it binds the test to data instead of to code. This applies to keys the code persists as references too — resolve them back to the natural key before comparing. Identifiers *created inside the test* (in the same transaction) are different: they are an effect of the code, so they can be frozen. When the test has to borrow rows that already exist, verify their presence and state before freezing them, and record in the test what is genuinely borrowed from the live environment.

The rule of thumb: **the snapshot must contain only what the code decided.** Everything the environment decides — the current time, a random draw, the physical layout of a table, the numeric id of a pre-existing row — is either normalized away or replaced by the stable identity the code actually used.

## "I can refactor now" criterion (Trust Verification)

Do not use the line coverage metric as your criterion of readiness. Apply **manual Mutation Testing** to audit your own test:
1. Once your characterization test passes green, go into the real legacy code.
2. Change a `+` to a `-`, a `>` to a `<`, or comment out a critical assignment.
3. Run the test. If it still passes green, **the test is not verifying that behavior** — see "Executed is not verified" below for what that can mean.
4. Undo the mutation immediately.

You are ready to refactor only when any deliberate mutation in the impact area breaks the test.

### Executed is not verified

A line that runs is not a line that is verified. Line coverage says which lines were *executed*; mutation says which *behaviors* are frozen. When a mutation leaves the test green, the test is not looking at what that line produces.

- **Capture the effect, not the arrival.** A test that only asserts "the flow reached the end" cannot see a change to the value the line produced. Assert the observable effect of that line — the state it writes, the query it builds, the payload it returns — not the fact of having passed through it.
- **Ask *which* path detected it.** When one line is shared by several paths, a mutation may break only some of them. "Some test failed" is not enough: if one path does not fail, that path is not asserting what you thought it was. Fix it so every path that should observe the line observes it.
- **A green mutation has three possible causes,** not two:
  1. the seam is in the wrong place (the test cannot influence that code),
  2. the test is a false positive (it asserts something that never varied), or
  3. **the code is unreachable** — no input reaches that line, so no test can observe it. This is a property of the code, not a defect of the test.
  Before settling on (1) or (2), try to *prove* (3): enumerate the input space that can reach the line, or reason about the predicates that guard it. If it is genuinely unreachable, document it as dead code and leave it untested — a test for unreachable code can only be made to pass by inventing an input no caller can produce.
- **Report both directions.** The report must list the mutations that broke the test *and* the ones that did not, with the reason for each undetected one. A report listing only detected mutations cannot tell "the net is solid" apart from "the net was never tested in that direction".

### After the mutations: use coverage as a map, not as a metric

Mutation testing tells you whether the behaviors you *thought to check* are really frozen. It cannot tell you which behaviors you never thought of. That is what the coverage report is for — and it is why it comes *after* the mutations, not instead of them: coverage is a **map of where you never went**, mutation is the proof that where you did go, the net holds.

When the environment allows it (coverage instrumentation installed, run affordable), re-run the tests with coverage and read the report as a list of **unvisited decision paths**, not as a percentage to maximize.

- **Scope it.** Measure the code under characterization, and separately the collaborators it delegates to: the first shows what this test contributes, the second what it merely inherits from other tests.
- **Turn every uncovered line into a question.** Is this a path a caller can actually reach, and does reaching it produce a *meaningfully different* outcome? If yes, that is a scenario the golden master is missing: write it, freeze it, and then mutate that new path to confirm the new scenario really detects it.
- **Separate reachable from unreachable before writing anything.** The report cannot tell them apart. Prove reachability — enumerate the input space that reaches the line, or reason about the predicates that guard it. Unreachable code is documented as dead, not tested with an invented input.
- **Do not chase the percentage.** A covered line is not a frozen behavior (see "Executed is not verified"), and full line coverage does not mean the characterization is complete: a file can execute every line and still miss an input that yields a different outcome. Enumerate decision paths, not lines.
- **If instrumentation is unavailable or too slow, do it by hand.** The goal — finding the paths nobody looked at — does not depend on the tool: read the code and list the decision paths (branches, short-circuits, distinct input values that take the same route) and check each one against your scenarios.

A characterization is finished when the uncovered paths have all been either exercised and frozen, or proven unreachable and documented — not when the coverage number is high.

## What NEVER to do, in this phase

- Do not fix detected bugs — document them.
- Do not "clean up" code (except for the disposable Scratch Refactoring).
- Do not mock dependencies returning "ideal" data — the double must reproduce the garbage that the real dependency spits out today.
- Do not try to cover 100% of a monolith — cover only the impact surface of the change you are going to make.

## Output report (universal)

When finishing the safety net setup, always deliver:
1. Which seam type was used for each touched point and the justification per the decision tree.
2. Results of the manual Mutation Testing: **which mutations broke the test and which did not**, with the reason for each undetected one (unreachable code, or a path that does not assert that effect).
3. Documented bugs discovered.
4. Snapshot files (Approval Testing) generated.
5. The uncovered paths the coverage pass surfaced, and for each one what was done: exercised and frozen, or proven unreachable and documented as dead code.

## Note about stack-specific skills

This skill defines the underlying reasoning. For exact syntax, snapshotting library names, or framework-specific injection conventions, delegate to the skill specific to the technology.