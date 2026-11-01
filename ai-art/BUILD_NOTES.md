# Build Notes: Woven Memory

*Work in progress.* Sections marked **In my words** are still to be filled in by me.

## The idea

*Woven Memory* is a digital version of my photo-weaving technique. A family image (to start, my painting of a man pulling a child in a red wagon, recreated from an old family photo) is cut into strips and woven over-under with strips of a fluid color "pour" in my palette. The image is toned to look like faded film, with grain and a light leak.

The goal of the assignment was to use **context stuffing**: give the AI my own taste, style, and past work all at once, so it mimics *my* aesthetic instead of producing something generic. My context is in [`style-pack/`](style-pack/).

## Tools

- **Claude** (chat at claude.ai) as the AI collaborator. It read my style pack and photos of my work, proposed the concept, and wrote the code.
- **The artwork tool itself:** [`woven-memory.html`](woven-memory.html), a single web page that runs in any browser. No installs, no account, works offline (except for fonts).
- My own family photos and paintings as source material.

## Process

1. **Started physical, switched to digital.** I first planned a physical piece (painting, collage, or craft) with the AI as planner. I switched to digital art so the AI could make the piece directly and I could iterate on it.
2. **Built my style pack.** I answered seven questions about format, colors, mood, subject, inspiration, my own work, and dislikes, and uploaded 15 photos of my artwork. This was the entire "context" stuffed into the AI.
3. **The AI's reading of my work.** It identified weaving and grids, family memory and film, and fluid ink as my recurring threads (see `style-pack/STYLE_PACK.md`).
4. **Concept.** It proposed weaving a family image with a color pour, echoing my bark photo-weavings and loom weavings. I agreed.
5. **Tool instead of a single image.** Rather than one fixed picture, the AI built an interactive tool so that I make the creative decisions: weave pattern, strip size, gaps, hand-cut wobble, how muted or vivid the color is, film fade, grain, and light leak. I can also weave in my own family photos, which never leave my computer.
6. **Iterating.** **In my words:** which settings and versions I chose and why. What felt like me, and what didn't. Which outputs are in `outputs/`.

## Failures and how they were fixed

1. **Wrong photo.** The AI's first version wove my sneakers-in-a-box study instead of the wagon painting. It mixed up two of my uploaded file names. It caught this by rendering the result and looking at it, then switched to the correct file.
2. **The color pour looked like an oil slick.** The first pour was busy, high-frequency marbling with harsh outlines, nothing like my ink washes. The fix was larger, slower-moving shapes and softer, fewer "tide line" edges, closer to how ink pools and dries.
3. **The vivid slider barely worked.** Chartreuse, orange, and pink almost never appeared, even at high settings, because of a threshold bug in how accent colors were mixed in. After the fix, the slider moves from mostly muted to strong color fields.
4. **Format issue with my photos.** Several of my iPhone photos were HEIC files, which the AI could not see until they were converted to JPG. GitHub also doesn't preview HEIC, so all the images here are converted.
5. **In my words:** any problems I ran into while using the tool or getting the AI to understand what I wanted.

## How it works (technical)

Everything is drawn on an HTML canvas with JavaScript:

- **The color pour** is generated from layered, "domain-warped" noise, a technique that bends a random pattern back into itself so it flows like liquid. The values are mapped onto my palette: mostly burgundy, mauve, dusty periwinkle, and deep green, with pockets of chartreuse, orange, pink, and clear periwinkle. Darker edges imitate watercolor tide lines. Each "New pour" uses a different random seed, recorded in the caption and the saved filename.
- **The film look** lowers saturation, lifts the blacks, warms the highlights, tints the shadows mauve, and adds a vignette, grain, and an orange-pink light leak.
- **The weave** draws all horizontal strips, then all vertical strips, then redraws each spot where a horizontal strip should pass over a vertical one. Soft shadows under each strip make it read as paper. Small random shifts in each strip's width and position imitate hand-cutting.
- **Patterns:** over-under (plain weave), diagonal (twill), and open rows (gaps like the lace rows in my indigo weaving). The "woven patch" layout weaves a section on top of the full image, like my strips on tree bark.

## Reflection

**In my words:** AI doesn't understand creativity, but it can mimic the data you give it. How much of the final piece feels like mine? What did the AI contribute, and what did only I bring?

## Next steps

- **In my words:** what I would change or add next.
