# Mechanizmy i narzędzie automatycznego wykrywania i inwentaryzacji infrastruktury

Narzędzie w postaci aplikacji w języku Python agregujące różnego rodzaju mechanizmy i metody wykrywania i inwentaryzacji infrastruktury sieciowej, udostępniające pozyskane dane w ustandaryzowanej formie - pliku w formacie JSON.

## Protokoły/standardy:

### ARP

Address Resolution Protocol (ARP) -- protokół komunikacyjny wykorzystywany do odnajdywania adresów fizycznych (warstwy 2) i mapowania ich na adresy IP (warstwa 3).

### SNMP

Simple Network Management Protocol (SNMP) -- protokół wykorzystywany do zbierania i organizowania informacji o zarządzanych urządzeniach w sieciach IP, oraz modyfikowania tych informacji (w celu zmiany konfiguracji urządzenia). Protokół ten obsługiwany jest przez wiele różnych urządzeń, w tym routery, przełączniki, drukarki, itp.

Protokół SNMP standardowo korzysta z portu 161 do wysyłania i odbierania zapytań, oraz portu 162 do przechwytywania sygnałów *trap* od monitorowanych urządzeń.

### SSH

Secure Shell Protocol (SSH) -- protokół komunikacyjny umożliwiający zdalne logowanie i wykonywanie poleceń. Komunikacja z wykorzystaniem SSH jest szyfrowana.

## Narzędzia:

### arp-scan

Narzędzie *arp-scan* pozwala na wykrycie i identyfikację klientów podłączonych do sieci lokalnej. Jest to realizowane poprzez wysyłanie zapytań ARP na zadane adresy IP lub całe ich przedziały (np. wszystkie adresy IP w sieci o określonej masce). W ten sposób możemy dowiedzieć się, które ze sprawdzanych adresów są przypisane do klientów podłączonych do sieci.

Ponieważ obsługa protokołu ARP jest konieczna by korzystać z sieci IP, będzie go obsługiwać każde z urządzeń, zatem każde urządzenie zostanie wykryte. Jest to istotna zaleta w porównaniu z narzędziem *ping*, które korzysta z protokołu ICMP, który może być blokowany przez niektóre urządzenia (np. te z zainstalowanym systemem Windows z domyślną konfiguracją).

### arp-fingerprint

Narzędzie *arp-fingerprint* wysyła różne rodzaje zapytań ARP i przetwarza uzyskane odpowiedzi, tworząc "odcisk palca" złożony z "1" dla zapytań, na które uzyskano odpowiedź, i "0" dla zapytań bez odpowiedzi. Przykładowy odcisk palca może wyglądać następująco: 01000100000. Na podstawie odcisku palca można można wnioskować o systemie operacyjnym urządzenia, do którego wysyłane były zapytania (jednakże trafność rozpoznawania na tej podstawie systemu operacyjnego jest niezadowalająca, ponieważ wiele systemów operacyjnych może dawać taki sam odcisk palca).

### snmpget i snmpwalk

Narzędzia *snmpget* i *snmpwalk* służą do wysyłania zapytań SNMP. *snmpget* pozwala na odczytanie wartości pojedynczego liścia drzewa wartości, natomiast *snmpwalk* -- całego drzewa lub jego fragmentu.

Za pomocą *snmpget* odpytujemy każde ze znalezionych wcześniej urządzeń o jego nazwę (OID 1.3.6.1.2.1.1.5.0) i opis (OID 1.3.6.1.2.1.1.1.0).

Następnie za pomocą *snmpwalk* uzyskujemy listę adresów IP (OID 1.3.6.1.2.1.1.5.0) i adresów MAC (OID 1.3.6.1.2.1.4.22.1.2) połączonych z nim urządzeń.

Ze względu na przyjęte założenie znacznej automatyzacji procesu wykrywania infrastruktury, korzystamy z uwierzytelnienia za pomocą community *public* (co jednak jest w większości przypadków wystarczające dla uzyskania pożądanych informacji).

### Nmap

Nmap (Network Mapper) -- narzędzie służące do skanowania portów i wykrywania usług sieciowych. Umożliwia testowanie portów na wiele różnych sposobów.

W naszym narzędziu z *nmap* korzystamy na dwa sposoby: uzyskując jedynie informację o dostępności urządzeń o podanych adresach IP (`nmap -nsP`), lub informacje rozszerzone o otwarte porty (oraz dla jakich usług typowo są te porty wykorzystywane) i zainstalowany system operacyjny.

### SSH

Ponieważ zakres działania *arp-scan* ogranicza się tylko do sieci lokalnej, potrzebowaliśmy możliwości uruchamiania go na zdalnych maszynach. Do tego celu korzystamy z SSH, za pomocą którego można połączyć się do zdalnej maszyny, pobrać na nią nasze narzędzie, uruchomić je, przesłać z powrotem plik wynikowy, a następnie usunąć wszystkie pobrane i wygenerowane pliki z maszyny zdalnej (przywracając ją do stanu sprzed użycia narzędzia).
