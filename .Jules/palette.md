
## 2024-03-10 - Accessible Modal Close Controls
**Learning:** This application uses a consistent pattern of `span.close` with `&times;` for modal close buttons across various templates (`my_fines.html`, `appointments.html`, `official_dashboard.html`). These default elements are not inherently keyboard accessible or semantic.
**Action:** When adding new modals or interacting with existing ones in this app, ensure the `span.close` includes `role="button"`, `tabindex="0"`, `aria-label="Cerrar modal"`, clear `:focus-visible` CSS outlines, and explicit JavaScript `keydown` listeners (handling 'Enter' and 'Space') to guarantee full keyboard and screen reader accessibility.
