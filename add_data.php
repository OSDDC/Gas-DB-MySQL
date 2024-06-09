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
