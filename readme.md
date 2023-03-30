## System accountant dostępny przez stronę www
### Bazując na aplikacji do zarządzania firmą, stwórz jej webowy odpowiednik.
#### Na stronie głównej wyświetl informację na temat stanu konta,magazynu oraz trzy formularze: 
1. zakup, 
2. sprzedaż, 
3. zmiana salda.
#### Formularz zakupu powinien zawierać trzy pola: 
1. nazwa produktu,
2. cena produktu,
3. ilość
#### Formularz sprzedaży powinien zawierać dwa pola:
1. nazwa produktu,
2. ilość
#### Formularz zmiany salda powinien zawierać jedno pole:
1. wartość zmiany salda
#### Dodatkowo utwórz drugą podstronę zawierającą historię wykonanych operacji. Podstrona powinna być dostępna pod URL "/historia/" oraz "/historia/<start>/<koniec>"
1. W przypadku "/historia/" na stronie ma się pojawić cała dostępna historia.
2. W przypadku "/historia/<start>/<koniec>" zależnie od podanych wartości w <start> i <koniec>, mają się pojawić wskazane linie, np. od 3 do 12. W przypadku podania złego (lub nieistniejącego zakresu indeksów), program poinformuje o tym użytkownika i wyświetli możliwy do wybrania zakres historii.
#### Zadanie wciąż powinno korzystać z plików do przechowywania stanu konta, magazynu i historii.