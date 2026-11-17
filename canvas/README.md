# Canvas homepage version

This folder holds the Canvas copy of the course homepage, like the one in the
Future Edge Networks course repository.

## Files

- `home.html`: the Canvas page body. It is built from `../index.html` with inline
  styles, no scripts, and absolute links to the GitHub Pages site, so lecture PDFs
  stay on GitHub and the Canvas links keep working.
- `build_home.py`: rebuilds `home.html` from `../index.html`. Run it from the repo
  root after editing `index.html`: `python canvas/build_home.py`.
- `push_to_canvas.ps1`: sends `home.html` to the Canvas course front page
  (course 380530, COP4610 Spring 2027, sections 0002/0007/0008). It needs a Canvas
  access token in `canvas/.canvas_token`, which git ignores.

When the schedule changes, edit `../index.html`, rebuild `home.html`, and push both.
