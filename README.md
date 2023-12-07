# MOKKA
Python runtime and workspace manager

## Requirements
- Python 3.12 or higher

## Installation on Linux
```
curl -sSL https://raw.githubusercontent.com/mokny/mokka/main/shared/install.sh | bash
```

## Using MOKKA

### Creating a workspace
Workspaces can contain multiple modules to keep things structured. You need at least one workspace.
```
mokka workspace create <NAME>
```

### Installing modules
Modules can be any Python script. The only requirement is a well formatted `mokka.toml` file in the root directory of the module. If you want to make use of MOKKAs internal inter process communication interface, import mokkalib in your python script. The library will be automatically copied while the module installation process. For more information see mokkalib.
```
mokka install <WORKSPACENAME> </PATH/TO/MODULE>
```

### Running modules
Modules run as subprocess in mokka. Each module can communicate with other modules that run in MOKKA (see mokkalib).
```
mokka run <WORKSPACENAME> <MODULEIDENT>
```

