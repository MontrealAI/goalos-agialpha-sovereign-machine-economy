# 14 — Repository Operating Manual for Non-Technical Operators

This guide explains how to operate the repository using the GitHub Web UI.

## One-time settings

Open the repository settings:

```text
Settings → Actions → General → Workflow permissions
```

Select:

```text
Read and write permissions
```

Then open:

```text
Settings → Pages → Build and deployment → Source
```

Choose:

```text
GitHub Actions
```

## Correct workflow order

For a brand-new repository:

```text
1. goalos-autopilot-institutional-evidence.yml
2. goalos-historical-master-update-autopilot.yml
3. goalos-ascension-visual-parity-v4-autopilot.yml
4. goalos-document-series-autopilot.yml
```

For the existing repository:

```text
1. goalos-historical-master-update-autopilot.yml
2. goalos-ascension-visual-parity-v4-autopilot.yml
3. goalos-document-series-autopilot.yml
```

## Why V4 runs last

```text
Historical Master = everything we mean.
Visual Parity V4 = how it must feel.
```

The V4 action is the final visual quality pass. Run it after content actions.

## How to add a workflow

1. Open the repository.
2. Click **Code**.
3. Click **Add file → Create new file**.
4. Paste the path:

```text
.github/workflows/<workflow-name>.yml
```

5. Paste the workflow contents.
6. Commit directly to `main`.
7. Go to **Actions**.
8. Select the workflow.
9. Click **Run workflow**.

## First-run inputs

Use:

```text
commit_changes: true
deploy_pages: true
create_release: false
create_issues: true
```

After visual approval, rerun with:

```text
create_release: true
```

## Pages to inspect

```text
/
historical-command-center.html
console.html
frontier-release-room.html
meta-agentic-alpha-agi.html
agi-alpha-node-v0.html
agi-jobs-v0-v2.html
research-spine.html
holy-grail-candidate.html
proof-run-001.html
multi-agent-institution.html
coordination-console.html
document-series.html
```

## What green means

A green workflow run means the workflow completed. It does not by itself prove empirical claims. Always inspect the generated pages and reports.
