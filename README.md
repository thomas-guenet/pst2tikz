pst2Tickz
=========
**pst2Tikz** is a Python program created to help transform **inkscape** figures to **tikz** format way of writing, and be included in a Latex document.
Its purpose is to create a base tikz coding of the figure, some editing will be necessary for line style, and text.

Usage:
------
Create or import your figure in Inkscape.
Best practice is to clear any text and add it afterwards with tikzpicture commands. 
It is also preferable to get rid of arrows or style of the line, and redefining them afterwards.
1. In Inkscape save figure as a LaTeX with PSTricks macros (*tex)

Run **pst2tex** on the previously created file. Define a scale to adapt the size of the figure to your document; it is also possible to define the format of numbers that will be written in the output file.
2. python pst2tex -i filename.tex -o output.tex --scale=65 --formatOfNumbers=%.3f

Compile the result to see the result.
3. pdflatex output.tex

If the size of the figure is not adapted to your document, it is possible to change the `scale` value (see step 2.).
Finally, it may be necessary to edit the output file by redefining the style of lines using the brackets after the command (`draw`, `fill`, and `filldraw`):
- `thin`,
- `thick`,
- `very thick`,
- `ultra thick`
- `dotted`,
- `dashed`,
- `dashdotted`,
or their shape:
- `>=stealth,<-`
- `>=latex,->`
- `<->`
- `smooth`
To add text, use `node []{text};` command after the point coordinates (`\draw` command).
Example:
```
\draw (0,0) -- (1.8,2.0) node [right]{$\sigma_r$};
```
