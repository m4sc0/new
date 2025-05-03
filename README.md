# `new`

A CLI tool to create new projects or files from versioned template images.

`new` is a fast and minimal command-line tool for generating new projects or files using local or remote templates. It uses a Docker-style image system (e.g. `project/python:3.10`) and supports dynamic placeholders.



## 🚀 Features

- Create new projects from versioned template **images**
- Fully supports **local template cache**
- Placeholder replacement with system metadata and user prompts
- `$EDITOR` integration to open files automatically after creation
- Future-ready for **remote registry support**, **template builds**, and **pulling**



## 📦 Installation

Clone the repository and run using a wrapper script or install via symlink:

```bash
git clone https://github.com/m4sc0/new.git
cd new
python -m main.py create project/python:3.10 my-app
```

You can also use a wrapper script to add this to your `$PATH`

```bash
#!/bin/bash

python3 -m /path/to/repo/main.py $@
```

The feature of a complete cli to download will come in the future

## 🧱 Template Structure

Templates are cached locally under:

```
~/.cache/new/templates/
```

Example structure:
```
~/.cache/new/templates/
└── project/
    └── python/
        └── 3.10/
            ├── template.json
            ├── main.py
            └── README.md
```

Each template must include a `template.json` file with metadata.

Example `template.json`:
```json
{
  "name": "Python CLI App",
  "category": "project",
  "version": "3.10",
  "placeholders": ["project_name"],
  "open": "main.py"
}
```



## 📚 Usage

### Create a project from an image

```bash
new create project/python:3.10 my-app
```

This renders the template into `./my-app`, replacing placeholders and optionally opening the main file in `$EDITOR`.



### List local templates

```bash
new list local
```

Output:
```
Available local templates:
 - project/python:3.10
 - doc/markdown:latest
```



## 🔁 Placeholder System

Placeholders like `{{project_name}}`, `{{user}}`, `{{date}}`, etc., are automatically replaced.

Default values include:
- `project_name`, `template_name`, `project_title`
- `timestamp`, `year`, `month`, `day`, `weekday`, `time`
- `user`, `hostname`, `uuid`, `os`

Any undefined placeholders will be prompted for interactively.



## 🛠 Planned Features

- `new pull <image>` to fetch templates from a remote registry
- `new build` to create and version templates from local folders
- `new list remote` to query hosted registries
- JSON schema validation for `template.json`
- Global config overrides



## ❤️ Contributing

PRs, template contributions, and ideas are welcome.



## 📄 License

MIT

