#!/bin/bash
# Image Rename Script — All 202 images across 4 folders
# Generated from visual inspection of every image
# Batches of 5, 15s sleep between batches

set -e

BASE="/Users/jockib/Desktop/CALM-RIO-V1/assets/images/imgs"
BATCH=0

run_batch() {
  BATCH=$((BATCH + 1))
  echo "=== Batch $BATCH ==="
  for cmd in "$@"; do
    eval "$cmd"
  done
  echo "Sleeping 15s..."
  sleep 15
}

echo "Starting FALM renames (70 images)..."
cd "$BASE/FALM"

# --- FALM BATCH 1 ---
run_batch \
  'mv "_SLR5068 И Olivier Schindler.webp" "cottage-blue-shutters-exterior-01.webp"' \
  'mv "_SLR5072 И Olivier Schindler.webp" "cottage-blue-shutters-exterior-02.webp"' \
  'mv "_SLR5073 И Olivier Schindler.webp" "cottage-blue-shutters-exterior-night-01.webp"' \
  'mv "_SLR5077 И Olivier Schindler.webp" "cottage-garden-deckchairs-01.webp"' \
  'mv "_SLR5079 И Olivier Schindler.webp" "cottage-pergola-green-sails-01.webp"'

# --- FALM BATCH 2 ---
run_batch \
  'mv "_SLR5084 И Olivier Schindler.webp" "cottage-pergola-deckchairs-01.webp"' \
  'mv "_SLR5086 И Olivier Schindler.webp" "cottage-garden-deckchairs-02.webp"' \
  'mv "_SLR5087 И Olivier Schindler.webp" "cottage-exterior-blue-shutters-03.webp"' \
  'mv "_SLR5088 И Olivier Schindler.webp" "cottage-harbor-view-01.webp"' \
  'mv "_SLR5089 И Olivier Schindler.webp" "cottage-garden-pergola-02.webp"'

# --- FALM BATCH 3 ---
run_batch \
  'mv "_SLR5090 И Olivier Schindler.webp" "cottage-outdoor-dining-01.webp"' \
  'mv "_SLR5092 И Olivier Schindler.webp" "cottage-exterior-night-02.webp"' \
  'mv "_SLR5097 И Olivier Schindler.webp" "cottage-exterior-night-03.webp"' \
  'mv "_SLR5099 И Olivier Schindler.webp" "cottage-garden-path-01.webp"' \
  'mv "_SLR5100 И Olivier Schindler.webp" "cottage-blue-shutters-exterior-04.webp"'

# --- FALM BATCH 4 ---
run_batch \
  'mv "_SLR5102 И Olivier Schindler.webp" "cottage-garden-bbq-01.webp"' \
  'mv "_SLR5103 И Olivier Schindler.webp" "cottage-garden-deckchairs-03.webp"' \
  'mv "_SLR5106 И Olivier Schindler.webp" "cottage-grey-wallpaper-bedroom-01.webp"' \
  'mv "_SLR5109 И Olivier Schindler.webp" "cottage-grey-wallpaper-bedroom-02.webp"' \
  'mv "_SLR5111 И Olivier Schindler.webp" "cottage-floral-wallpaper-bedroom-01.webp"'

# --- FALM BATCH 5 ---
run_batch \
  'mv "_SLR5113 И Olivier Schindler.webp" "cottage-floral-wallpaper-bedroom-02.webp"' \
  'mv "_SLR5114 И Olivier Schindler.webp" "cottage-grey-wallpaper-bedroom-03.webp"' \
  'mv "_SLR5117 И Olivier Schindler.webp" "cottage-outdoor-dining-02.webp"' \
  'mv "_SLR5121 И Olivier Schindler.webp" "cottage-exterior-05.webp"' \
  'mv "_SLR5124 И Olivier Schindler.webp" "cottage-exterior-06.webp"'

