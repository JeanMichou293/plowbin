## plowbin

### Structure
`plowbin.py`: main script: compiles every source specified in `sources.json`, then call `instrument.sh`  
`instrument.sh`: passes resulting binaries to callgrind && cologrind

### Usage
`./plowbin.py`

### Source parameters
`compiler_args`: optional args (e.g. linker options)  
`compiler_cmd`: e.g. "gcc ..."  
`file_in`: path to source file, relative to dataset directory  
`file_out`: path to resulting file (binary). `{}` is replaced with the right path