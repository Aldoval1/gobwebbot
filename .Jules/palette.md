## 2024-05-18 - Missing labels in register form
**Learning:** The user registration form (`app/templates/register.html`) lacks explicit `<label>` elements, relying instead on WTForms placeholders. This is an accessibility issue to be resolved.
**Action:** When adding labels, use the standard `<label for="...">` format and link it correctly to the WTForms generated id (e.g., `first_name`).

## 2024-05-18 - WTForms and accessibility labels without custom CSS
**Learning:** When adding accessibility labels to WTForms inputs where custom CSS is strictly forbidden (meaning `.sr-only` classes cannot be added), adding visually hidden `<label>` elements is not viable.
**Action:** Pass `aria-label` as kwargs to the WTForms field call in the template directly, e.g., `{{ form.first_name(placeholder="Nombre", **{'aria-label': 'Nombre'}) }}`, which maintains design boundaries while satisfying accessibility needs.