# --- FALM BATCH 6 ---
run_batch \
  'mv "_SLR5125 И Olivier Schindler.webp" "cottage-harbor-view-02.webp"' \
  'mv "_SLR5126 И Olivier Schindler.webp" "cottage-garden-path-02.webp"' \
  'mv "_SLR5128 И Olivier Schindler.webp" "cottage-exterior-night-04.webp"' \
  'mv "_SLR5129 И Olivier Schindler.webp" "cottage-exterior-night-05.webp"' \
  'mv "_SLR5136 И Olivier Schindler.webp" "cottage-garden-pergola-03.webp"'

# --- FALM BATCH 7 ---
run_batch \
  'mv "_SLR5138 И Olivier Schindler.webp" "cottage-blue-shutters-exterior-07.webp"' \
  'mv "_SLR5145 И Olivier Schindler.webp" "cottage-grey-wallpaper-bedroom-04.webp"' \
  'mv "_SLR5146 И Olivier Schindler.webp" "cottage-garden-deckchairs-04.webp"' \
  'mv "_SLR5147 И Olivier Schindler.webp" "cottage-harbor-view-03.webp"' \
  'mv "_SLR5149 И Olivier Schindler.webp" "cottage-exterior-day-01.webp"'

# --- FALM BATCH 8 ---
run_batch \
  'mv "_SLR5151 И Olivier Schindler.webp" "cottage-exterior-day-02.webp"' \
  'mv "_SLR5153 И Olivier Schindler.webp" "cottage-garden-path-03.webp"' \
  'mv "_SLR5159 И Olivier Schindler.webp" "cottage-exterior-day-03.webp"' \
  'mv "_SLR5163 И Olivier Schindler.webp" "cottage-garden-deckchairs-05.webp"' \
  'mv "_SLR5168 И Olivier Schindler.webp" "cottage-exterior-day-04.webp"'

# --- FALM BATCH 9 ---
run_batch \
  'mv "_SLR5170 И Olivier Schindler.webp" "cottage-harbor-view-04.webp"' \
  'mv "_SLR5173 И Olivier Schindler.webp" "cottage-garden-path-04.webp"' \
  'mv "_SLR5180 И Olivier Schindler.webp" "cottage-floral-wallpaper-bedroom-03.webp"' \
  'mv "_SLR5181 И Olivier Schindler.webp" "cottage-grey-wallpaper-bedroom-05.webp"' \
  'mv "_SLR5183 И Olivier Schindler.webp" "cottage-exterior-day-05.webp"'

# --- FALM BATCH 10 (Modern style starts) ---
run_batch \
  'mv "_SLR5395 И Olivier Schindler.webp" "modern-living-grey-tiles-01.webp"' \
  'mv "_SLR5397 И Olivier Schindler.webp" "modern-living-grey-tiles-02.webp"' \
  'mv "_SLR5399 И Olivier Schindler.webp" "modern-kitchen-black-countertop-01.webp"' \
  'mv "_SLR5401 И Olivier Schindler.webp" "modern-kitchen-light-wood-01.webp"' \
  'mv "_SLR5403 И Olivier Schindler.webp" "modern-kitchen-black-rangehood-01.webp"'

# --- FALM BATCH 11 ---
run_batch \
  'mv "_SLR5406 И Olivier Schindler.webp" "modern-kitchen-double-oven-01.webp"' \
  'mv "_SLR5407 И Olivier Schindler.webp" "modern-living-blue-accent-01.webp"' \
  'mv "_SLR5409 И Olivier Schindler.webp" "modern-bedroom-botanical-01.webp"' \
  'mv "_SLR5411 И Olivier Schindler.webp" "modern-bedroom-botanical-02.webp"' \
  'mv "_SLR5412 И Olivier Schindler.webp" "modern-bedroom-wallpaper-01.webp"'

