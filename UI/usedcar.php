<html>

<head>

<title>Used Car</title>

<link rel="stylesheet" href="CSS/page.css">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
</head>

<body>
<?php
    require_once "classes/carautotrader.php";
    require_once "classes/cardetailDAO.php";
    $check = true;
    echo "<div class = 'containeroutside'>";
    echo "<h1>Sheosar Search Engine</h1></br>";
    echo "<form method = 'POST'>";
    echo "<button type='submit' name = 'used'>Used Car</button>";
    echo "<button type='submit' name  = 'new'>New Car</button>";
    echo "<button type='submit' name = 'sell'>Sell My Car</button></br>";
    echo "<div class = 'container'>";
    echo "<input type = 'text' name = 'carmake' value = 'Car Make or Model'>  ";
    echo "<input type = 'text' name  = 'year' value = 'Registered Year'>   ";
    echo "<input type = 'text' name = 'vehicle type' value = 'Vehicle Type'>  ";
    echo "<button type='submit' name  = 'find'>Find</button>  ";
    echo "<button type='submit' name = 'advanced'>Advanced Search</button></br>";
    echo "</div>";
    #locate individual data
    if (isset($_POST['used']) or $check == true){
        $dao = new cardetailDAO();
        $crawlingAuto = $dao->extractfromautotrader();
        foreach ($crawlingAuto as $data){
            $brand = $data->getbrand();
            $model = $data->getmodel();
            $price = $data->getprice();
            $milleage = $data->getmilleage();
            $year = $data->getyearofmanufactured();
            $engine = $data->getenginecapacity();
            $transmission = $data->gettransmssion();
            echo "<table class='a'>";
                echo "<tr>";
                    echo "<td rowspan = '8' colspan = '5'><img src='image/sample1.jpg' width='300' height='200'></td>";
                    echo "<td colspan = '6'><h2>$brand $model</h2></td>";
                    echo "<td colspan = '20'></td>";
                    echo "<td colspan = '2'><h3>Asking Price</h3></td>";
                echo "</tr>";
                echo "<tr>";
                    echo "<td colspan = '3'><h3>Location<h3></td>";
                    echo "<td colspan = '22'></td>";
                    echo "<td colspan = '3'><h2>$price</h2></td>";
                echo "<tr>";
                echo "<tr>";
                    echo "<td colspan = '28'></td>";
                echo "</tr>";
                echo "<tr>";
                    echo "<td colspan = '28'></td>";
                echo "</tr>";
                echo "<tr>";
                    echo "<td colspan = '28'></td>";
                echo "</tr>";
                echo "<tr>";
                    echo "<td></td>";
                    echo "<td></td>";
                    echo "<td>$milleage</td>";
                    echo "<td></td>";
                    echo "<td></td>";
                    echo "<td>$year</td>";
                    echo "<td></td>";
                    echo "<td></td>";
                    echo "<td>$engine</td>";
                    echo "<td></td>";
                    echo "<td></td>";
                    echo "<td>$transmission</td>";
                echo "</tr>";
                echo "<tr><td colspan = '28'></></tr>";
            echo "</table>";
        }
    }
    echo "</form>";
    echo "</div>";
#Add in the load more button after 20 display


?>
</body>

</html>
