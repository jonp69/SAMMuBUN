# Context — Video Meme Compositor (finalized)
this is  aprogram wich expands uppon 
https://github.com/yangchris11/samurai
to segment a video into masks to add on top of a background frame photo or video
the program relies on the SAMJurai folders plus "ingest", "egest" video folders 
"ingest", "egest" video folders have sub sub folders for foreground and background
the foregrpound video is ingested and passed to SAmurai (possibly using ffmpeg.exe in the "BIN" folder)
the video is then kept and converted into a gif using ffmpeg.exe (from BIN folder)



This file captures the final, actionable context for the local agent/desktop pipeline. It reflects the decisions you made interactively:
- only the DVD top/bottom bands are upscaled (center region preserved);
- AI generation/inpainting runs exactly once on a single background frame (the one used for wizard overlay);
- center‑pixel DATA mapping is authoritative (not merely center coordinates);
- masks drive all operations and foreground/face pixels are never generatively replaced.

---

## Inputs
- Widescreen source (high-detail; sample 3840×1610 in tests)
- DVD source (720×540) — contains extra vertical detail above and below widescreen crop
- Aligned 4:3 source (if available; used for cross-checks)
- Single external reference frame (used once to set start time / center)
- Face insertion asset: `El_xox_sillyface.jpg`

---

## High-level rules (short)
- Downscale + aggressive crop is used only for matching/synchronization.
- For final compositing use full‑resolution originals; do not discard real pixels.
- Map center pixel DATA (the actual sample) from each source to the canonical output center pixel exactly — prefer integer scale factors so mapping is exact.
- DVD generative replacement of the wizard/face is forbidden. Allowed operations on subject: restoration/upscale, recolor (masked), masked effects, tracked compositing.
- AI inpainting/generation is permitted only once, on a single background frame, and only on areas explicitly outside Foreground/Face masks.

---

## Final pipeline (concise, ordered)

1. Pre‑match (sync-only)
   - Temporarily downscale/crop the widescreen and DVD to intersection region for matching only; use the single external reference frame once to set start.

2. Frame matching loop
   - Match frames A↔B across the requested duration using the temporary copies; stop when either stream ends.

3. Determine DVD band geometry (representative frame)
   - Compute the DVD top/bottom bands that extend beyond the widescreen crop; use the manual visual sample mapping (960×540 center sample → band upscale factor 4×).

4. Per matched pair (use full‑res originals)
   - Map center pixel DATA to canonical output center exactly; extract DVD center/core, top band, bottom band; upscale only the bands (4×) and composite real pixels with priority to widescreen samples.

5. Masks & segmentation (per shot)
   - Run segmentation once for the shot (Background, Foreground, Face), refine and feather 8–20 px, save and reuse; propagate masks per-frame via optical flow/XMem/Samurai.

6. Background: single generation pass
   - Select the single background key frame; build inpaint_mask = (missing/padding/corners) ∧ Background_mask (exclude Foreground/Face); run AI inpainting once and save generated_background_key.

7. Foreground per frame
   - Propagate masks to each frame; recolor (wizard → pink) via mask preserving luminance; apply masked CA/restorations; punch/restore face per-frame.

8. Face insertion per frame
   - Track face transform and stitch `El_xox_sillyface.jpg` into the punched hole (alpha blend, feather, color match).

9. Final composite per frame
   - Composite order: generated_background_key → recolored foreground (with upscaled bands) → face insertion → unify; export MP4 + GIF, keep intermediates.

---

## Zero‑shot outpaint (short paragraph — added)
When you only have a single widescreen keyframe and lack a 4:3 source, perform zero‑shot outpainting of the top/bottom bands as follows: protect the subject by producing authoritative masks with SAM (foreground and face submask) and feather them; expand the canvas vertically and build an inpaint mask that is the union of the new canvas areas and any padding/black regions, ANDed with the background mask (explicitly exclude all foreground/face pixels). First attempt non‑ML exemplar/patch synthesis (PatchMatch) to extend foliage and film grain; if that fails or looks inconsistent, run a single controlled diffusion outpaint (Stable Diffusion img2img/inpaint) on that inpaint mask with low denoising and strong border conditioning (ControlNet edges/depth if available), then seam‑blend and color‑match. Save that one generated background and reuse it for all frames — do not let the outpaint change any protected subject pixels.

---

## One‑line checklist for the agent (exact parameters and steps)
- Generate masks: SAM → save `mask_foreground.png` and `mask_face.png`, create feathered versions (8–20px).
- Expand canvas: output_w = chosen width (e.g., 3840), output_h = chosen height; place original so its source_center maps to canonical_center (Ox,Oy) exactly.
- Inpaint mask: inpaint_mask = ((canvas_area_not_covered_by_original) OR black_pixels) ∧ mask_background; ensure mask_foreground and mask_face are zero inside mask.
- Try PatchMatch outpainting: run exemplar fill on inpaint_mask; if pass (visual continuity OK) → save `generated_background_key.png` and STOP.
- Else run SD outpaint once with params: init_img=expanded_canvas, mask=inpaint_mask, prompt="photorealistic green foliage, dappled sunlight, film grain, match lighting and color of the source", negative_prompt="person, face, clothing, hat", sampler=Euler_a (or DDIM), steps=20–30, guidance=7.0–8.5, denoise=0.20–0.35, seed=fixed_or_random; if ControlNet available, add edge/depth conditioning of the original borders.
- Postprocess: feather mask edges 8–20px, Poisson blend seams, histogram color match of generated regions to adjacent original pixels; assert that generated_background_key pixel values under mask_foreground are unchanged (diff must be empty).
- Save outputs: `generated_background_key.png`, masks (binary+feathered), debug overlay diff images.

---

## Practical tips & model choices (very short)
- Try OpenCV PatchMatch / LaMa inpainting first (fast, non‑generative).
- If SD outpaint used: use low denoise, constrained prompt, ControlNet for structure if available.
- For mask propagation use XMem or Samurai (SAM + propagation wrappers) — one‑shot mask propagation from keyframe works well.
- Tile upscaling for 4× bands to avoid OOM: overlap tiles and stitch, then blend overlaps.

---

## Validation & automated checks (minimal)
- Assert: `generated_background_key` has no pixels modified under `mask_foreground` (pixelwise check).
- Visual seam check: max delta near seam ≤ small threshold (tunable).
- Save debug overlays and an align_report for future debugging.

---

## What changed and why (one line)
- Added a concise zero‑shot outpaint recipe and a one‑line agent checklist so your local agent/copilot can run a single controlled outpaint on the top/bottom bands using one keyframe while strictly protecting the wizard/face pixels.

--- 

Keep this file next to your code so the local agent reads it as authoritative context before generating module code. If you want, I can also add a tiny "agent invocation example" line (one short command template) to the bottom — say so and I will append it.