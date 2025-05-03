# `new`

A CLI tool to create new projects or files from templates

`new` is a simple command-line interface utility for quickly generating new project folders or files from starter templates

---

## Features

- Create new projects using templates
```bash
new project python my-app
```
- Generate documents quickly
```bash
new doc meeting-notes
```
- Built-in and user-defined templates
- Placeholder replacement (e.g. `{{project_name}}`)
- Configurable and extensible structure

## Installation

Clone the repo and install as a local CLI tool (symlink or wrapper script)

```bash
git clone https://github.com/m4sc0/new.git
# optional: add `new` to your PATH
```

## Template Structure

Templates live in either the built-in `templates/` directory or your user folder at

```
~/.config/new/templates/
```

Example layout
```
templates/
├── project/
│   └── python/
│       ├── template.json
│       ├── main.py
│       └── README.md
└── doc/
    └── default/
        ├── template.json
        └── note.md
```

## Commands

### Create a new project

```bash
new project <type> <name>
```

Creates a new folder from the specified project type

### Create a new document

```bash
new doc <name>
```

Creates a single file using a template (e.g. a Markdown note)

## Template configuration

Each template folder contains a `template.json` file that defines how placeholders are handled and which files to include

Example `template.json`
```json
{
    "placeholders": ["project_name"],
}
```

# TODO / Coming Soon

- User-defined templates inf `~/.config/new`
- `new list` to show available templates
- Placeholder prompting (`{{author}}`, `{{year}}`)
- Git-based template cloning
- Configurable default values
