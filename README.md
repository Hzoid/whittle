# Whittle

## Description

Whittle is a versatile tool designed for refining large wordlists into more manageable and targeted subsets, ideal for password audits and security testing. 

## Features

* Filters passwords by minimum and maximum length
* Enforces [Microsoft's Password Complexity Requirements](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/password-must-meet-complexity-requirements)
* Allows for the filtering of passwords containing user-specific information (samAccountName & displayName) - see the above link.
* Verbose output for detailed processing information
* Efficient processing suitable for large wordlists like rockyou.txt

# Usage

## Basic Usage

### Enforce Microsoft's Password Complexity Requirements and output to text file
`python whittle.py -c -w /path/to/wordlist.txt -o /path/to/output.txt`

### Only allow passwords with a minimum length of 8 and a maximum length of 12
`python whittle.py -m 8 -M 12 -w /path/to/wordlist.txt -o /path/to/output.txt`

### Enforce Microsoft's Password Complexity Requirements, alongside the samAccountName and displayName of a target
`python whittle.py -c --sam-account jdoe --display-name "John Doe" -w /path/to/wordlist.txt -o /path/to/output.txt`

### Process with verbose statistics
`python whittle.py -v -w /path/to/wordlist.txt -o /path/to/output.txt`

## Help Page

```
usage: whittle.py [-h] [-m MINIMUM_LENGTH] [-M MAXIMUM_LENGTH] [-c] [--sam-account SAM_ACCOUNT [SAM_ACCOUNT ...]]
                  [--display-name DISPLAY_NAME [DISPLAY_NAME ...]] -w WORDLIST [-o OUTPUT] [-v]


░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓████████▓▒░
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓██████▓▒░
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░
 ░▒▓█████████████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░  ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓████████▓▒░

    A tool to refine big wordlists - because sometimes less is more.

options:
  -h, --help            show this help message and exit
  -m MINIMUM_LENGTH, --minimum-length MINIMUM_LENGTH
                        Minimum password length (default: 7)
  -M MAXIMUM_LENGTH, --maximum-length MAXIMUM_LENGTH
                        Maximum password length
  -c, --complexity-check
                        Enforce Microsoft's password complexity requirements
  --sam-account SAM_ACCOUNT [SAM_ACCOUNT ...]
                        User samAccountName(s) if known
  --display-name DISPLAY_NAME [DISPLAY_NAME ...]
                        Windows display name(s) if known
  -w WORDLIST, --wordlist WORDLIST
                        Path to wordlist
  -o OUTPUT, --output OUTPUT
                        Path for processed wordlist - prints to stdout by default
  -v, --verbose         Increase output verbosity
```
## Benchmarks

Whittle is designed with speed and efficiency in mind, as it is intended for larger wordlists.
Computationally inexpensive checks such as password length restrictions are made first, which also happened to be the highest factor of rejection.

Current testing showed effecient processing of [rockyou.txt](https://github.com/praetorian-inc/Hob0Rules/blob/master/wordlists/rockyou.txt.gz), using a system with 64GB DDR4 and a Ryzen 7 2700X:

```
python whittle.py -w ..\wordlists\rockyou.txt -o .\whittled_rockyou.txt -M 12 -m 6 -v -c

Passwords processed: 14344391/14344391
Total Passwords Processed: 14344391
Passwords Accepted: 771797
Passwords Rejected: 13572594
Processing Time: 348.05 seconds
```

# Installation

### Clone the Whittle repository to your local machine

`git clone https://github.com/hzoid/whittle.git`

### Install Dependencies

Install the required Python module using the requirements.txt file:

`pip3 install -r requirements.txt`

# Contributing

Contributions and feature requests are welcome! Please refer to the contributing guidelines for more information.
