# SugarScape Boredom Mod

My ABM midterm project. Takes the SugarScape model and adds a boredom mechanism to the agents, so they don't always follow the greedy rule.

## What I did

In the original model, agents always move to the cell with the most sugar in their vision. I thought this was kind of unrealistic — real people don't always optimize, they get bored and try new things even when there's no good reason to. So I added a boredom counter to each agent. If they stay in one spot for too long, they just move randomly.

I wanted to see if this would make the society more equal (lower Gini). Turns out it actually made inequality a bit *higher* at the peak, which I didn't expect. The paper explains why I think that happened.

## Files

- `agents.py` — added the boredom stuff here
- `model.py` — changed a few default parameters so agents live longer (otherwise they die before they have time to get bored lol)
- `app.py` — didn't touch this
- `sugar-map.txt` — didn't touch this either
- `SugarScape_Midterm_Paper.docx` — the paper

All my changes in the code are marked with `>>> MY MODIFICATION #N <<<` so they're easy to find.

## How to run

```
solara run app.py
```

Then go to `localhost:8765` in your browser.

You need `mesa` and `solara` installed.

## Results (short version)

Ran both versions with seed 42 for 5000+ steps:

- Original peak Gini: ~0.36
- Modified peak Gini: ~0.39
- Both settle around 0.28 long-term

So boredom actually made things worse in the short run. My guess for why this happened is in the paper.
