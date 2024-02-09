# Technical assignment

A python command line tool that takes architecture (amd64, arm64, etc.) as an argument and outputs the statistics of the top 10 packages from a Debian mirror that have the most files associated with them.

## Example of usage:

Installation:
```
pip install git+https://github.com/262882/myTechnicalAssignment
```

Running:
```
package_statistics list <architecture>
```

Returns:
```
Processing package statistics for 'amd64' from http://ftp.uk.debian.org/debian/dists/stable/main/
The top 10 packages with the highest file counts are:
1.piglit                           53007
2.esys-particle                    18408
3.acl2-books                       16907
4.libboost1.81-dev                 15456
5.racket                           9599
6.zoneminder                       8161
7.horizon-eda                      8130
8.libtorch-dev                     8089
9.liboce-modeling-dev              7458
10.linux-headers-6.1.0-15-amd64    6499
```

Using alternative mirrors:
```
package_statistics --debian_mirror http://ftp.am.debian.org/debian/dists/bullseye/main/ list amd64
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
