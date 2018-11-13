# Kontrola stylu zdrojového kódu

Jedna věc nám v Atomu přeci jen chybí: plugin pro kontrolu správného
stylu zdrojového kódu.

Tak jako čeština má Python typografická providla.
Například za čárkou se píše mezera, ale před ní ne.
Jsou nepovinná, program bude fungovat i při jejich nedodržení,
ale pomáhají psát přehledný kód, tak je dobré je dodržovat už od začátku.
Pravidla pro Python jsou popsána v dokumentu
[PEP8](https://www.python.org/dev/peps/pep-0008/).

Aby sis je nemusel{{a}} všechny pamatovat, nainstaluj si plugin,
který tě na jejich porušení upozorní.

Nejprve je potřeba si nainstalovat speciální knihovnu, která se o kontrolu
dokáže postarat. Do příkazové řádky zadej následující:

```console
$ python -m pip install flake8
```

A nyní si nainstaluj plugin do samotného editoru. V hlavní nabídce vyber
„Soubor > Nastavení<span class="en">/File > Settings</span>“ a v nabídce
uprostřed okna vyber poslední položku
„Instalovat<span class="en">/Install</span>“. Do vyhledávacího pole zadej
„linter-flake8“ a v seznamu nalezených pluginů klikni u položky stejného jména
na tlačítko „Instalovat<span class="en">/Install</span>“. Bude ještě potřeba
schválit instalaci všech závislostí, na které se Atom postupně zeptá.
