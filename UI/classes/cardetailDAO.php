<?php
    require_once "connectionmanager.php";
    class cardetailDAO{
    function extractfromautotrader(){
        $connMgr = new connectionmanager();
        $conn = $connMgr->getConnection();

        $sql = 'select * from autotradercarinfo';
        $stmt = $conn->prepare($sql);
        $stmt->setFetchMode(PDO::FETCH_ASSOC);
        $stmt->execute();
        $result = array();
        while ($row = $stmt->fetch()){
            $result[] = new carautotrader($row['carplatenumber'], $row['brand'], $row['model'], $row['yearofmanufactured'], $row['milleage'], $row['price'], $row['transmission'], $row['dealercode'], $row['enginecapacity']);
        }
        $stmt->closeCursor();
        $conn = null;
        return $result;
    }
}



?>