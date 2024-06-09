<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

<?php 
$serverName = "DESKTOP-P5PRM6N";
$connectionOptions = array(
    "database" => "ESQL_project",
    "uid" => "user", 
    "pwd" => "0000",
    "CharacterSet" => "UTF-8"
);

$name = $_GET["name"];
$qty = $_GET["qty"];
//echo $name;
//echo $qty;

$dbconn = sqlsrv_connect($serverName, $connectionOptions);

$query = "SELECT *
          FROM product
          WHERE pname = '$name'"; 

$result = sqlsrv_query($dbconn, $query);
$stmt = sqlsrv_query($dbconn, $query);
$row = sqlsrv_fetch_array($stmt, SQLSRV_FETCH_ASSOC);

if($qty>0){
if($row["pnum"]){
    $pnum = $row["pnum"];
    $price = $row["price"] * $qty;
    $query = "SELECT qty_current
          FROM stock
          WHERE pnum = '$pnum'"; 

$result = sqlsrv_query($dbconn, $query);
$stmt = sqlsrv_query($dbconn, $query);
$row = sqlsrv_fetch_array($stmt, SQLSRV_FETCH_ASSOC);
$qty_current = $row["qty_current"];

if(($qty_current - $qty)>=0){
    $qty_current = $qty_current - $qty;

    $query = "UPDATE stock
              SET qty_current = '$qty_current'
              WHERE pnum = '$pnum'";
    $result = sqlsrv_query($dbconn, $query);
    $stmt = sqlsrv_query($dbconn, $query);
    if($stmt){
        
        echo "<script>alert('주문이 완료되었습니다.');</script>";
        $timestamp = date("Y-m-d/H:i:s");
        $query = "INSERT INTO salesSlip
                  VALUES ('$timestamp','$pnum','$qty','$price')";
        $result = sqlsrv_query($dbconn, $query);
        $stmt = sqlsrv_query($dbconn, $query);
    }
    }
else{
        echo "<script>alert('상품 수량이 부족합니다.');</script>";}
}
else{
    echo "<script>alert('올바른 상품이름을 입력해주세요.');</script>";}
}
else{
    echo "<script>alert('0 이상의 수량을 입력해주세요.');</script>";}
?>

<!DOCTYPE html>
<html>
  <head><br><b><font color="blue", size="7">주문내역<br><br></font></b></head>
  <body>
    <p>주문시간: <?php echo date("Y-m-d/H:i:s");?></p>
    <p>상품이름: <?php echo $name; ?></p>
    <p>주문수량: <?php echo $qty; ?></p>
    <p>가격: <?php echo $price; ?></p>
    <p>현재 남은수량: <?php echo $qty_current; ?></p>
  </body>
</html>


 