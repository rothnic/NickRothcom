NickRoth.com
-----------------------
This is the source of my website
It is a fork of [Pythonic Perambulations](http://jakevdp.github.io)
blog. It is built using the [Pelican](http://blog.getpelican.com/)
blogging platform.

Requirements
------------

- Recent version of [IPython](http://github.com/ipython/ipython).  The
  liquid_tags plugin above requires IPython 1.0.  Note that previously
  this could be built with the stand-alone nbconvert package.  That
  no longer works with the recent liquid_tags plugin.

- Recent version of [Pelican](http://github.com/getpelican/pelican).  For
  the static paths (downloads, images, figures, etc.) to appear in the right
  place, Pelican 3.3+ must be used.

Instructions
---
Uses fabric to automate build and updates, since it is cross platform.

### Commands

List all commands: `fab -l`

```
build       Build local version of site
clean       Remove generated files
develop     Runs `serve` and `regenerate` in parallel.
gh_pages    Publish to GitHub Pages
preview     Build production version of site
rebuild     `clean` then `build`
regenerate  Automatically regenerate site upon file modification
reserve     `build`, then `serve`
serve       Serve site at http://localhost:8000/
```

Any of the above can be called from the project folder with `fab {command}`. The most useful command will be `fab develop`.

### Development

The fabric command, `fab develop` uses fabuild to run both the serve and regenerate tasks as separate threads. The same thing can be accomplished by running each separately, but you have to do so in individual consoles.

The requirements to use the fabric automation is:
- Fabric
- Fabuild
