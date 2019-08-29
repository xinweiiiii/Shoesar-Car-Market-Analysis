<?php

class carautotrader{
    private $carplatenumber;
    private $brand;
    private $model;
    private $yearofmanufactured;
    private $milleage;
    private $price;
    private $transmission;
    private $dealercode;
    private $enginecapacity;

    public function __construct($carplatenumber, $brand, $model, $yearofmanufactured, $milleage, $price, $transmission, $dealercode, $enginecapacity){
        $this->carplatenumber = $carplatenumber;
        $this->brand = $brand;
        $this->model = $model;
        $this->yearofmanufactured = $yearofmanufactured;
        $this->milleage = $milleage;
        $this->price = $price;
        $this->transmission = $transmission;
        $this->dealdercode = $dealercode;
        $this->enginecapacity = $enginecapacity;
    }

    public function getcarplatenumber(){
        return $this->carplatenumber;
    }

    public function getbrand(){
        return $this->brand;
    }

    public function getmodel(){
        return $this->model;
    }

    public function getyearofmanufactured(){
        return $this->yearofmanufactured;
    }

    public function getmilleage(){
        return $this->milleage;
    }

    public function getprice(){
        return $this->price;
    }

    public function gettransmssion(){
        return $this->transmission;
    }

    public function getdealercode(){
        return $this->dealercode;
    }

    public function getenginecapacity(){
        return $this->enginecapacity;
    }
}




?>