from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

print(app)


class Manager:
    def __init__(self):
        self.actions = {}
        self.dostepne_operacje = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista', 'magazyn', 'przeglad', 'koniec']
        self.int_tpl = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
        self.fl_tpl = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.')
        self.historia = {}
        self.magazyn = {}
        self.konto = 0

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb
        return decorate

    def execute(self, name, *args, **kwargs):
        if name not in self.actions:
            print("Action not defined")
        else:
            self.actions[name](self, *args, **kwargs)


manager = Manager()


@manager.assign("pobierz_saldo")
def pobierz_saldo(manager):
    with open('saldo.txt') as sal:
        manager.konto = float(sal.readline().strip())


@manager.assign("nadpisz_saldo")
def nadpisz_saldo(manager, val):
    with open('saldo.txt', 'w') as sal:
        sal.write(f'{val}\n')


@manager.assign("wczytaj_historie")
def wczytaj_historie(manager):
    with open('log.txt') as log:
        pos = 0
        manager.historia.clear()
        for m in log:
            if pos == 0:
                key = int(m.strip())
                pos += 1
            elif pos == 1:
                opis1 = m.strip()
                pos += 1
            elif pos == 2:
                opis2 = m.strip()
                pos += 1
            elif pos == 3:
                opis3 = m.strip()
                pos += 1
            elif pos == 4:
                opis4 = m.strip()
                pos = 0
                manager.historia[key] = [opis1, opis2, opis3, opis4]


@manager.assign("zapisz_historie")
def zapisz_historie(manager, id, oper, par1, par2, par3):
    with open('log.txt', 'a') as log:
        log.write(f'{id}\n{oper}\n{par1}\n{par2}\n{par3}\n')


@manager.assign("wczytaj_magazyn")
def wczytaj_magazyn(manager):
    with open('mag.txt') as mag:
        poz = 0
        manager.magazyn.clear()
        for p in mag:
            if poz == 0:
                kex = p.strip()
                poz += 1
            elif poz == 1:
                ops1 = p.strip()
                poz += 1
            elif poz == 2:
                ops2 = float(p.strip())
                poz += 1
            elif poz == 3:
                ops3 = int(p.strip())
                poz = 0
                manager.magazyn[kex] = [ops1, ops2, ops3]


@manager.assign("nadpisz_magazyn")
def nadpisz_magazyn(manager, magazyn_new):
    f = open('mag.txt', 'w')
    f.close()
    for n in magazyn_new:
        id_prd = n
        prd = magazyn_new[n][0]
        cena_prd = magazyn_new[n][1]
        ilosc_prd = magazyn_new[n][2]
        with open('mag.txt', 'a') as mag:
            mag.write(f'{id_prd}\n{prd}\n{cena_prd}\n{ilosc_prd}\n')


@app.route('/')
def str_glowna():
    return render_template('index.html', operacje=manager.dostepne_operacje)


@app.route('/historia/', methods=['GET', 'POST'])
def przeglad_historii():
    operacja = request.form.get('operacja')
    od = request.form.get('hi_od')
    do = request.form.get('hi_do')
    informacja = ''
    dane = []
    if operacja == "przeglad":
        manager.execute("wczytaj_historie")
        if len(manager.historia) < 1:
            informacja = "Brak wpisow"
        else:
            if od == '' and do == '':
                informacja = "Podano puste wartosci - wyswietlam cala historia"
                dane = manager.historia
            elif od == '' and do != '':
                # sprawdzamy wprowadzona wartosc czy jest int+
                noint = 0
                for y in do:
                    if y not in manager.int_tpl:
                        noint = 1
                if noint == 1 or do == '0':
                    informacja = "Podana wartosc jest niepoprawna"
                    informacja = f"Dopuszczalne wartosci powinny zawierac sie pomiedzy 1 i {len(manager.historia)}"
                else:
                    informacja = "Wyswietlam historie od poczatku do podanej wartosci"
                    for i in manager.historia:
                        if i <= int(do):
                            elm = (i, manager.historia[i])
                            dane.append(elm)
                    dane = dict(dane)
            elif od != '' and do == '':
                noint = 0
                for y in od:
                    if y not in manager.int_tpl:
                        noint = 1
                if noint == 1 or od == '0':
                    informacja = "Podana wartosc jest niepoprawna"
                    informacja = f"Dopuszcalne wartosci powinny zawierac sie pomiedzy 1 i {len(manager.historia)}"
                else:
                    informacja = "Wyswietlam historie od podanej wartosci do konca"
                    for i in manager.historia:
                        if i >= int(od):
                            elm = (i, manager.historia[i])
                            dane.append(elm)
                    dane = dict(dane)
            elif od != '' and do != '':
                noint = 0
                for y in od:
                    if y not in manager.int_tpl:
                        noint = 1
                for z in do:
                    if z not in manager.int_tpl:
                        noint = 1
                if noint == 1:
                    informacja = "Przynajmniej  jedna podana wartosc jest niepoprawna"
                elif int(od) == 0 or int(do) == 0:
                    informacja = f"Podano niedopuszczalna zerowa wartosc dopuszczalne wartosci" \
                                 f" powinny zawierac sie pomiedzy 1 i {len(manager.historia)}"
                elif int(od) > int(do):
                    informacja = f"Wartosc poczatkowa wieksza od koncowej dopuszczalne wartosci " \
                                   "powinny zawierac sie pomiedzy 1 i {len(manager.historia)}"
                else:
                    informacja = "Wyswietlam historie dla podanego zakresu wartosci"
                    for i in manager.historia:
                        if int(od) <= i <= int(do):
                            elm = (i, manager.historia[i])
                            dane.append(elm)
                    dane = dict(dane)
    return render_template('historia.html', informacja=informacja, dane=dane)