# --- FALM BATCH 12 ---
run_batch \
  'mv "_SLR5419 И Olivier Schindler.webp" "modern-bedroom-wallpaper-02.webp"' \
  'mv "_SLR5423 И Olivier Schindler.webp" "modern-bathroom-01.webp"' \
  'mv "_SLR5424 И Olivier Schindler.webp" "modern-bathroom-02.webp"' \
  'mv "_SLR5429 И Olivier Schindler.webp" "modern-living-open-plan-01.webp"' \
  'mv "_SLR5466 И Olivier Schindler.webp" "modern-kitchen-open-plan-01.webp"'

# --- FALM BATCH 13 ---
run_batch \
  'mv "_SLR5498 И Olivier Schindler.webp" "modern-bedroom-wallpaper-03.webp"' \
  'mv "_SLR5547 И Olivier Schindler.webp" "modern-kitchen-counter-detail-01.webp"' \
  'mv "_SLR5551 И Olivier Schindler.webp" "modern-living-grey-tiles-03.webp"' \
  'mv "_SLR5552 И Olivier Schindler.webp" "modern-bedroom-botanical-03.webp"' \
  'mv "_SLR5554 И Olivier Schindler.webp" "modern-kitchen-bar-stools-01.webp"'

# --- FALM BATCH 14 ---
run_batch \
  'mv "_SLR5556 И Olivier Schindler.webp" "modern-living-blue-accent-02.webp"' \
  'mv "_SLR5558 И Olivier Schindler.webp" "modern-bedroom-white-bedding-01.webp"' \
  'mv "_SLR5562 И Olivier Schindler.webp" "modern-kitchen-black-countertop-02.webp"' \
  'mv "_SLR5565 И Olivier Schindler.webp" "modern-living-open-plan-02.webp"' \
  'mv "_SLR5568 И Olivier Schindler.webp" "modern-bathroom-03.webp"'

echo ""
echo "FALM complete (70 images renamed). Moving to Face au phare..."
echo ""

cd "$BASE/Face au phare"

# --- FACE AU PHARE BATCH 1 ---
run_batch \
  'mv "_SLR5194 И Olivier Schindler.webp" "face-exterior-yellow-01.webp"' \
  'mv "_SLR5198 И Olivier Schindler.webp" "face-exterior-yellow-02.webp"' \
  'mv "_SLR5205 И Olivier Schindler.webp" "face-sign-01.webp"' \
  'mv "_SLR5208 И Olivier Schindler.webp" "face-exterior-red-roof-01.webp"' \
  'mv "_SLR5215 И Olivier Schindler.webp" "face-living-blue-white-01.webp"'

# --- FACE AU PHARE BATCH 2 ---
run_batch \
  'mv "_SLR5223 И Olivier Schindler.webp" "face-living-fireplace-01.webp"' \
  'mv "_SLR5225 И Olivier Schindler.webp" "face-living-french-doors-01.webp"' \
  'mv "_SLR5231 И Olivier Schindler.webp" "face-bedroom-anchor-pillow-01.webp"' \
  'mv "_SLR5235 И Olivier Schindler.webp" "face-bedroom-blue-white-01.webp"' \
  'mv "_SLR5241 И Olivier Schindler.webp" "face-bedroom-nautical-01.webp"'

# --- FACE AU PHARE BATCH 3 ---
run_batch \
  'mv "_SLR5245 И Olivier Schindler.webp" "face-bedroom-nautical-02.webp"' \
  'mv "_SLR5250 И Olivier Schindler.webp" "face-bedroom-blue-white-02.webp"' \
  'mv "_SLR5254 И Olivier Schindler.webp" "face-bathroom-stone-01.webp"' \
  'mv "_SLR5262 И Olivier Schindler.webp" "face-bathroom-glass-shower-01.webp"' \
  'mv "_SLR5264 И Olivier Schindler.webp" "face-bedroom-lighthouse-art-01.webp"'

