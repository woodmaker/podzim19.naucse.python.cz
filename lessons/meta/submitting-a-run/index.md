# Přidání kurzu na Nauč se Python

Když už máme nadefinováný vlastní kurz, zbývá nám jen ho dostat na [naucse.python.cz](https://naucse.python.cz/).
Budeme k tomu potřebovat jen pár příkazu v gitu a trochu trpělivosti.

## Nahrání do vlastního forku

První věc, kterou budeš potřebovat je vlastní účet na [GitHubu](https://github.com/).
Poté, co se zaregistruješ na GitHubu, potřebuješ „Fork” [repozitáře pyvec/naucse.python.cz](https://github.com/pyvec/naucse.python.cz).
Fork si vytvoříš tím, že půjdeš na stránku repozitáře a vpravo nahoře klikneš na tlačítko Fork.

<div style="text-align: center">
{{ figure(
    img=static('naucse_fork.png'),
    alt="Tlačítko na vytvoření forku repozitáře s Nauč se Python",
) }}
</div>

Vytvoření chvilku trvá.
To, že je fork vytvořen poznáš tak, že tě GitHub přesměruje na stránku, která bude skoro stejná, ale v hlavičce bude tvoje uživatelské jméno a pod tím text `forked from pyvec/naucse.python.cz`.

Tvůj fork si teď potřebuješ přidat do lokálního repozitáře jako referenci, aby jsi tam pak mohl{{a}} poslat svůj kurz.
To uděláš pomocí příkazu (nahraď `tvojejmeno` za tvoje uživatelské jméno na GitHubu):

```console
$ git remote add tvojejmeno https://github.com/tvojejmeno/naucse.python.cz.git
```

Dále potřebuješ vytvořit commit se svým kurzem a případně se změnami v materiálech.
Je také nutné se rozhodnout, jestli chceš svoje změny dělat přímo v hlavní větvi nebo jestli si na kurz vytvořit separátní větev.
Pokud se s větvemi nechceš zaobírat, můžeš vytvářet rovnou commit, pokud chceš větev vytvořit, vymysli si nějaký její název a pusť příkazy

```console
$ git branch nazevvetve
$ git checkout nazevvetve
```

Jak vytvořit commit najdeš například v [návodu na používání gitu]({{lesson_url("git/git-collaboration-2in1")}}).
Více o větvích se můžeš dozvědět v [návodu na větvení v gitu]({{lesson_url("git/branching")}}).

Svůj commit teď potřebuješ dostat do svého forku na GitHubu.
To uděláš příkazem (`tvojejmeno` nahraď za tvoje uživatelské jméno na GitHubu):

```console
$ git push tvojejmeno
```

## Informace o forku pro Nauč se

Teď potřebuješ dostat informaci o tvém forku do základního repozitáře.
To se dělá pomocí souboru `link.yml`, se kterým se udělá Pull Request do základního repozitáře.

Nejdřív si vytvoř novou větev odvozenou od původního repozitáře, ve které vytvoříš soubor `link.yml`.
To uděláš tímto příkazem (`pridanikurzu` můžeš změnit):

```console
$ git checkout -b pridanikurzu origin/master
```

Možná sis všiml{{a}}, že tvoje změny jsou najednou pryč, ale neboj, ony jsou uložené jak na tvém počítači tak na GitHubu, jen zrovna nejsou vidět.

Teď potřebuješ vytvořit stejnou složku jako jsi vytvořil{{a}} pro soubor `info.yml` – musí se jmenovat úplně stejně.
V té složce vytvoř soubor, který se tentokrát bude jmenovat `link.yml`.
Bude zase ve formátu YAML, ale tentokrát bude jednoduchý.
Jedinou povinou informací je klíč `repo`, do kterého musíš dát odkaz na tvůj fork.
Pokud sis vytvořil{{a}} i na kurz separátní větev, napiš jí do kíče `branch` (pokud ne, klíč `branch` tam vůbec nemusíš dávat).
Výsledný soubor pak vypadá následovně:

```yaml
repo: https://github.com/tvojejmeno/naucse.python.cz.git
branch: nazevvetve
```

Vytvoř s tímto souborem (a jen tímto souborem) commit a zase odešli změnu na GitHub.

```console
$ git push tvojejmeno
```

Teď už potřebuješ udělat Pull Request (dále jen jako PR) se souborem `link.yml`.
Jak udělat PR je popsáno v [návodu na používání gitu]({{lesson_url("git/git-collaboration-2in1")}}).
Ideálně do popisku napiš kdo jsi a co organizuješ za kurz, ať to správci nemusí zjišťovat například z popisku v `info.yml`.

Po tom co se správci PR schváli a sloučí tvoje změny do základního repozitáře, stačí počkat pár minut a tvůj kurz se objeví na [naucse.python.cz](https://naucse.python.cz/).

## Upravování kurzu

Už naprosto poslední věc, kterou je potřeba zařídit, je aby, když uděláš změny ve svém kurzu u sebe ve forku, tak aby se projevily na Nauč se.
To se dělá pomocí tzv. webhooků, webových adres, které reagují na nějaké akce.
Musíme tedy nastavit tvůj fork, aby posílal akce na webhook, který vyvolá nové nasazení Nauč se.

Pro instalaci webhooků máme speciální aplikaci, která je umí sama nastavit.
Běží na adrese [hooks.nauc.se](https://hooks.nauc.se).
Když se v té aplikaci přihlásíš, uvidíš tam svůj fork Nauč se (a všechny ostatní forky Nauč se, ke kterým máš přístup).
Poté už jen stačí kliknout na tlačítko Aktivovat u správného repozitáře a webhook se nainstaluje.
A to je všechno! Přidal{{a}} jsi kurz na Nauč se!

> [note]
> Pokud to umíš a chceš, můžeš si webhook nainstalovat {{gnd("sám", "sama")}} manuálně.
> Adresa webhooku je `https://hooks.nauc.se/hooks/push`, je potřeba `Content-Type` `application/json` a secret není potřeba zadávat.
