# `new`

A CLI tool to create new projects or files from versioned template images.

`new` is a fast and minimal command-line utility for generating new project structures using local templates. It uses a Docker-style image syntax (like `project/python:3.10`) and supports dynamic placeholder replacement, user prompts, and `$EDITOR` integration.

## 🚀 Features

- Create new projects using versioned **template images**
- Supports building local templates with `new build`
- Intelligent **placeholder replacement** from context (like timestamp, user, etc.)
- Auto-opens generated files in `$EDITOR` (optional)
- Clean, cache-based template system (`~/.cache/new/images`)
- Future-proofed for remote registries (e.g. `new pull`, `new list remote`)

## 📦 Installation

Clone the repository and run via symlink or wrapper script:

```bash
git clone https://github.com/m4sc0/new.git
cd new
chmod +x run  # optional helper script
````

Add to your PATH or use a wrapper like:

```bash
#!/bin/bash
python3 /path/to/new/main.py "$@"
```

## 🧱 Template Image Structure

Templates are versioned and stored under:

```
~/.cache/new/templates/<category>/<name>/<version>/
```

Example:

```
~/.cache/new/images/
└── project/
    └── python/
        └── 3.10/
            ├── template.json
            ├── main.py
            └── README.md
```

Each template must contain a `template.json` file with metadata.

Example:

```json
{
  "description": "Starter project for building a Python CLI",
  "placeholders": ["project_name"],
  "open": "main.py"
}
```

## 📚 Usage

### 🛠 Create a project

```bash
new create project/python:3.10 my-app
```

Generates `./my-app` from the specified image and replaces all placeholders.

### 🔍 List available templates

```bash
new list local
```

Output:

```
Available local templates:
 - project/python:3.10
 - doc/markdown:latest
```

### 🧱 Build a template from a local folder

```bash
new build project/python:3.10 ./path-to-template
```

Options:

* `-f`, `--force` – Overwrite if template already exists
* `-v`, `--verbose` – Print details
* `--dry-run` – Show what would happen

## 🔁 Placeholder System

The template renderer replaces all `{{...}}` placeholders in files and filenames.

### Auto-filled placeholders:

* `project_name`, `template_name`, `project_title`
* `timestamp`, `date`, `year`, `month`, `day`, `weekday`, `time`
* `user`, `hostname`, `os`, `uuid`

Any missing placeholder will prompt for input during creation.

## 🧪 Planned Features

* `new pull` for downloading templates from remote registries
* `new list remote` to browse available online templates
* JSON Schema validation for `template.json`
* `.newignore` support for excluding files from build
* Centralized template discovery via web registry

## ❤️ Contributing

PRs, ideas, and new templates are very welcome. This project is minimal by design but structured for power users.

## 📄 License

MIT
