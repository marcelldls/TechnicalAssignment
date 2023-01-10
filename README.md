# Technical assignment: Python Software Engineer - Ubuntu Hardware Certification Team

A python command line tool that takes architecture (amd64, arm64, etc.) as an argument and outputs the statistics of the top 10 packages (from Debian mirror: http://ftp.uk.debian.org/debian/dists/stable/main/) that have the most files associated with them.

## Example of usage:

Running:
```
./package_statistics.py amd64
```

Returns:
```
<package name 1>         <number of files>
<package name 2>         <number of files>
......
<package name 10>         <number of files>
```

## Assignment requests:
- Work in a local Git repository
- Submit a tar.gz of the repo
- Time spent on the exercise (sum hours in commit messages)

## High level solution

Could use the following process with top bullet as a testable unit
- Recognise desired architecture
- Aquire data
  - Connect to mirror						 
  - Download compressed Contents file                    
  - Decompress file  						
- Process data
  - Read file
  - Parse file into list (see proposal)
  - sort list (see proposal)
  - clean up 
- Return results

#### File parsing proposal:

Example of file content:
```
usr/share/latex-cjk-common/utils/subfonts/clonevf.pl    tex/latex-cjk-common
usr/share/latex-cjk-common/utils/subfonts/hlatex2agl.pl tex/latex-cjk-common
usr/share/latex-cjk-common/utils/subfonts/makefdx.pl    tex/latex-cjk-common
usr/share/latex-cjk-common/utils/subfonts/sfd2uni.pl    tex/latex-cjk-common
usr/share/latex-cjk-common/utils/subfonts/subfonts.pe   tex/latex-cjk-common
usr/share/latex-cjk-common/utils/subfonts/uni2sfd.pl    tex/latex-cjk-common
usr/share/latex-cjk-common/utils/subfonts/vertical.pe   tex/latex-cjk-common
usr/share/latex-cjk-common/utils/subfonts/vertref.pe    tex/latex-cjk-common
```

While new line available:
- Read line
- To get package name: Reading from right to left, drop everything from (including) first "/" 
- Append name to "raw_names" list.

#### Sorting proposal
Capture data into two (built in) lists:
- package_names list = unique entries ("A repository must not include different packages (different content) with the same package name, version, and architecture" - https://wiki.debian.org/RepositoryFormat#A.22Contents.22_indices)
- file_count list = Each file has new line therefore sum name occurances to determine number of files

Compute rank of file_count entries numerically, use to sort both file_count and package_names lists respectively 

## Assumptions (Considering context of the role applied to):
- Tool to be used on an Ubuntu machine (Use only python standard libarary to avoid adding dependancies, no pip)
  - Debian Python Policy 0.12.0.0 documentation -> "Packages in Debian should use Python 3"
  - The following included modules should be sufficent: sys, os, urllib, tarfile 
- The delivered tool need not be installed (Run with ./)

## Design considerations:

If no third party dependancies, no need to manage virtual environment if code supported by python 3.x
Also no need for installation means no packaging (execute by script calling interpreter with shebang line)

The following is tested: 
- PEP 8 conformity – Style Guide for Python Code (check with Pylint) 
- Python 3.x compatibility (check with tox)   

The following failure modes are considered:
- Call error
  - Expected arguments is only one. Additional or no aruguments to raise an exception and inform user of incorrect usage
  - Only limited architectures are supported. However hardcoding this to the tool is limiting so the argument is not filtered. If no contents file found: "No Contents file associated with <architecture>". Feels like not enough architectures exist to justify spell correct/recommender so this functionality will keep it simple rather.  
- Connection error
  - Return exception, unable to connect to mirror

The following edge cases are considered:
- Multiple packages with the same number of assocaited files are ranked alphabetically. The first 10 are only ever returned
- If less than 10 packages exist then use "\<package_name\>" as a placeholder for each missing entry

The MIT license is chosen -> "short and simple permissive license"
