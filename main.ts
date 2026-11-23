// news-image-20261123: one image summing up the world news of
// Monday 23 November 2026.
//
// The image itself (entry.png, 1024x1024) is a front page drawn in this
// session: six verified stories of the day, with the date in the masthead.
// This program only copies those exact bytes to the output path, so two
// runs always produce the same file, with no network and no randomness.
//
// Usage:
//   MAKEFUN_OUTPUT_DIR=out node main.ts        # writes out/entry.png
//   node main.ts                               # writes /output/entry.png
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024; // 1 MiB, the competition cap

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

// The source must be a whole PNG inside the size cap; anything else
// would fail the gate, so refuse loudly instead of writing bad bytes.
const bytes = readFileSync(source);
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}
if (!bytes.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
  throw new Error("entry.png does not start with the PNG signature");
}
if (statSync(source).size !== bytes.length) {
  throw new Error("entry.png changed while reading it");
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`wrote ${target} (${bytes.length} bytes)`);
