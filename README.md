# Helper Scripts for COMP3012 Course

## [todo.py](./todo.py)
### Description
Searches for all `@todo` and `TODO` comments in the `.` and `src` directories and displays them along with vscode clickable links to file and line number.

*__Note:__* Place into root of Lab/Assignment to run.

### Usage
```bash
py todo.py
```
![](./imgs/todo.png)

## [mongodb-service.py](./mongodb-service.py)
### Description
Setup and run `mongod` as a service on windows (does not install `mongod` just handles the service).

*__Note:__* Requires admin permission, will attempt to elevate if not launched with insignificant permissions.

### Usage
```
mongodb-service.py

SERVICE_NAME:   MongoDB
DB_PATH:        C:\mongodb\db
LOG_PATH:       C:\mongodb\log.txt

usage: mongodb-service.py [-h] (--install | --remove | --start | --stop)

optional arguments:
  -h, --help  show this help message and exit

Action:
  --install   install a service for MongoDB
  --remove    remove MongoDB service
  --start     start MongoDB service
  --stop      stop MongoDB service

```

## [set-npm-shell.py](./set-npm-shell.py)
###  Description
On Windows `npm` uses `cmd` as its default shell, this can cause issues (particularly with environment variables) due to how things are often handled directly between `cmd` and `sh`/`bash`/`zsh` (the usual for non Windows systems). This script will attempt to locate `sh.exe` (with `pwsh.exe` and `powershell.exe` as backups) and use it to set `node`'s `script-shell` option.

*__Warning:__* Setting a different `script-shell` can cause it's own problems so only use if you are sure you need it.

### Usage
```bash
py set-npm-shell.py
```