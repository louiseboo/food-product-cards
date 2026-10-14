# Renderer input

See `examples/demo.json` in the repository for an executable fictional example. Asset paths are relative to the input JSON, or absolute local paths. PNG, JPEG, WebP and SVG are supported. Inputs are trusted local assets; do not use SVGs obtained from untrusted sources without sanitising them.

Root: `title` (string), `products` (non-empty list), optional `menu` (list of groups), optional `menu_subtitle` (string).

Each product: `id`, `name`, `subtitle`, `photo`, `sections`, `labels`; optional `kind` = `food` (default) or `beverage`.

Food requires `diagram` (exploded view). Beverage requires `cutaway` (one unlabelled image of the same cup: real-photo left half and continuous cutaway right half). `photo` is the original source photo and remains required for verification. Beverage `labels` use y percentages within the composite canvas; use the same aspect ratio in the image and `cutaway_ratio` (width / height, default 0.8). Trim excess image margins before assigning labels. The renderer does not perform image editing. Do not pass two unaligned cup images and expect it to join them.

`sections`: exactly three objects with `heading`, `title`, `body`, in selling point / sensory / strategy order. Body retains the approved full meaning; split into another card if too long.

`labels`: list of `{text, y}`; `y` is vertical percent in [0, 95]. Food needs at least two separated layers. Beverage needs at least one ingredient label.

Menu group: `title`, `items` list. Item: `product_id`, `price` (display string), optional `new` (boolean), `core` (boolean), `note` (string). Group titles contain approved surcharge language. The renderer sorts new first stably within each group and orders cards by first menu occurrence, then appends any cards absent from menu. At most three groups and six entries per group per deck: split larger menus into separate decks/pages before rendering.

Do not put sourcing notes, internal file paths, credentials or unpublished business data in public examples. Rendering embeds the supplied images, so review output before sharing.
