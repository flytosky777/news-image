[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/flytosky777/news-image/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/flytosky777/news-image/reward.svg)](https://make.fun/bounty/news-image-20261123)

# The World in One Day — Monday 23 November 2026

A make.fun entry for
[news-image-20261123](https://make.fun/bounty/news-image-20261123):
one image that sums up the world's news of Monday 23 November 2026.

## The image

`entry.png` (1024×1024, ~134 KB) is a front page drawn in this session
with PIL: the date in the masthead, then six stories, each verified against
reporting of the day:

1. **COP31 climate talks collapse with no deal** — UN negotiations in
   Turkey end without an agreement after the EU rejects any pact with no
   language on phasing out fossil fuels. (The Hindu, BBC)
2. **Trump threatens to sink Iranian ships** — after a US strike on an oil
   tanker; Houthis claim hits on a Saudi refinery. (FeedCast, Indian Express)
3. **AI sell-off rattles world markets** — Seoul's KOSPI plunges 5%; US
   futures rebound as Nasdaq jumps 3%. (Hindu BusinessLine, Fortune)
4. **Democrats win biggest House majority since 1992** — 258 seats clinched
   after a North Carolina recount win. (BBC)
5. **Boy, 7, pulled alive from rubble** — rescuers free a child hours after
   a Russian strike on Ukraine. (BBC)
6. **Mets sign Skubal for a record $450m** — a nine-year deal, the richest
   ever for a pitcher. (FeedCast)

## The program

`main.ts` (Node 22, no dependencies) copies `entry.png` byte for byte to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`), after
checking it is a whole PNG inside the 1 MiB cap. No network, no randomness:
two runs write identical bytes.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT. See [LICENSE](LICENSE).
