# linker.md

an incredibly basic recursive linker for markdown files (or anything else)


#### Usage:

Either

**1.** run `./linker.py [SOURCE] [DEST]` or `./linker.py [SOURCE]` (which will print results to stdout), or

**2.** use it through python (or whatever you want to FFI that to)
> ```python
> from linker import link
> open('dest.md', 'w').writelines(link('src.md')) 
> ```

Files referenced with `!require(relative/path/to/file)` will be inserted. `!req()` and `!r()` also should do the trick, or you can specify your own syntax with a regex pattern.