# --- FACE AU PHARE BATCH 4 ---
run_batch \
  'mv "_SLR5267 И Olivier Schindler.webp" "face-garden-palm-01.webp"' \
  'mv "_SLR5270 И Olivier Schindler.webp" "face-garden-deckchairs-01.webp"' \
  'mv "_SLR5276 И Olivier Schindler.webp" "face-beach-view-01.webp"' \
  'mv "_SLR5277 И Olivier Schindler.webp" "face-beach-buoys-01.webp"' \
  'mv "_SLR5278 И Olivier Schindler.webp" "face-harbor-ferris-wheel-01.webp"'

# --- FACE AU PHARE BATCH 5 ---
run_batch \
  'mv "_SLR5281 И Olivier Schindler.webp" "face-ice-cream-cart-01.webp"' \
  'mv "_SLR5282 И Olivier Schindler.webp" "face-living-accents-01.webp"' \
  'mv "_SLR5284 И Olivier Schindler.webp" "face-bedroom-white-01.webp"' \
  'mv "_SLR5287 И Olivier Schindler.webp" "face-bedroom-blue-striped-01.webp"' \
  'mv "_SLR5293 И Olivier Schindler.webp" "face-garden-path-01.webp"'

# --- FACE AU PHARE BATCH 6 ---
run_batch \
  'mv "_SLR5295 И Olivier Schindler.webp" "face-bathroom-stone-02.webp"' \
  'mv "_SLR5299 И Olivier Schindler.webp" "face-exterior-garden-01.webp"' \
  'mv "_SLR5301 И Olivier Schindler.webp" "face-bedroom-nautical-03.webp"' \
  'mv "_SLR5304 И Olivier Schindler.webp" "face-living-white-brick-01.webp"' \
  'mv "_SLR5364 И Olivier Schindler.webp" "face-beach-people-01.webp"'

# --- FACE AU PHARE BATCH 7 ---
run_batch \
  'mv "_SLR5368 И Olivier Schindler.webp" "face-street-sea-view-01.webp"' \
  'mv "_SLR5371 И Olivier Schindler.webp" "face-bedroom-blue-white-03.webp"' \
  'mv "_SLR5378 И Olivier Schindler.webp" "face-exterior-blue-shutters-01.webp"' \
  'mv "_SLR5381 И Olivier Schindler.webp" "face-garden-palm-02.webp"' \
  'mv "_SLR5388 И Olivier Schindler.webp" "face-bedroom-twin-01.webp"'

# --- FACE AU PHARE BATCH 8 ---
run_batch \
  'mv "_SLR5393 И Olivier Schindler.webp" "face-vacances-pillow-01.webp"'

echo ""
echo "Face au phare complete (36 images renamed). Moving to Lazure IO..."
echo ""

cd "$BASE/Lazure IO"

# --- LAZURE IO BATCH 1 ---
run_batch \
  'mv "_SLR4938 И Olivier Schindler.webp" "latelier-living-blue-sofa-01.webp"' \
  'mv "_SLR4939 И Olivier Schindler.webp" "latelier-living-blue-sofa-02.webp"' \
  'mv "_SLR4941 И Olivier Schindler.webp" "latelier-kitchen-teal-cabinets-01.webp"' \
  'mv "_SLR4945 И Olivier Schindler.webp" "latelier-kitchen-pass-through-01.webp"' \
  'mv "_SLR4947 И Olivier Schindler.webp" "latelier-living-cream-armchair-01.webp"'

# --- LAZURE IO BATCH 2 ---
run_batch \
  'mv "_SLR4948 И Olivier Schindler.webp" "latelier-living-wood-stove-01.webp"' \
  'mv "_SLR4952 И Olivier Schindler.webp" "latelier-living-open-plan-01.webp"' \
  'mv "_SLR4953 И Olivier Schindler.webp" "latelier-living-beams-01.webp"' \
  'mv "_SLR4955 И Olivier Schindler.webp" "latelier-dining-area-01.webp"' \
  'mv "_SLR4956 И Olivier Schindler.webp" "latelier-kitchen-teal-detail-01.webp"'

