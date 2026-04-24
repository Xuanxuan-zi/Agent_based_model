import math
## Using experimental agent type with native "cell" property that saves its current position in cellular grid
from mesa.discrete_space import CellAgent

## Helper function to get distance between two cells
def get_distance(cell_1, cell_2):
    x1, y1 = cell_1.coordinate
    x2, y2 = cell_2.coordinate
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx**2 + dy**2)

class SugarAgent(CellAgent):
    ## Initiate agent, inherit model property from parent class
    def __init__(self, model, cell, sugar=0, metabolism=0, vision = 0):
        super().__init__(model)
        ## Set variable traits based on model parameters
        self.cell = cell
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision

        # ============================================================
        # >>> MY MODIFICATION #1: Added boredom mechanism attributes <<<
        # ============================================================
        # Motivation: In the original model, agents are purely rational
        # greedy optimizers. I wanted to explore what happens when agents
        # have a behavioral quirk - getting "bored" of staying in one
        # place and forced to explore randomly.
        #
        # Each agent tracks how long it has been stuck in the same cell,
        # and has a personal patience threshold (heterogeneous across agents).
        self.steps_in_current_location = 0
        self.boredom_threshold = self.random.randint(2, 4)
        # ============================================================
        # >>> END OF MODIFICATION #1 <<<
        # ============================================================

    ## Define movement action
    def move(self):
        # ============================================================
        # >>> MY MODIFICATION #2: Boredom-driven random exploration <<<
        # ============================================================
        # If the agent has been stuck in the same place for too long,
        # it abandons the greedy strategy and moves to a random empty
        # neighbor instead. This simulates exploration behavior.
        if self.steps_in_current_location > self.boredom_threshold:
            possibles = [
                cell
                for cell in self.cell.get_neighborhood(self.vision, include_center=False)
                if cell.is_empty
            ]
            if possibles:
                self.cell = self.random.choice(possibles)
                self.steps_in_current_location = 0
            else:
                # >>> MY MODIFICATION #2a: Handle crowded case <<<
                # If no empty neighbors exist (overcrowding), stay put
                # and continue being bored. Prevents crash when grid is full.
                self.steps_in_current_location += 1
        else:
            # ============================================================
            # >>> END OF MODIFICATION #2 (returning to original logic) <<<
            # ============================================================

            ## Determine currently empty cells within line of sight
            possibles = [
                cell
                for cell in self.cell.get_neighborhood(self.vision, include_center=True)
                if cell.is_empty
            ]

            # ============================================================
            # >>> MY MODIFICATION #3: Safety check for empty possibles <<<
            # ============================================================
            # Bug fix: When the grid becomes crowded, an agent may find
            # zero empty cells within its vision. Without this check,
            # max(sugar_values) below would crash with
            # "max() iterable argument is empty".
            # Solution: If no empty cells, stay put and increment boredom.
            if not possibles:
                self.steps_in_current_location += 1
                return
            # ============================================================
            # >>> END OF MODIFICATION #3 <<<
            # ============================================================

            ## Determine how much sugar is in each possible movement target
            sugar_values = [
                cell.sugar
                for cell in possibles
            ]
            ## Calculate the maximum possible sugar value in possible targets
            max_sugar = max(sugar_values)
            ## Get indices of cell(s) with maximum sugar potential within range
            candidates_index = [
                i for i in range(len(sugar_values)) if math.isclose(sugar_values[i], max_sugar)
            ]
            ## Identify cell(s) with maximum possible sugar
            candidates = [
                possibles[i]
                for i in candidates_index
            ]
            ## Find the closest cells with maximum possible sugar
            min_dist = min(get_distance(self.cell, cell) for cell in candidates)
            final_candidates = [
                cell
                for cell in candidates
                if math.isclose(get_distance(self.cell, cell), min_dist, rel_tol=1e-02)
            ]
            ## Choose one of the closest cells with maximum sugar (randomly if more than one)
            old_cell = self.cell
            self.cell = self.random.choice(final_candidates)

            # ============================================================
            # >>> MY MODIFICATION #4: Update boredom counter <<<
            # ============================================================
            # If agent couldn't find a better spot and stayed put,
            # increment boredom. Otherwise reset the counter.
            if self.cell == old_cell:
                self.steps_in_current_location += 1
            else:
                self.steps_in_current_location = 0
            # ============================================================
            # >>> END OF MODIFICATION #4 <<<
            # ============================================================

    ## Consume sugar in current cell, depleting it, then consume metabolism
    def gather_and_eat(self):
        self.sugar += self.cell.sugar
        self.cell.sugar = 0
        self.sugar -= self.metabolism

    ## If an agent has zero or negative sugar, it dies and is removed from the model
    def see_if_die(self):
        if self.sugar <= 0:
            self.remove()
