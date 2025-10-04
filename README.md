# Obliv CLI

Obliv is a powerful workflow automation tool designed for cybersecurity professionals, penetration testers, and SOC analysts. It provides a command-line interface to create, manage, and execute automated workflows for various security tasks.

## Features

- **Interactive Shell**: User-friendly command-line interface with color coding
- **Workflow Management**: Create, run, and export custom workflows
- **Authentication System**: Secure API key-based authentication
- **Real-time Dashboard**: Monitor workflow execution and client information
- **Auto-Update System**: Built-in version checking and update mechanism

## Installation

1. Clone the repository:
```bash
git clone https://github.com/BUZZ-zip/obliv-cli.git
cd obliv-cli
```

2. Create config directory:
```bash
mkdir -p ~/.obliv
```

3. Run the main script:
```bash
./main.sh
```

## Usage

### Available Commands

- **help**: Display list of available commands
```bash
help
```

- **auth**: Authenticate with your API key
```bash
auth <your-api-key>
```

- **showall**: Display all available workflows
```bash
showall
```

- **run**: Execute a workflow
```bash
run -name <workflow_name> [params...]
run -uid <workflow_uid> [params...]
run -number <workflow_number> [params...]
```

- **export**: Export a workflow to a binary
```bash
export -name <workflow_name> -binary_name <output_name>
```

- **refresh**: Refresh the workflow list
```bash
refresh
```

- **clear**: Clear the terminal screen
```bash
clear
```

- **update**: Update the client to the latest version
```bash
update
```

- **exit**: Quit the application and close tmux session
```bash
exit
```

### Dashboard Features

The dashboard displays:
- Client information (username, API key status)
- Number of available workflows
- Client version
- Real-time workflow execution status

## Configuration

### API Key Setup

1. Store your API key in `~/.obliv/config.json`:
```json
{
    "api_key": "your-api-key",
    "username": "your-username"
}
```

### Version Management

The client version is stored in the `VERSION` file at the root of the project. The client automatically checks for updates on startup and notifies you when a new version is available.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Use Python 3.x
- Follow PEP 8 style guide
- Add appropriate error handling
- Test your changes thoroughly

## License

This project is licensed under the MIT License - see the LICENSE file for details.
