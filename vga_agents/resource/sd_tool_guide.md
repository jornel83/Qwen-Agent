# SD Text-to-Image Tool

## SD Text-to-Image Tool Parameter Guide
When using the `flux_image_gen` tool, you can set the parameters as follows:

- `prompt`: Required. Describes the desired content of the generated image.
- `negative_prompt`: Optional. Describes content to avoid; defaults to an empty string.
- `width`: Optional. Width of the generated image (pixels), default is 512.
- `height`: Optional. Height of the generated image (pixels), default is 512.
- `steps`: Optional. Number of diffusion steps, default is 30.
- `guidance_scale`: Optional. Controls the consistency between the image and the text description, default is 3.5.
- `seed`: Optional. Random seed, -1 means random.

The large model should reasonably infer these parameter values based on user needs before calling this tool.

## Stable Diffusion 3.5: Open-Weight Text-to-Image Model

The SD Text-to-Image Tool is a text-to-image tool built on top of Stable Diffusion 3.5 Model.

### Overview
Stable Diffusion 3.5 (SD-3.5) is an upgraded Multimodal Diffusion Transformer that improves image quality, prompt comprehension and text rendering while keeping the community-friendly open-weights ethos of earlier SD releases. :contentReference[oaicite:1]{index=1}

### Key Features

#### High-Resolution, Single-Prompt Generation
* Produces images from **≈512 × 512 px up to ~1.4 K × 1.4 K (≈0.25–2 MP)** out of the box, with the *Large Turbo* variant finishing in just a few seconds. :contentReference[oaicite:2]{index=2}  
* Excels at complex compositions, long prompts and **clean typography**, outperforming SD 2.1 on small text and fine detail. :contentReference[oaicite:3]{index=3}  

#### Ready-to-Run Inference Options
| Environment | How to use |
|-------------|------------|
| **Python / Diffusers** | `StableDiffusion3Pipeline` loads `stabilityai/stable-diffusion-3.5-large` with a few lines of code. :contentReference[oaicite:4]{index=4} |
| **ComfyUI** | Community nodes and FP16 / FP8 checkpoints enable low-VRAM workflows. :contentReference[oaicite:5]{index=5} |
| **Cloud API / DreamStudio** | Official REST endpoints and DreamStudio web UI expose SD-3.5 without local setup. :contentReference[oaicite:6]{index=6} |

#### Lightweight Fine-Tuning & Extensions
* Built-in support for **LoRA, DoRA, IP-Adapter and new ControlNets** lets users inject fresh styles or structural guidance without full retraining. :contentReference[oaicite:7]{index=7}  
* Two weight tiers—**Large (≈8 B params)** and **Medium (≈2.5 B)**—let developers match model size to hardware. :contentReference[oaicite:8]{index=8}  

### Licence & Usage
SD-3.5 ships under the **Stability Community License (SCL)**: it is free for research, non-commercial use and commercial deployments under US $1 million annual revenue; higher-revenue products require a paid enterprise licence. :contentReference[oaicite:9]{index=9}  

### Typical Use Cases
1. **Concept art & storyboarding** – iterate visual ideas rapidly while keeping assets on-prem.  
2. **Social-media marketing** – batch-generate posts with accurate text layout, reducing manual retouching.  
3. **Custom LoRA packs** – create brand- or IP-specific style adapters atop the open weights.  


#### Tip
If GPU memory is tight, switch to the Medium weights or load an FP8 checkpoint in ComfyUI. Add keywords like “clean typography” for the sharpest text results.

