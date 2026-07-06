---
status: public-alpha
capability_layer: goalos-incremental-proof-grail-v1
public_private: public-safe
last_reviewed: 2026-07-06T03:00:38+00:00
claim_level: architectural
---

# Website Incremental Autopilot Guide

This autopilot is additive. It creates new pages, docs, evidence manifests, reports, route entries, and optional navigation links. It refuses destructive deletion and does not overwrite non-managed files unless allow_overwrite is explicitly set to true.

Recommended first run: direct_commit, deploy_pages true, update_navigation true, allow_overwrite false, fail_on_audit_error true.
