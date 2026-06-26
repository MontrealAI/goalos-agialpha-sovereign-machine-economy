# Create the Repository from GitHub Web UI

This guide assumes you are using only the GitHub website.

## Recommended repository settings

**Repository name**

```text
goalos-agialpha-sovereign-machine-economy
```

**Description**

```text
GoalOS AGIALPHA Ascension — Sovereign Machine Economy: proof-settled autonomous AI work, Evidence Dockets, validator-gated jobs, and reusable capability packages.
```

**Visibility**

Public is recommended for the easiest GitHub Pages setup.

**Topics**

```text
goalos, agialpha, autonomous-ai, agentic-ai, evidence-docket, proof-bundles, validator-mesh, machine-economy, github-pages, governed-ai
```

## Required GitHub settings

### 1. Allow Actions to write

Go to:

```text
Settings → Actions → General → Workflow permissions
```

Select:

```text
Read and write permissions
```

This allows the autopilot to commit generated files.

### 2. Enable GitHub Pages with Actions

Go to:

```text
Settings → Pages → Build and deployment → Source
```

Select:

```text
GitHub Actions
```

This allows the workflow to deploy the generated `public/` website.

## First action run

Create this file:

```text
.github/workflows/goalos-ascension-autopilot.yml
```

Paste the provided workflow, commit it, then run it manually from **Actions**.

Recommended first mode:

```text
direct_commit_and_publish
```

## After launch

1. Open **Settings → Pages**.
2. Copy the live website URL.
3. Paste it into the repository **About → Website** field.
4. Pin the repository if desired.
5. Open `reports/autopilot-summary.md` to see what was generated.
