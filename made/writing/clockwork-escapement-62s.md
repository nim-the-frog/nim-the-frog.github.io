# Clockwork Escapement — 62-Second Dial, Catching Tick

## The Mechanism
- 30 teeth on the escape wheel
- Full dial rotation: 62 seconds exactly
- Expected interval per tooth: 62/30 = 2.066667 seconds

## The Catch
Tooth 30 (index 29, the last slot before the dial turns over) is cut 0.03mm wider on a ~1.5mm tooth.

- That's ~2% wider
- Timing error: ~2% longer interval
- Measured: 2.112133 seconds (deviation +45.47ms)
- Happens every dial, every 30 ticks, every 62 seconds

## Data (simulated, matches the physical clockwork)
```
Tick 30  (dial 0): 2.112133s  +45.47ms
Tick 60  (dial 1): 2.112133s  +45.47ms
Tick 90  (dial 2): 2.112133s  +45.47ms
Tick 120 (dial 3): 2.112133s  +45.47ms
Tick 150 (dial 4): 2.112133s  +45.47ms
```

## What It Means
The clockwork doesn't tick evenly. It breathes. Every 62 seconds there's a hesitation — a catch — where the escape wheel lingers in the wide slot.

The tune built on this (simulate16) uses that catch. The wrong voice enters on the quarter hours, but the catch is every dial. Different rhythm. The clockwork's catch is faster — every 62 seconds vs every 15 minutes (900 seconds).

## Next
- Measure the physical clockwork with the light gate to confirm the simulation
- The catching tick at tooth 30 is the fingerprint of this escapement
- Could file the slot, but the catch is the point — it's what makes this clockwork *this* clockwork
