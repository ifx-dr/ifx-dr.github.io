# Introduction
webpage for Digital Reference

# How to update

## Prerequisites
1. WiDoCo - Ensure WiDoCo is installed to generate documentation. If GUI isn't working, please  use terminal to open widoco
```
java -jar widoco-1.4.20-jar-with-dependencies_JDK-14.jar
```
2. Python - Confirm Python is set up and configured correctly to run `main.py`.
3. install BeautifulSoup
```
pip install bs4
```

## Installation

1. Clone the repository.
2. Navigate to the DR website generator folder.
3. open `main.py` to start the documentation process.

## Update Process

### Classes, Objects, and Properties

1. Use WiDoCo - Run WiDoCo and import the latest DigitalReference.ttl in https://github.com/tibonto/dr to generate the initial draft of the documentation for the Digital Reference.
2. File Path - Update the WiDoCo file path in main.py within the DR website generator folder.
3. Lobe List - Review the lobe list and add any new lobes that have been created.

### Namespaces

1. New Namespaces - With any new namespaces added, generate documentation using WiDoCo and create a folder in the subontology directory.
2. Manual Additions - Please search the div with id 'namespaces' in index.html to update the namespace section by manually adding references. For example:
```
<dt id="dr">
  <abbr title="Digital Reference">dr</abbr>
</dt>
<dd>
  <code>
    <a href="#" target="_blank">http://www.w3id.org/ecsel-dr#</a>
  </code>
</dd>
```
3. Table of Contents - Please search the summary with text 'Namespaces' in index.html to manually add the new namespace references to the table of contents within the summary section:
```
<li>
  <a href="#ecsel-dr-AH">ecsel-dr-AH</a>
</li>
```

## Hash Record Update

1. Copying Record - Take the hash record you received by email.
2. Update script.js - Paste this record into the bottom section of the script.js file and save the file, ensuring the indices and dates are correct.
3. Example of hash record entry:
```
{
    "index": 69,
    "date": "07.02.2024",
    "commitSHA": "cb51d9634a2ec010263a7340960ca18ccbc06a8d",
    "comment": "Synchronize version metadata and increase it by one minor",
    "hash": "acc72cc8041688e900a5f476fe91221ff900c11b18e3e32899e07ccd8f3853f0",
    "previousHash": "9383887fd0bca4f5b686d43df59b30bdc79d4ccc32dfd6945e2bf4a1d125a47b"
}
```