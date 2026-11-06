# Kiln

In an atelier (workshop), the **kiln** is the vessel that must hold the whole firing. Too much heat or charge and it cracks. Context is the same: the working window is the kiln; budgets are its safe temperature.

- Soft line → cool at the next logical boundary (phase end), do not interrupt mid-implementation.
- Peak line → must cool before the next phase starts.
- Handoff line → leave the kiln, write a state tablet, start a new firing (new session) with tablet + task only.

Roles share one kiln policy file but have different chambers:

- Designer chamber: larger budget, holds plans and decisions.
- Implementer chamber: smaller budget, one attempt, preferably a fresh fire each time.
