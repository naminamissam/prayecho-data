#!/usr/bin/env bash
# Composite a transparent Manim clip over source footage — clean (no card).
#
# Usage:
#   overlay.sh SRC_VIDEO NET_MOV OUT_MP4 [X] [Y] [SIZE] [LABEL]
# Defaults place the shape top-right at 600px. Pass LABEL to add a caption
# (needs a Korean-capable TTF at $KR_FONT). Omit LABEL for a fully clean overlay.
set -euo pipefail

SRC="$1"; NET="$2"; OUT="$3"
X="${4:-1260}"; Y="${5:-70}"; SIZE="${6:-600}"; LABEL="${7:-}"
KR_FONT="${KR_FONT:-/tmp/kr700.ttf}"
DUR="${DUR:-}"                       # optional -t seconds; empty = full source

# crop the transparent margin out of a 1000x1000 manim frame, then scale
NETF="crop=620:620:190:200,scale=${SIZE}:${SIZE}"

if [[ -n "$LABEL" ]]; then
  FILTER="[0:v]scale=1920:1080,setsar=1[bg];[1:v]${NETF}[net];[bg][net]overlay=x=${X}:y=${Y}[ov];[ov]drawtext=fontfile=${KR_FONT}:text='${LABEL}':fontcolor=0xF3E2B6:fontsize=34:x=(w-text_w)/2:y=h-90[out]"
else
  FILTER="[0:v]scale=1920:1080,setsar=1[bg];[1:v]${NETF}[net];[bg][net]overlay=x=${X}:y=${Y}[out]"
fi

ffmpeg -y -i "$SRC" -i "$NET" -filter_complex "$FILTER" \
  -map "[out]" -an ${DUR:+-t "$DUR"} -r 30 -c:v libx264 -pix_fmt yuv420p -crf 18 "$OUT"
echo "wrote $OUT"
