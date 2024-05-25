===============================================
Tutorial: Erstellen einer Webseite mit MySQL, PHP und Charts
===============================================

Voraussetzungen:
- Webserver mit PHP-Unterstützung (z.B. Apache)
- MySQL oder MariaDB
- phpMyAdmin (optional)

===============================================
Schritt 1: Einrichtung der Datenbank
===============================================

1. Datenbank und Tabellen erstellen:
   - Führen Sie die folgenden SQL-Befehle in phpMyAdmin aus:
    ```
   CREATE DATABASE sensordata;

   USE sensordata;

   CREATE TABLE readings (
       id INT AUTO_INCREMENT PRIMARY KEY,
       reading_date DATE,
       LPG FLOAT,
       Hum FLOAT,
       Temp FLOAT
   );

   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) UNIQUE,
       password VARCHAR(255)
   );
   ```

===============================================
Schritt 2: Einrichtung des Backend (PHP)
===============================================

2. Datenbankverbindung (db.php):
```
   <?php
   $servername = "localhost";
   $username = "root";
   $password = "";
   $dbname = "sensordata";

   // Create connection
   $conn = new mysqli($servername, $username, $password, $dbname);

   // Check connection
   if ($conn->connect_error) {
       die("Connection failed: " . $conn->connect_error);
   }
   ?>
   ```

3. Daten hinzufügen (add_data.php):
```
   <?php
   include 'db.php';

   if ($_SERVER['REQUEST_METHOD'] == 'POST') {
       $date = $_POST['date'];
       $LPG = $_POST['LPG'];
       $Hum = $_POST['Hum'];
       $Temp = $_POST['Temp'];

       $sql = "INSERT INTO readings (reading_date, LPG, Hum, Temp) VALUES ('$date', '$LPG', '$Hum', '$Temp')";
       
       if ($conn->query($sql) === TRUE) {
           echo "New record created successfully";
       } else {
           echo "Error: " . $sql . "<br>" . $conn->error;
       }
   }
   ?>
```

4. Daten abrufen (get_data.php):
```
   <?php
   include 'db.php';

   $sql = "SELECT * FROM readings";
   $result = $conn->query($sql);

   $data = [];

   if ($result->num_rows > 0) {
       while($row = $result->fetch_assoc()) {
           $data[] = $row;
       }
   }

   echo json_encode($data);
   ?>
```

5. Benutzeranmeldung und Registrierung (auth.php):
```
   <?php
   include 'db.php';
   session_start();

   if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['register'])) {
       $username = $_POST['username'];
       $password = password_hash($_POST['password'], PASSWORD_DEFAULT);

       $sql = "INSERT INTO users (username, password) VALUES ('$username', '$password')";
       
       if ($conn->query($sql) === TRUE) {
           echo "New user created successfully";
       } else {
           echo "Error: " . $sql . "<br>" . $conn->error;
       }
   }

   if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['login'])) {
       $username = $_POST['username'];
       $password = $_POST['password'];

       $sql = "SELECT * FROM users WHERE username='$username'";
       $result = $conn->query($sql);
       $user = $result->fetch_assoc();

       if ($user && password_verify($password, $user['password'])) {
           $_SESSION['user_id'] = $user['id'];
           echo "Login successful";
       } else {
           echo "Invalid credentials";
       }
   }
   ?>
````

===============================================
Schritt 3: Einrichtung des Frontend (HTML, CSS, JavaScript)
===============================================

6. HTML-Struktur (index.html):
```
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Sensor Data</title>
       <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
   </head>
   <body>
       <!-- HTML-Formulare für Registrierung, Anmeldung, Daten hinzufügen -->
       <!-- Chart.js-Canvas für die Anzeige der Daten als Liniengrafen -->
   </body>
   </html>
```
===============================================
Schritt 4: Sicherheitsmaßnahmen und Berechtigungen
===============================================

7. Passwort-Hashing und SQL-Injection verhindern.
8. Zugriffskontrolle: Sicherstellen, dass nur authentifizierte Benutzer auf bestimmte Seiten zugreifen können.
9. Berechtigungen setzen (Linux): Anpassen der Datei- und Ordnerberechtigungen, damit der Webserver darauf zugreifen kann.

===============================================
Zusammenfassung
===============================================

Mit diesen Schritten haben Sie eine komplette Anwendung erstellt, die Daten in einer MySQL-Datenbank speichert und diese als Liniengrafen darstellt. Benutzer können sich registrieren, anmelden und Daten hinzufügen. Achten Sie darauf, Ihre Anwendung kontinuierlich zu testen und sicherzustellen, dass alle Sicherheitslücken geschlossen sind.