# --- LAZURE IO BATCH 3 ---
run_batch \
  'mv "_SLR4963 И Olivier Schindler.webp" "latelier-bedroom-botanical-01.webp"' \
  'mv "_SLR4965 И Olivier Schindler.webp" "latelier-bedroom-botanical-02.webp"' \
  'mv "_SLR4967 И Olivier Schindler.webp" "latelier-bedroom-white-bedding-01.webp"' \
  'mv "_SLR4968 И Olivier Schindler.webp" "latelier-bedroom-terracotta-01.webp"' \
  'mv "_SLR4971 И Olivier Schindler.webp" "latelier-loft-mezzanine-01.webp"'

# --- LAZURE IO BATCH 4 ---
run_batch \
  'mv "_SLR4973 И Olivier Schindler.webp" "latelier-kids-room-colorful-01.webp"' \
  'mv "_SLR4975 И Olivier Schindler.webp" "latelier-kids-room-babar-01.webp"' \
  'mv "_SLR4976 И Olivier Schindler.webp" "latelier-kids-room-teddy-01.webp"' \
  'mv "_SLR4977 И Olivier Schindler.webp" "latelier-bedroom-blue-cream-01.webp"' \
  'mv "_SLR4978 И Olivier Schindler.webp" "latelier-bedroom-grey-headboard-01.webp"'

# --- LAZURE IO BATCH 5 ---
run_batch \
  'mv "_SLR4981 И Olivier Schindler.webp" "latelier-bathroom-coral-wallpaper-01.webp"' \
  'mv "_SLR4985 И Olivier Schindler.webp" "latelier-bathroom-double-vanity-01.webp"' \
  'mv "_SLR4986 И Olivier Schindler.webp" "latelier-bathroom-glass-shower-01.webp"' \
  'mv "_SLR4989 И Olivier Schindler.webp" "latelier-garden-pergola-curtains-01.webp"' \
  'mv "_SLR4991 И Olivier Schindler.webp" "latelier-garden-daybed-purple-01.webp"'

# --- LAZURE IO BATCH 6 ---
run_batch \
  'mv "_SLR4992 И Olivier Schindler.webp" "latelier-garden-adirondack-01.webp"' \
  'mv "_SLR4994 И Olivier Schindler.webp" "latelier-exterior-white-brown-01.webp"' \
  'mv "_SLR4995 И Olivier Schindler.webp" "latelier-exterior-terracotta-roof-01.webp"' \
  'mv "_SLR4999 И Olivier Schindler.webp" "latelier-exterior-stone-path-01.webp"' \
  'mv "_SLR5000 И Olivier Schindler.webp" "latelier-exterior-brown-shutters-01.webp"'

# --- LAZURE IO BATCH 7 ---
run_batch \
  'mv "_SLR5003 И Olivier Schindler.webp" "latelier-nameplate-01.webp"' \
  'mv "_SLR5006 И Olivier Schindler.webp" "latelier-nameplate-02.webp"' \
  'mv "_SLR5007 И Olivier Schindler.webp" "latelier-hallway-01.webp"' \
  'mv "_SLR5008 И Olivier Schindler.webp" "latelier-hallway-coat-rack-01.webp"' \
  'mv "_SLR5010 И Olivier Schindler.webp" "latelier-garden-bbq-01.webp"'

# --- LAZURE IO BATCH 8 ---
run_batch \
  'mv "_SLR5012 И Olivier Schindler.webp" "latelier-garden-pergola-curtains-02.webp"' \
  'mv "_SLR5013 И Olivier Schindler.webp" "latelier-garden-daybed-02.webp"' \
  'mv "_SLR5019 И Olivier Schindler.webp" "latelier-living-navy-sofa-01.webp"' \
  'mv "_SLR5022 И Olivier Schindler.webp" "latelier-kitchen-light-wood-01.webp"' \
  'mv "_SLR5023 И Olivier Schindler.webp" "latelier-living-open-plan-02.webp"'

