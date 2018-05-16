## plowbin

### Structure
`plowbin.py`: main script: compiles every source specified in `sources.json`, then call `instrument.sh`

`instrument.sh`: passes resulting binaries to callgrind && cologrind

### Usage
`./plowbin.py`