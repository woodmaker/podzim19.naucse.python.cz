# Lokální instalace Nauč se python

K přidání kurzu nejdřív člověk potřebuje vlastní, lokální instalaci Nauč se.

## Příprava

První věc, kterou budeš potřebovat je Python, a to ve verzi 3.6.
Pokud zrovna danou verzi Pythonu nainstalovanou nemáš, můžeš postupovat podle [návodu na instalaci Pythonu]({{lesson_url("beginners/install")}}).

Druhá věc, kterou budeš potřebovat je git – pokud nemáš ten, můžeš postupovat podle [návodu na instalaci gitu]({{lesson_url("git/install")}}).

Poslední věc, kterou potřebuješ už není žádný program, ale pár schopností.
Je potřeba, aby jsi uměl{{a}} s terminálem a s gitem.
Použivání příkazové řádky si můžeš připomenout v [návodu na používání terminálu]({{lesson_url("beginners/cmdline")}}) a používání gitu v [návodu na používání gitu]({{lesson_url("git/git-collaboration-2in1")}}).

## Instalace

Nejprve musíš naklonovat repozitář, ze kterého se Nauč se Python vykresluje.
To uděláš tímto příkazem:

```console
$ git clone https://github.com/pyvec/naucse.python.cz
```

Poté přepni adresář do naklonovaného repozitáře:

```console
$ cd naucse.python.cz
```

A vytvoř si v něm virtuální prostředí – pokud nevíš jak na to, můžeš se podívat do návodu na instalaci Pythonu, na který je odkaz výše.
Virtuální prostředí si rovnou aktivuj.

Poslední krok instalace je nainstalování závislostí:

```console
(__venv__)$ python -m pip install -r requirements.txt
```

{{ anchor('launch') }}
## Spuštění

Teď když máš Nauč se nainstalované, tak stačí už jen pustit.
Nejdříve si musíš nastavit proměnou prostředí.
Na Unixu (Linux, macOS):

```console
(__venv__)$ export PYTHONPATH=.
```

Na Windows:

```dosvenv
(__venv__)> set PYTHONPATH=.
```

Nauč se jde pustit ve dvou režimech.
První režim vykresluje každou stránku pokaždé znova – hodí se na vývoj, aby byly všechny změny okamžitě vidět.
Pustí se následovně:

```console
(__venv__)$ python -m naucse serve
 * Running on http://0.0.0.0:8003/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 256-270-314
```

V ukázce vidíš rovnou i příklad toho co to vypíše – zajímá tě jen ta adresa, to ve formátu `http://0.0.0.0:8003/`.
Když si ji zkopíruješ a otevřeš ve webovém prohlížeči, uvidíš Nauč se.

Druhý režim nejdříve vykreslí všechny stránky a až poté ti je zobrazí – hodí se spíše na kontrolu toho, že se při vývoji nic nepokazilo.
Pustí se následovně (pozor, nějakou chvíli to trvá):

```console
(__venv__)$ python -m naucse freeze --serve
Generating HTML...
 * Running on http://127.0.0.1:8003/ (Press CTRL+C to quit)
```

> [note]
> Když odnaviguješ například do seznamu kurzů, je možné, že tam nebudou všechny.
> To jsou kurzy, které se vykreslují z jiných forků, které jsou na lokálním prostředí
> automaticky vypnuté.
