# Obliv

Obliv is a powerful and flexible CLI workflow automation tool designed for cybersecurity professionals, bug bounty hunters, pentesters, SOC analysts, and anyone who needs to automate complex security tasks. Obliv lets you orchestrate, chain, and automate your favorite tools and scripts, making repetitive and advanced operations easy, reproducible, and auditable.

## Features

- **Workflow Automation:** Build, run, and share complex workflows for reconnaissance, scanning, exploitation, reporting, and more.
- **Modular & Extensible:** Easily add new modules, tools, and integrations.
- **User-Friendly CLI:** Intuitive command-line interface with rich help and feedback.
- **Configuration Management:** Manage API keys, settings, and environment variables securely.
- **For Cybersec Pros:** Tailored for bug bounty, pentest, SOC, and blue/red team operations.
- **Cross-Platform:** Works on Linux, macOS, and Windows (with Python 3.8+).

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/BUZZ-zip/obliv-cli.git
cd obliv-cli
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Make the CLI Executable

```bash
chmod +x main.sh
```

Or run directly with Python:

```bash
python3 shell/main_shell.py
```

---

## Usage

### Running Obliv

```bash
./main.sh
# or
python3 shell/main_shell.py
```

### Available Commands

| Command                        | Description                                 |
|--------------------------------|---------------------------------------------|
| `help`                         | Show all available commands                 |
| `scan`                         | Perform a scan using configured tools       |
| `workflow run`                 | Run a specific workflow                     |
| `workflow list`                | List all available workflows                |
| `config set <key> <value>`     | Set a configuration value                   |
| `config get <key>`             | Get a configuration value                   |
| `auth <key>`                   | Authenticate with an API key                |
| `export`                       | Export a workflow as a binary               |
| `refresh`                      | Refresh the workflow list                   |
| `clear`                        | Clear the terminal screen                   |
| `exit`                         | Exit Obliv                                  |
| `update`                       | Update Obliv to the latest version          |

---

## Commands Examples

### 1. Scan

```bash
obliv scan --target example.com --tool nmap
```
_Expected output:_
```
[12:00:00] Starting scan on example.com with nmap...
[12:00:05] Scan complete. Results saved to results/example.com_nmap.txt
```

### 2. Run a Workflow

```bash
obliv workflow run -name recon-basic
```
_Expected output:_
```
[12:01:00] Running workflow: recon-basic
[12:01:01] Step 1: Subdomain enumeration...
[12:01:10] Step 2: Port scan...
[12:01:20] Workflow completed successfully.
```

### 3. List Workflows

```bash
obliv workflow list
```
_Expected output:_
```
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Index    ┃ Workflow Name        ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ 1        │ recon-basic          │
│ 2        │ full-audit           │
│ 3        │ web-app-test         │
└──────────┴──────────────────────┘
```

### 4. Configure Settings

```bash
obliv config set api_key sk-xxxxxx
obliv config get api_key
```

### 5. Help

```bash
obliv help
```

---

## Configuration

Obliv uses a configuration file to store API keys and settings.

### Example Configuration File (`~/.obliv/config.json`)

```json
{
  "api_key": "sk-xxxxxx",
  "username": "yourname",
  "default_workflow": "recon-basic"
}
```

You can also set environment variables for sensitive data:

```bash
export OBLIV_API_KEY=sk-xxxxxx
```

---

## Contributing

We welcome contributions from the community!

1. Fork the repository and create your branch:
   ```bash
   git checkout -b feature/your-feature
   ```
2. Commit your changes and push to your fork.
3. Open a pull request on GitHub.

**Coding Standards:**
- Write clear, concise code and comments.
- Follow PEP8 for Python code.
- Add tests for new features when possible.

**Pull Request Process:**
- Describe your changes clearly.
- Reference related issues if applicable.
- Ensure your branch is up to date with `main`.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Screenshots

![Obliv CLI Screenshot](docs/screenshot.png)

---

## Tips & Best Practices

- Use descriptive workflow names for easy management.
- Store sensitive keys in environment variables or config files with proper permissions.
- Regularly update Obliv with the `update` command to get the latest features and fixes.
- Use `obliv help` or `obliv <command> --help` for detailed usage.

---

**Obliv** – Automate, orchestrate, and accelerate your cybersecurity workflows from the command line!