# --- LAZURE IO BATCH 9 ---
run_batch \
  'mv "_SLR5024 И Olivier Schindler.webp" "latelier-bedroom-botanical-03.webp"' \
  'mv "_SLR5025 И Olivier Schindler.webp" "latelier-bedroom-floral-01.webp"' \
  'mv "_SLR5027 И Olivier Schindler.webp" "latelier-living-cream-01.webp"' \
  'mv "_SLR5036 И Olivier Schindler.webp" "latelier-kitchen-teal-cabinets-02.webp"' \
  'mv "_SLR5037 И Olivier Schindler.webp" "latelier-living-grey-beams-01.webp"'

# --- LAZURE IO BATCH 10 ---
run_batch \
  'mv "_SLR5038 И Olivier Schindler.webp" "latelier-kitchen-open-shelf-01.webp"' \
  'mv "_SLR5039 И Olivier Schindler.webp" "latelier-dining-wood-table-01.webp"' \
  'mv "_SLR5052 И Olivier Schindler.webp" "latelier-bedroom-terracotta-02.webp"' \
  'mv "_SLR5054 И Olivier Schindler.webp" "latelier-loft-railing-01.webp"' \
  'mv "_SLR5055 И Olivier Schindler.webp" "latelier-kids-room-colorful-02.webp"'

# --- LAZURE IO BATCH 11 ---
run_batch \
  'mv "_SLR5059 И Olivier Schindler.webp" "latelier-bedroom-blue-cream-02.webp"' \
  'mv "_SLR5060 И Olivier Schindler.webp" "latelier-bathroom-fern-wallpaper-01.webp"' \
  'mv "_SLR5063 И Olivier Schindler.webp" "latelier-garden-adirondack-02.webp"' \
  'mv "_SLR5064 И Olivier Schindler.webp" "latelier-garden-wood-deck-01.webp"' \
  'mv "_SLR5184 И Olivier Schindler.webp" "latelier-exterior-white-stucco-01.webp"'

# --- LAZURE IO BATCH 12 ---
run_batch \
  'mv "_SLR5186 И Olivier Schindler.webp" "latelier-exterior-terracotta-02.webp"' \
  'mv "_SLR5395 И Olivier Schindler.webp" "latelier-living-pass-through-01.webp"' \
  'mv "_SLR5397 И Olivier Schindler.webp" "latelier-kitchen-black-counter-01.webp"' \
  'mv "_SLR5399 И Olivier Schindler.webp" "latelier-living-wood-stove-02.webp"' \
  'mv "_SLR5401 И Olivier Schindler.webp" "latelier-bedroom-white-02.webp"'

# --- LAZURE IO BATCH 13 ---
run_batch \
  'mv "_SLR5403 И Olivier Schindler.webp" "latelier-bedroom-botanical-04.webp"' \
  'mv "_SLR5406 И Olivier Schindler.webp" "latelier-kitchen-teal-detail-02.webp"' \
  'mv "_SLR5407 И Olivier Schindler.webp" "latelier-living-blue-sofa-03.webp"' \
  'mv "_SLR5409 И Olivier Schindler.webp" "latelier-dining-pass-through-01.webp"' \
  'mv "_SLR5411 И Olivier Schindler.webp" "latelier-garden-curtains-01.webp"'

# --- LAZURE IO BATCH 14 ---
run_batch \
  'mv "_SLR5412 И Olivier Schindler.webp" "latelier-garden-daybed-purple-02.webp"' \
  'mv "_SLR5419 И Olivier Schindler.webp" "latelier-exterior-white-brown-02.webp"' \
  'mv "_SLR5423 И Olivier Schindler.webp" "latelier-bathroom-double-02.webp"' \
  'mv "_SLR5424 И Olivier Schindler.webp" "latelier-hallway-02.webp"' \
  'mv "_SLR5429 И Olivier Schindler.webp" "latelier-bedroom-loft-02.webp"'

