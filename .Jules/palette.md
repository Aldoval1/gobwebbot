## 2024-05-24 - WTForms ARIA attributes requirement
**Learning:** WTForms in this application cannot handle hyphenated ARIA attributes correctly without specifically unpacking a dictionary within the Jinja template (e.g. `**{'aria-label': 'Value'}`).
**Action:** When adding ARIA attributes to WTForm inputs in this application, always use the unpacking method.