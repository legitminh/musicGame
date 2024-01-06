from UI import UiElement, UiElementGroup


class ListGroup(UiElementGroup):
    def __init__(
        self,
        dist_between_elements: float,
        *elements: UiElement,
    ) -> None: 
        self.dist_between_elements = dist_between_elements
        super().__init__(*elements)
    
