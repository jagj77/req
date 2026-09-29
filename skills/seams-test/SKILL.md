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
- [ ] All non-determinism is frozen (time, random, IDs, UUIDs, collection ordering).
- [ ] **Transactional isolation:** If the DB could not be mocked, the entire test MUST run inside a transaction that forces a `ROLLBACK` in `teardown`, guaranteeing a constant clean state.
- [ ] Every decision path and every side effect (persistence, fired events) is covered.
- [ ] Bugs found are commented with `// BUG:`, not fixed.

## "I can refactor now" criterion (Trust Verification)

Do not look at the line coverage metric. Apply **manual Mutation Testing** to audit your own test:
1. Once your characterization test passes green, go into the real legacy code.
2. Change a `+` to a `-`, a `>` to a `<`, or comment out a critical assignment.
3. Run the test. If it still passes green, **your seam is in the wrong place or you have a false positive**.
4. Undo the mutation immediately.

You are ready to refactor only when any deliberate mutation in the impact area breaks the test.

## What NEVER to do, in this phase

- Do not fix detected bugs — document them.
- Do not "clean up" code (except for the disposable Scratch Refactoring).
- Do not mock dependencies returning "ideal" data — the double must reproduce the garbage that the real dependency spits out today.
- Do not try to cover 100% of a monolith — cover only the impact surface of the change you are going to make.

## Output report (universal)

When finishing the safety net setup, always deliver:
1. Which seam type was used for each touched point and the justification per the decision tree.
2. Results of the manual Mutation Testing (which line you mutated to verify the test).
3. Documented bugs discovered.
4. Snapshot files (Approval Testing) generated.

## Note about stack-specific skills

This skill defines the underlying reasoning. For exact syntax, snapshotting library names, or framework-specific injection conventions, delegate to the skill specific to the technology.