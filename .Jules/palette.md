
## 2025-02-17 - Button Loading State
**Learning:** Testing intermediate loading states (button disabled, spinner visible) with Playwright during a standard form submission requires `no_wait_after=True` on the click action, and preventing the actual navigation (e.g., via `javascript:void(0)` action) allows for reliable inspection without race conditions.
**Action:** Use this pattern for verifying other form submission loading states to avoid flaky tests.
