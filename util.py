from enum import Enum

class PLGroups(Enum):
    INSTRUCTOR = "Instructor"
    TA = "TA"
    STUDENT = "Student"


def _canvas_to_PL_roles(canvas_role : str) -> str:
    assert canvas_role is not None, "canvas_role is None"
    assert canvas_role != "", "canvas_role is empty string"
    canvas_role = canvas_role.strip()
    # already PL roles
    if canvas_role in ("Instructor", "TA", "Student"):
        return canvas_role
    if canvas_role == "Waitlist Student":
        return "Student"
    elif canvas_role in ("Teacher", "Lead TA"):
        return "Instructor"
    else:
        return "TA"