@app.route('/', methods=['GET', 'POST'])
def menu_glowne():
    operacja = request.form.get('Operacja')
    saldo_add = request.form.get('kwota')
    produkt = request.form.get('mg_nazwa')
    z_nazwa = request.form.get('za_nazwa')
    z_cena = request.form.get('za_cena')
    z_ilosc = request.form.get('za_ilosc')
    s_nazwa = request.form.get('sp_nazwa')
    s_cena = request.form.get('sp_cena')
    s_ilosc = request.form.get('sp_ilosc')
    komunikat = ''
    wartosc = []
    manager.execute("pobierz_saldo")
    if operacja == "saldo":
        if saldo_add != '':
            if manager.konto + float(saldo_add) < 0:
                komunikat = "Operacja niemozliwa do wykonania"
            else:
                manager.konto += float(saldo_add)
                manager.execute("nadpisz_saldo", manager.konto)
                manager.execute("wczytaj_historie")
                manager.execute("zapisz_historie", len(manager.historia) + 1, 'saldo', manager.konto, '-', '-')
        else:
            komunikat = "Podano pustą wartosc - operacja niemozliwa do wykonania"
    elif operacja == "konto":
        manager.execute("pobierz_saldo")
        komunikat = f"Stan konta wynosi: {manager.konto}"
    elif operacja == "lista":
        komunikat = "Magazyn jest pusty"
        manager.execute("wczytaj_magazyn")
        if not manager.magazyn:
            komunikat = "Magazyn jest pusty"
        else:
            wartosc = manager.magazyn
            komunikat = ''
    elif operacja == "magazyn":
        if produkt == '':
            komunikat = "Podano pusta nazwa - operacja niemozliwa do wykonania"
        else:
            manager.execute("wczytaj_magazyn")
            komunikat = 'Magazyn jest pusty'
            kontrolna = 1
            for element in manager.magazyn:
                if produkt == manager.magazyn[element][0]:
                    kontrolna = 0
                    elem = element, manager.magazyn[element]
                    wartosc.append(elem)
                    wartosc = dict(wartosc)
            if kontrolna == 1:
                komunikat = "Brak w magazynie"
            else:
                komunikat = ''
    elif operacja == "zakup":
        if z_nazwa == '' or z_cena == '' or z_ilosc == '':
            komunikat = "Operacja niemozliwa - podano pusta wartosc"
        else:
            # sprawdzamy poprawnosc ceny i ilosci
            noint = 0
            for y in z_cena:
                if y not in manager.fl_tpl:
                    noint = 1
            for z in z_ilosc:
                if z not in manager.int_tpl:
                    noint = 1
            if noint == 1 or z_cena == '0' or z_ilosc == '0':
                komunikat = "Przynajmniej  jedna podana wartosc jest niepoprawna"
            else:
                manager.execute("pobierz_saldo")
                z_ilosc = int(z_ilosc)
                # jako identyfikatora uzyjemy sumy nazwy i ceny - bo mozemy miec te same produkty o roznych cenach
                magazyn_add = z_nazwa + z_cena, z_nazwa, float(z_cena), z_ilosc
                # Najpierw sprawdzamy czy mamy wystarczajace srodki na koncie
                if manager.konto < (float(magazyn_add[2]) * int(magazyn_add[3])):
                    komunikat = "Operacja niemozliwa - brak wystarczajacych srodkow na koncie"
                else:
                    manager.execute("wczytaj_magazyn")
                    if magazyn_add[0] not in manager.magazyn:
                        # jesli takiego produktu niema w magazynie dopisujemy do magazynu
                        manager.magazyn[magazyn_add[0]] = [magazyn_add[1], magazyn_add[2], magazyn_add[3]]
                        manager.konto -= magazyn_add[2] * magazyn_add[3]
                        manager.execute("nadpisz_saldo", manager.konto)
                        manager.execute("nadpisz_magazyn", manager.magazyn)
                        komunikat = "Dodano produkt do magazynu"
                        manager.execute("wczytaj_historie")
                        manager.execute("zapisz_historie", len(manager.historia)+1, 'zakup', z_nazwa,
                                        float(z_cena), z_ilosc)
                    else:
                        # jesli taki produkt istnieje dodajemy tylko ilosc sztuk
                        x = manager.magazyn[magazyn_add[0]][1]
                        y = manager.magazyn[magazyn_add[0]][2] + z_ilosc
                        manager.magazyn[magazyn_add[0]] = [z_nazwa, x, y]
                        manager.konto -= magazyn_add[2] * magazyn_add[3]
                        manager.execute("nadpisz_saldo", manager.konto)
                        manager.execute("nadpisz_magazyn", manager.magazyn)
                        komunikat = "Zmodyfikowano liczbe produktow w magazynie"
                        manager.execute("wczytaj_historie")
                        manager.execute("zapisz_historie", len(manager.historia)+1, 'zakup', z_nazwa,
                                        float(z_cena), z_ilosc)
    elif operacja == "sprzedaz":
        # weryfikujemy poprawnosc zlecenia
        if s_nazwa == '' or s_cena == '' or s_ilosc == '':
            komunikat = "Operacja niemozliwa - podano pusta wartosc"
        else:
            noint = 0
            for y in s_cena:
                if y not in manager.fl_tpl:
                    noint = 1
            for z in s_ilosc:
                if z not in manager.int_tpl:
                    noint = 1
            if noint == 1 or s_cena == '0' or s_ilosc == '0':
                komunikat = "Przynajmniej  jedna podana wartosc jest niepoprawna"
            else:
                s_ilosc = int(s_ilosc)
                magazyn_mv = s_nazwa + s_cena, s_nazwa, float(s_cena), s_ilosc
                # sprawdzamy czy mamy taki produkt
                manager.execute("wczytaj_magazyn")
                if magazyn_mv[0] not in manager.magazyn:
                    komunikat = "Produktu o takiej nazwie i/lub cenie niema w magazynie"
                else:
                    # sprawdzamy czy mamy wystarczajaca ilosc sztuk
                    if s_ilosc > manager.magazyn[magazyn_mv[0]][2]:
                        komunikat = f"Dostepna ilosc produktu jest mniejsza i wynosi:" \
                                    f" {manager.magazyn[magazyn_mv[0]][2]}"
                    else:
                        # jesli zlecenie zabiera wszystkie sztuki produktu usuwamy produkt z magazynu
                        if s_ilosc == manager.magazyn[magazyn_mv[0]][2]:
                            del manager.magazyn[magazyn_mv[0]]
                            manager.konto += magazyn_mv[2] * magazyn_mv[3]
                            manager.execute("nadpisz_saldo", manager.konto)
                            manager.execute("nadpisz_magazyn", manager.magazyn)
                            komunikat = f"Sprzedano caly zapas produktu: {magazyn_mv[1]} i cenie: {magazyn_mv[2]}"
                            manager.execute("wczytaj_historie")
                            manager.execute("zapisz_historie", len(manager.historia)+1,
                                            'sprzedaz', s_nazwa, float(s_cena), s_ilosc)
                        # jesli taki produkt istnieje modyfikujemy tylko ilosc sztuk
                        else:
                            x = manager.magazyn[magazyn_mv[0]][1]
                            y = manager.magazyn[magazyn_mv[0]][2] - s_ilosc
                            manager.magazyn[magazyn_mv[0]] = [s_nazwa, x, y]
                            manager.konto += magazyn_mv[2] * magazyn_mv[3]
                            manager.execute("nadpisz_saldo", manager.konto)
                            manager.execute("nadpisz_magazyn", manager.magazyn)
                            komunikat = f"Zmodyfikowano ilosc produktu: {magazyn_mv[1]} i cenie: {magazyn_mv[2]} "\
                                        f"obecny stan to {manager.magazyn[magazyn_mv[0]][2]}"
                            manager.execute("wczytaj_historie")
                            manager.execute("zapisz_historie", len(manager.historia)+1,
                                            'sprzedaz', s_nazwa, float(s_cena), s_ilosc)
    # koniec - konczymy program
    elif operacja == "koniec":
        print("Koniec programu")
        quit()
    return render_template('index.html', operacje=manager.dostepne_operacje, komunikat=komunikat, wartosc=wartosc)
