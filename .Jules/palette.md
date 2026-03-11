## 2024-05-18 - Modal Close Button Accessibility
**Learning:** Custom span-based modal close buttons without `role="button"` and `tabindex="0"` are invisible to screen readers and unreachable via keyboard navigation, breaking accessibility.
**Action:** When adding or maintaining custom modal close buttons (e.g. `<span class="close">`), always add `role="button"`, `tabindex="0"`, an `aria-label`, explicit `:focus-visible` styling, and a JavaScript keydown listener for 'Enter' and 'Space' events to simulate clicks.