# --- LAZURE IO BATCH 15 ---
run_batch \
  'mv "_SLR5501 И Olivier Schindler.webp" "latelier-garden-pergola-night-01.webp"' \
  'mv "_SLR5505 И Olivier Schindler.webp" "latelier-garden-pergola-night-02.webp"' \
  'mv "_SLR5508 И Olivier Schindler.webp" "latelier-garden-deck-night-01.webp"' \
  'mv "_SLR5509 И Olivier Schindler.webp" "latelier-exterior-night-patio-01.webp"' \
  'mv "_SLR5510 И Olivier Schindler.webp" "latelier-garden-canopy-night-01.webp"'

# --- LAZURE IO BATCH 16 ---
run_batch \
  'mv "_SLR5512 И Olivier Schindler.webp" "latelier-garden-awning-led-01.webp"' \
  'mv "_SLR5514 И Olivier Schindler.webp" "latelier-garden-dining-night-01.webp"' \
  'mv "_SLR5522 И Olivier Schindler.webp" "latelier-decorative-fish-01.webp"' \
  'mv "_SLR5525 И Olivier Schindler.webp" "latelier-garden-pergola-night-03.webp"' \
  'mv "_SLR5535 И Olivier Schindler.webp" "latelier-exterior-night-wide-01.webp"'

echo ""
echo "Lazure IO complete (80 images renamed). Moving to imgs_2..."
echo ""

cd "$BASE/imgs_2"

# --- IMGS_2 BATCH 1 ---
run_batch \
  'mv "_SLR6150 И Olivier Schindler.webp" "loft-twin-room-honeycomb-01.webp"' \
  'mv "_SLR6152 И Olivier Schindler.webp" "loft-twin-room-honeycomb-02.webp"' \
  'mv "_SLR6154 И Olivier Schindler.webp" "loft-twin-room-wardrobe-01.webp"' \
  'mv "_SLR6155 И Olivier Schindler.webp" "loft-twin-room-front-01.webp"' \
  'mv "_SLR6158 И Olivier Schindler.webp" "loft-twin-room-wide-01.webp"'

# --- IMGS_2 BATCH 2 ---
run_batch \
  'mv "_SLR6160 И Olivier Schindler.webp" "loft-bathroom-geometric-tile-01.webp"' \
  'mv "_SLR6164 И Olivier Schindler.webp" "loft-bathroom-shower-01.webp"' \
  'mv "_SLR6165 И Olivier Schindler.webp" "loft-bathroom-vanity-01.webp"' \
  'mv "_SLR6167 И Olivier Schindler.webp" "loft-bathroom-wide-01.webp"' \
  'mv "_SLR6168 И Olivier Schindler.webp" "loft-exterior-door-closeup-01.webp"'

# --- IMGS_2 BATCH 3 ---
run_batch \
  'mv "_SLR6169 И Olivier Schindler.webp" "loft-garden-grasses-01.webp"' \
  'mv "_SLR6172 И Olivier Schindler.webp" "loft-exterior-front-01.webp"' \
  'mv "_SLR6174 И Olivier Schindler.webp" "loft-exterior-front-02.webp"' \
  'mv "_SLR6178 И Olivier Schindler.webp" "loft-exterior-wide-01.webp"' \
  'mv "_SLR6182 И Olivier Schindler.webp" "loft-exterior-mailbox-01.webp"'

# --- IMGS_2 BATCH 4 ---
run_batch \
  'mv "_SLR6186 И Olivier Schindler.webp" "loft-lifestyle-sofa-phone-01.webp"'

echo ""
echo "=== ALL 202 IMAGES RENAMED ==="
echo "FALM: 70 images"
echo "Face au phare: 36 images"
echo "Lazure IO: 80 images"
echo "imgs_2: 16 images"
echo "Total: 202 images"
