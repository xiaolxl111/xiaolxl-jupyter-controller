# Xiaolxl-Jupyter-Controller

This repository provides utilities for controlling several Stable Diffusion
related projects. Originally the interface was built for Jupyter notebooks
using `ipywidgets`. The code base has been refactored to include a Gradio
frontend so the controller can be accessed from a browser without relying on a
Jupyter environment.

## Running the Gradio interface

```bash
python gradio_launcher.py
```

This will launch a Gradio app with a simple downloader and shell interface. It
uses the existing controller utilities under `xiaolxl_jupyter_controller` to
execute commands.
