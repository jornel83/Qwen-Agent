# Flux Text-to-Image Tool

## Flux Text-to-Image Guide
When using the flux_image_gen tool, you need to understand the basic concepts related to this tool.

### What is "Prompt"?
A required field that describes the desired content of the generated image. It serves as the core instruction for what the model should create.

### What is "Negative Prompt"?
An optional field that describes content you want to avoid in the generated image. If not specified, it defaults to an empty string, meaning no exclusions are applied.

### What is "Steps"?
An optional setting that defines the number of diffusion steps used in image generation. More steps typically lead to higher quality and more refined outputs, at the cost of longer generation time.

### What is "Guidance Scale"?
An optional parameter that controls how strongly the model should follow the prompt. Higher values mean stricter adherence to the text description, while lower values allow more creative freedom.

### What is "Seed"?
An optional parameter that sets the random seed for generation. A value of -1 means the seed is random, producing different results each time. A fixed seed ensures reproducibility of the same output.

## Flux Dev: Open-Weight Text-to-Image Model

The Flux Text-to-Image Tool is a text-to-image tool built on top of Flux Dev Model.

### Overview
Flux Dev (formally **FLUX 1 dev**) is a 12-billion-parameter text-to-image model released by **Black Forest Labs**.  
It offers near-flagship image quality, ships with full FP16 weights (~23 GB), and
is distributed under a research-friendly non-commercial licence that still
allows fine-tuning and private deployment.

### Key Features

#### High-Resolution Single-Prompt Generation
* Generates images up to **2048 × 2048 px** natively, with community workflows
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