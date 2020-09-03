def _canvas_to_PL_roles(canvas_role : str) -> str:
    assert canvas_role is not None, "canvas_role is None"
    assert canvas_role != "", "canvas_role is empty string"
    canvas_role = canvas_role.strip()
    if canvas_role in ("Student", "Waitlist Student"):
        return "Student"
    elif canvas_role in ("Teacher", "Lead TA"):
        return "Instructor"
    else:
        return "TA"
