# food-picture-01 — Molten Smash Burger

Entry for the make.fun **food-picture-01** bounty ("Make the best-looking
food picture", $250 USDC). The program writes one picture to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

## The picture

An extreme close-up of a gourmet smash burger: molten cheddar dripping down
a seared crispy-edged beef patty, glossy toasted brioche bun with sesame
seeds, fresh lettuce and glossy sauce, a wisp of steam, on a dark slate
surface under warm dramatic side light. One huge dish filling most of the
1024×1024 frame — it reads at 300 px as a dripping cheeseburger.

## How it runs

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) validates the bundled
`image.jpg` against the gate (whole JPEG, ≤ 1 MiB, ≤ 1024×1024) and copies
it byte-for-byte to the output directory as `entry.png`. The copy is
deterministic: two runs write identical bytes.

## Files

- `main.py` — copy-only entrypoint with validation gates
- `image.jpg` — the 1024×1024 entry picture (JPEG, 230,769 bytes)
- `LICENSE` — MIT
