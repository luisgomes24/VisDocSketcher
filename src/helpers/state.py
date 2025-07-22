from typing import TypedDict, Optional, List, Dict


class DiagramState(TypedDict):
    # Raw input (only seen by analyser)
    notebook: Optional[str]

    # Analysis results (only seen by sketcher)
    analysis: Optional[Dict]

    # Mermaid code (only seen by repair and visual generator)
    mermaid_code: Optional[str]

    # Visual elements (only seen by visual generator and critique)
    visual_elements: Optional[Dict]

    # Feedback (only seen by critique and sketcher)
    feedback: List[str]

    # System state (internal use only)
    current_stage: str
    iteration: int
    max_iterations: int = 3
