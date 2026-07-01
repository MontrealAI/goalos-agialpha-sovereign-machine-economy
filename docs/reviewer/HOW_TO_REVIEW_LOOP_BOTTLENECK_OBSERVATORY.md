# How to Review the Loop Bottleneck Observatory

Use this page to evaluate whether the loop makes its own next bottleneck visible.

## Reviewer route

1. Open `public/loop-bottleneck-observatory.html`.
2. Run the default loop.
3. Stress the weak loop.
4. Toggle each hard gate off and confirm the decision state changes.
5. Confirm the custom objective is preserved in exported artifacts.
6. Download the bottleneck report, loop contract, trace ledger, replay pack, and reviewer brief.
7. Confirm the public-alpha boundary is visible.
8. Confirm the page does not use network calls, wallet APIs, local storage, or analytics.

## Acceptance criteria

- Contract weakness becomes visible.
- Missing disk state blocks restartability.
- Missing independent evaluator blocks trust.
- High harness overhead becomes its own bottleneck.
- Disabled public/private boundary blocks promotion.

## Possible reviewer verdicts

Accept, reject, revise, or dissent. Preserve the no-data/no-funds boundary in all feedback.
