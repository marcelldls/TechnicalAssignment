# Technical assignment

A python command line tool that takes architecture (amd64, arm64, etc.) as an argument and outputs the statistics of the top 10 packages (from Debian mirror: http://ftp.uk.debian.org/debian/dists/stable/main/) that have the most files associated with them.

## Example of usage:

Installation:
```
pip install git+https://github.com/262882/myTechnicalAssignment
```

Running:
```
package_statistics <architecture>
```

Returns:
```
<package name 1>         <number of files>
<package name 2>         <number of files>
......
<package name 10>         <number of files>
```

## Development

Installation:
```
pip install -e .[dev]
```

Running tests:
```
tox
```

## Assignment requests:
- Work in a local Git repository
- Submit a tar.gz of the repo
- Time spent on the exercise (sum hours in commit messages)
