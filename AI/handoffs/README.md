# AI HANDOFFS

This directory stores persistent handoff documents for switching between
AI models.

## Current handoff

Read:

``` text
AI/handoffs/BAI1_COMPLETE.md
```

It contains:

-   Bài 1 completion state
-   architecture
-   testcase status
-   important PCAP facts
-   implementation decisions
-   Git workflow
-   instructions for continuing

## Rule

When switching models:

``` text
MASTER_CONTEXT
      ↓
CURRENT_STATUS
      ↓
PROJECT_RULES
      ↓
handoffs/BAI1_COMPLETE.md
      ↓
inspect actual code
      ↓
continue next task
```

Do not rely on conversational memory alone.
