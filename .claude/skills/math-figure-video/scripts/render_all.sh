#!/usr/bin/env bash
set -e
cd /tmp/manim_pyth
MANIM=/tmp/manim-venv/bin/manim
OUT=/tmp/manim_pyth/deliverables
mkdir -p "$OUT"
BASE="media/videos/pyth_scenes/1080p30"

declare -A NAME=( [Phase1]=1_figure [Phase2]=2_left [Phase3]=3_right [Phase4]=4_fill [Full]=5_full )

for SC in Phase1 Phase2 Phase3 Phase4 Full; do
  n=${NAME[$SC]}
  echo ">>> $SC white"
  $MANIM -r 1920,1080 --fps 30 --format mp4 pyth_scenes.py $SC >/dev/null 2>&1
  cp "$BASE/$SC.mp4" "$OUT/${n}_white.mp4"
  echo ">>> $SC transparent"
  TRANSPARENT=1 $MANIM -r 1920,1080 --fps 30 -t --format mov pyth_scenes.py $SC >/dev/null 2>&1
  cp "$BASE/$SC.mov" "$OUT/${n}_alpha.mov"
done
echo "ALL DONE"
ls -la "$OUT"
