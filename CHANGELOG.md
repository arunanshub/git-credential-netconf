## 0.1.0 (2021-07-30)

### Feat

- **netconf**: check if `port` param is an integer and add it to `host`
- **cli**: add a quit flag to tell git not to consult any more helpers
- init

### Refactor

- **netconf**: use long flag names
- **cli**: force flush stdout buffer

### Fix

- **cli**: shift the args to root parser
- **cli**: add newline to stdout
- **proc**: prevent deadlock when using stdout=PIPE or stderr=PIPE