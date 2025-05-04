# `new`

A CLI tool to create new projects or files from versioned template images.

`new` is a fast and minimal command-line utility for generating new project structures using local or remote templates. It uses a Docker-style image syntax (like `project/python:3.10`) and supports placeholder replacement, user prompts, and `$EDITOR` integration.

## 🚀 Features

- Create new projects using versioned **template images**
- Build custom templates from local folders (`new build`)
- Upload local templates to a remote registry (`new push`)
- Browse and download remote templates (`new list remote`, `new pull`)
- Placeholder-based generation with intelligent defaults
- Secure upload via token prompt
- Cache-based architecture (`~/.cache/new/templates`)
- `$EDITOR` support to open main file after creation (optional)

## 📦 Installation

Clone the repository and use via symlink or wrapper script:

```bash
git clone https://github.com/m4sc0/new.git
cd new
chmod +x run  # optional helper script
````

Add to your PATH or create a wrapper:

```bash
#!/bin/bash
python3 /path/to/new/main.py "$@"
```

## 🧱 Template Image Structure

Templates are stored under:

```
~/.cache/new/templates/<category>/<name>/<version>/
```

Example:

```
~/.cache/new/templates/
└── project/
    └── python/
        └── 3.10/
            ├── template.json
            ├── main.py
            └── README.md
```

Each template must include a `template.json` file:

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

This uses the cached template to generate `./my-app` with placeholder replacements.

### 🔍 List available templates

#### Local

```bash
new list local
```

#### Remote

```bash
new list remote
```

### 📥 Pull a remote template

```bash
new pull project/python:3.10
```

Downloads and caches a template from the configured remote registry.

### ⬆️ Push a template (with token)

```bash
new push project/python:3.10
```

Pushes the cached template to the remote.
🔐 Requires token input when prompted.

### 🧱 Build a template from a folder

```bash
new build project/python:3.10 ./path-to-template
```

Options:

* `-f`, `--force` – Overwrite if it already exists
* `-v`, `--verbose` – Show detailed output
* `--dry-run` – Simulate without writing

## 🔁 Placeholder System

The renderer replaces all `{{...}}` placeholders in files and filenames.

### Auto-filled placeholders:

* `project_name`, `template_name`, `project_title`
* `timestamp`, `date`, `year`, `month`, `day`, `weekday`, `time`
* `user`, `hostname`, `os`, `uuid`

Missing placeholders will trigger interactive prompts.

## 🔐 Remote Upload Security

All remote uploads are protected by a token:

* On `new push`, you'll be prompted for an upload token
* Token is passed as a `Bearer` header for secure authentication
* Server-side logic determines access

## 🧪 Planned Features

* JSON Schema validation for `template.json`
* `.newignore` for excluding files during build
* Shared template registry with ratings/search
* Auto-tagging of templates via metadata

## 📡 Related Projects

`new-remote` - A FastAPI-absed server to host and distribute versioned templates used by `new` via `new pull`, `new push` and `new list remote`.

## ❤️ Contributing

Ideas, issues, and PRs are welcome.
This tool is built for power users but designed to stay minimal.

## 📄 License

MIT

