# PROJECT RULES -- IDS PROJECT

## 1. Preserve existing architecture

Use the existing structure:

``` text
src/parser/transport/
src/parser/network/
src/parser/application/
src/pipeline/
tests/
TEST/
```

Do not create duplicate modules such as:

``` text
src/parser/tcp.py
```

when the existing module is:

``` text
src/parser/transport/tcp.py
```

## 2. Preserve existing tests

When adding a testcase:

-   append a new test
-   do not overwrite previous tests
-   do not remove previous testcase data
-   run the full test suite

## 3. Test-first workflow

For each new testcase:

``` text
understand requirement
 ↓
prepare input
 ↓
implement/change code
 ↓
pytest
 ↓
run main.py if applicable
 ↓
inspect JSONL
 ↓
README
 ↓
git add .
 ↓
commit
 ↓
push
```

## 4. Git policy

Each testcase/task must have its own commit.

Use concise messages:

``` text
test: complete TCXX <description>
feat: ...
fix: ...
docs: ...
```

Do not:

-   squash
-   rewrite history
-   force push
-   reset away completed testcase commits

## 5. JSONL

When a task produces events, verify:

``` text
--output <path>.jsonl
```

and inspect the generated file.

One event per line.

## 6. Error handling

Unsupported/malformed input should not crash the pipeline.

Prefer safe fallback behavior over an unnecessary new parser.

## 7. Minimal changes

If a task only needs a parser change, do not refactor unrelated files.

If a design change is necessary, explain why before changing it.

## 8. AI handoff

Before starting work, read:

``` text
AI/MASTER_CONTEXT.md
AI/CURRENT_STATUS.md
AI/PROJECT_RULES.md
AI/handoffs/BAI1_COMPLETE.md
```

Then inspect the actual code rather than relying only on this document.
