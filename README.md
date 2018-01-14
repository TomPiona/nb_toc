nb_toc
=============

## Usage

```python
from nb_toc import generate
generate('my_notebook.ipynb')
```

-------------

## Optional Parameters

Argument | Default Value | Role
--- | --- | ---
`title` | 'Table of Contents' | header for TOC cell
`additional_text` | None | text to go in TOC cell
indent_size | 4 | amount of indentation for TOC
ignore_level | 0 | Ignores headers up to this size