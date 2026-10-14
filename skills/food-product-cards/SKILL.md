---
name: food-product-cards
description: Create food product cards and launch menus from product briefs and photos, with Peet’s styling, exploded ingredient diagrams, selling points, sensory design and complete product strategy. Use for 食品产品卡、饮品分层解读、产品会汇报、菜单与新品介绍.
---

# Food Product Cards

Use the bundled cream/brown visual system, Peet’s logo, menu layout and three-column product layout by default. Keep brand/style fixed unless the user asks to change it. Product inputs are the approved brief, original photo, selling points and strategy. Never substitute generic decoration for product evidence.

## Content before design

Read the full current approved project brief, not only a weekly summary. Resolve conflicts with the user; do not silently choose a convenient version. Maintain source/conflict notes separately from the finished card. First present the exact card text for approval, then render after approval; existing approval counts.

Each product needs:
- A name and concise product proposition.
- Selling points supported by ingredient, provenance or process evidence. Do not invent origin, certification, percentages or nutrition claims.
- Sensory design explaining how actual components create aroma, taste and texture.
- Strategy preserving every material decision in the brief: product role, consumer occasion, new base/platform, portfolio gap, distinction from existing items and intended commercial mechanism where documented. Do not reduce a new bread platform to “enrich choices”. Do not invent a commercial target.

Read [the input contract](references/input.md) when preparing render data and [diagram guidance](references/diagrams.md) before creating images.

## Visuals

Food defaults to a genuine exploded ingredient diagram beside its original photo. Separate components vertically with visible air gaps and correct counts. A photograph with labels is not an exploded diagram. Keep sliced cake tips facing right; do not mirror images with text. Use the user's verified components; unknown manufacturing order must not become a claimed production instruction.

Use the available image generation/editing tool to create diagrams from verified references. Never draw a stock shape and present it as the real product. If no generation tool is available, report that blocker and retain the original photo; do not call the card complete. Keep text labels outside the generated image for crisp typography. Align label y positions after viewing the image.

For beverages, use a single cup split vertically at its centre: the LEFT half preserves the actual product photograph, and the RIGHT half shows a clean continuous cutaway of the verified drink layers. Match the cup rim, base, perspective, scale and layer boundaries across the centre seam. Do not create two cups, two separate full images, or floating exploded layers. Retain realistic gradients, ice and cup texture on the photo half; simplify the cutaway half into legible ingredients. Put leader lines and layer explanations to the right of the cup. Keep selling points, sensory design and full strategy in the card's separate copy column.

Read [beverage guidance](references/beverages.md). Use the original drink photo as an editing reference and preserve its left half. Supply the finished, unlabelled single-cup composite as `cutaway`; the renderer places external labels alongside it. `photo` remains the source asset for review and is not repeated as another full cup on the card. Never copy the example drink's recipe, origin or health claims into another product.

## Build

Prepare UTF-8 JSON following the input contract. Relative asset paths resolve from that JSON's directory. Run:

```sh
python3 scripts/render.py input.json output.html
```

The renderer emits a self-contained HTML file with embedded assets. No third-party Python dependencies. Menu pages precede cards; group menu items by set surcharge, new items first in each group. Card order follows menu order. Preserve an explicitly approved order; packaging goes last when requested. Paginate long menus instead of shrinking text.

The provided layout is 1600 × 1000. Open HTML in a browser and export PDF with backgrounds and CSS page size. Inspect every page at desktop and narrow viewport; check image completeness, text/label collisions, full strategy and page order. Compare PDF page count and rendered pages with HTML before claiming PDF completion.

## Clean final copy

Keep only product-facing content. No sources, production notes, reasoning, “待补”, “结构示意”, redundant photo captions, QA prompts or unresolved assumptions in the finished artifact. Keep evidence backstage. Use semantic HTML containers. Missing required inputs must produce a clear error rather than silently drop content. Public examples must be fictional and contain no confidential launch plans, sales figures, supplier files or private paths.
