# ManimGL Animations for ML Concepts

This repository contains ManimGL animations exploring various machine learning concepts. These animations are based on the excellent work by Grant Sanderson (3Blue1Brown) and have been modified for specific ML concept demonstrations.

## Credit
This project uses ManimGL, created by Grant Sanderson (3Blue1Brown). The original ManimGL library and many of the base animation concepts can be found at:
- [3Blue1Brown's YouTube Channel](https://www.youtube.com/c/3blue1brown)
- [ManimGL GitHub Repository](https://github.com/3b1b/manim)

## Installation

1. First, ensure you have Python 3.8 or higher installed.

2. Install system dependencies (varies by operating system):

   ### For Ubuntu/Debian:
   ```bash
   sudo apt update
   sudo apt install libcairo2-dev ffmpeg \
       libpango1.0-dev python3-dev \
       python3-pip pkg-config
   ```

   ### For MacOS:
   ```bash
   brew install cairo ffmpeg pkg-config pango
   ```

   ### For Windows:
   - Install [Cairo](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycairo)
   - Install [FFmpeg](https://ffmpeg.org/download.html)
   - Add FFmpeg to your system PATH

3. Install ManimGL:
   ```bash
   pip install manimgl
   ```

## Scenes Overview

The repository contains several files with different animations:

### attention.py
```bash
manimgl attention.py -pl       # List all scenes
manimgl attention.py [SceneName]  # Render specific scene
```

### auto_regression.py
```bash
manimgl auto_regression.py -pl
manimgl auto_regression.py [SceneName]
```

### embedding.py
```bash
manimgl embedding.py -pl
manimgl embedding.py [SceneName]
```

### generation.py
```bash
manimgl generation.py -pl
manimgl generation.py [SceneName]
```

### ml_basics.py
```bash
manimgl ml_basics.py -pl
manimgl ml_basics.py [SceneName]
```

### network_flow.py
```bash
manimgl network_flow.py -pl
manimgl network_flow.py [SceneName]
```

### supplements.py
```bash
manimgl supplements.py -pl
manimgl supplements.py [SceneName]
```

## Common ManimGL Commands

- List all scenes in a file:
  ```bash
  manimgl file.py -pl
  ```

- Render a specific scene:
  ```bash
  manimgl file.py SceneName
  ```

- Render in high quality:
  ```bash
  manimgl file.py SceneName -hq
  ```

- Save the animation (without previewing):
  ```bash
  manimgl file.py SceneName -w
  ```

- Preview without saving:
  ```bash
  manimgl file.py SceneName -p
  ```

## Output Location

By default, rendered videos will be saved in the `media/videos/` directory within your project folder.

## Common Issues and Solutions

1. **Cairo Import Error**:
   - Windows: Install the appropriate wheel file from the provided Cairo link
   - Linux: Ensure all system dependencies are installed
   - MacOS: Make sure Cairo is properly installed via Homebrew

2. **FFmpeg Not Found**:
   - Ensure FFmpeg is properly installed and added to your system PATH

3. **Performance Issues**:
   - Try reducing the quality using `-l` flag instead of `-hq`
   - Close other resource-intensive applications
   - Consider rendering without preview using the `-w` flag

## Dependencies

- Python 3.8+
- ManimGL
- Cairo
- FFmpeg
- PyOpenGL
- NumPy
- Pango

## Contributing

Feel free to contribute by:
1. Forking the repository
2. Creating your feature branch
3. Committing your changes
4. Pushing to the branch
5. Creating a Pull Request

## License

This project is licensed under the same terms as ManimGL and videos . Please see the original [3Blue1Brown/manim repository](https://github.com/3b1b/manim) for more details.

---

Remember to check out 3Blue1Brown's [YouTube channel](https://www.youtube.com/c/3blue1brown) for excellent mathematical animations and explanations that inspired this project.