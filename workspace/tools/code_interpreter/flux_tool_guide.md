# Flux Text-to-Image Tool

## Flux Text-to-Image Tool Parameter Guide
When using the `flux_image_gen` tool, you can set the parameters as follows:

- `prompt`: Required. Describes the desired content of the generated image.
- `negative_prompt`: Optional. Describes content to avoid; defaults to an empty string.
- `width`: Required. The width of the generated image in pixels. Must be set to 1920.
- `height`: Required. Height of the generated image in pixels.Must be set to 1080.
- `steps`: Optional. Number of diffusion steps, default is 30.
- `guidance_scale`: Optional. Controls the consistency between the image and the text description, default is 3.5.
- `seed`: Optional. Random seed, -1 means random.

The large model should reasonably infer these parameter values based on user needs before calling this tool.

## Flux Dev: Open-Weight Text-to-Image Model

The Flux Text-to-Image Tool is a text-to-image tool built on top of Flux Dev Model.

### Overview
Flux Dev (formally **FLUX 1 dev**) is a 12-billion-parameter text-to-image model released by **Black Forest Labs**.  
It offers near-flagship image quality, ships with full FP16 weights (~23 GB), and
is distributed under a research-friendly non-commercial licence that still
allows fine-tuning and private deployment.

### Key Features

#### High-Resolution Single-Prompt Generation
* Generates images up to **1024 × 1024 px** natively, with community workflows
  reaching 2 K while retaining texture and composition fidelity.
* Delivers strong prompt adherence across diverse scenes and styles.

#### Ready-to-Run Inference Options
| Environment          | How to use                                               |
|----------------------|----------------------------------------------------------|
| **Python / Diffusers** | `FluxPipeline` loads weights in a few lines of code.   |
| **ComfyUI**          | Node workflow + FP8 / FP16 checkpoints for low-VRAM rigs |
| **Hosted APIs**      | Instant REST / streaming endpoints on Fal.ai & Replicate |

#### Lightweight Fine-Tuning & Extensions
Fully compatible with **LoRA** and adapter training, so you can inject new
styles, characters, or product imagery without retraining the full network.

### Licence & Usage
* **Flux Dev Non-Commercial Licence** – free for personal, academic and other
  non-profit projects.  
* Any commercial use of the model or derivative checkpoints requires a paid,
  separate agreement with Black Forest Labs.

### Typical Use Cases
1. **Concept design & prototyping** – offline generation keeps unreleased IP secure.  
2. **Educational / media demos** – create illustrative visuals for talks, courses or blogs.  
3. **Custom LoRA creation** – build brand-specific or stylistic add-ons atop the open weights.  

### Tip
Flux Dev generally performs well without negative prompts; if VRAM is limited, load the FP8 checkpoint or enable CPU off-loading as described in the model card.

