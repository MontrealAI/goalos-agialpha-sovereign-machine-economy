# Create the Repository Using Only GitHub Web UI

This guide assumes you do not want to use a terminal.

## Step 1 — Create the repository

On GitHub, click **New repository**.

Use:

```text
Repository name: goalos-agialpha-sovereign-machine-economy
Visibility: Public
Add a README file: Yes
```

Click **Create repository**.

## Step 2 — Let the Action write files

Open:

```text
Settings → Actions → General → Workflow permissions
```

Select:

```text
Read and write permissions
```

Click **Save**.

## Step 3 — Let GitHub Pages use Actions

Open:

```text
Settings → Pages
```

Under **Build and deployment**, set **Source** to:

```text
GitHub Actions
```

## Step 4 — Create the workflow file

Open the **Code** tab.

Click:

```text
Add file → Create new file
```

Name the file:

```text
.github/workflows/goalos-ascension-autopilot.yml
```

Paste the autonomous workflow.

Click **Commit changes**.

## Step 5 — Run the Autopilot

Open **Actions**.

Click:

```text
GoalOS AGIALPHA Ascension — Sovereign Machine Economy Autopilot
```

Click **Run workflow**.

Use:

```text
mode: direct_commit_and_publish
overwrite_existing_files: true
```

Click the green **Run workflow** button.

## Step 6 — Find your website

When the workflow is done, open:

```text
Settings → Pages
```

Copy the URL shown there.

## Step 7 — Add the website to the About box

On the repository home page, click the gear icon near **About**.

Paste the GitHub Pages URL.

Add the repository description and topics from [`LAUNCHPAD.md`](LAUNCHPAD.md).

## Step 8 — Verify quality

Open:

```text
reports/site-qa.json
reports/claim-scan.json
reports/repo-validation.json
reports/institutional-scorecard.json
```

If all are passing, the launch surface is ready for public review.
