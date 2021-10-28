# lotusops
A DevOps tool for lotus
### install
```
pip install -U lotusops
```
### usages
```
lotusops [subcommand] [keyword]
```
subcommand|expl|format|example
-----|----------|------|------
ab|abort all jobs<br> with a certain keyword|```lotusops ab [sector-state]```|```lotusops rmall PreCommit1```
rm|remove all sectors<br> in a certain state|```lotusops rm [sector-state]```|```lotusops rmall PreCommit1```
pb|continous pledge<br> in a certain interval|

