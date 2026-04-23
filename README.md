# SugarScape with Boredom Mechanism

Modified version of Epstein and Axtell's SugarScape model. Only `agents.py` was changed.

## What Changed

Added a boredom mechanism to agents. Each agent has a random boredom threshold (5-15 steps). If an agent stays in one location longer than its threshold, it must move to a random neighboring cell instead of following the greedy sugar-seeking behavior.

The idea is that agents get restless and move even if they're in a good spot, which is more realistic than agents staying forever in one place.

## Files

- `agents.py` - **MODIFIED** (added boredom logic to the move() method)
- `model.py` - unchanged
- `app.py` - unchanged  
- `sugar-map.txt` - unchanged

## How to Run

```bash
solara run app.py
```

## Results

The boredom mechanism spreads agents across the map instead of clustering them. But Gini coefficient (inequality) stays the same (0.30) in both versions. 

This shows that spatial distribution and inequality are separate things—you can change where agents live without changing how unequal they become. The inequality is determined by metabolism differences, not by clustering.

Basically: forcing people to move around doesn't automatically make them equal.

## Key Observation

- Baseline (no boredom): agents cluster in 2-3 areas, Gini = 0.30
- Modified (with boredom): agents spread everywhere, Gini = 0.30

Same inequality, different distribution.
