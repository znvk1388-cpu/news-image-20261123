// Entry program for make.fun's "Sum up 23 November's world news in one image" bounty.
//
// The repository carries the finished front-page image as entry.png (drawn by
// make_image.py). This program copies it, byte for byte, to the output
// directory as entry.png, so both grader runs produce identical bytes.
// Node 22, standard library only, no network.
//
// Locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// In the grader, MAKEFUN_OUTPUT_DIR is unset and the image goes to /output.

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
