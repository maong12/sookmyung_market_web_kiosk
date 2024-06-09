<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

<?php 

$serverName = "DESKTOP-P5PRM6N";
$connectionOptions = array(
    "database" => "ESQL_project", 
    "uid" => "user", 
    "pwd" => "0000", 
    "CharacterSet" => "UTF-8"
);

// DB커넥션
$dbconn = sqlsrv_connect($serverName, $connectionOptions);

 ?>

<!DOCTYPE html>
<html>
    <body>
        <h1> 숙명매점 </h1>
        <table border="1">
            <tr>
                <td>상품번호</td><td>상품이름</td><td>가격</td><td>남은수량</td>
                <?php
                $query = "SELECT p.pnum, pname, price, qty_current 
                          FROM product p, stock s
                          where p.pnum = s.pnum"; 

                $stmt = sqlsrv_query($dbconn, $query);

                while ($row = sqlsrv_fetch_array($stmt, SQLSRV_FETCH_ASSOC)){

                    $filtered = array(

                    'pnum'=>htmlspecialchars($row['pnum']),
                    'pname'=>htmlspecialchars($row['pname']),
                    'price'=>htmlspecialchars($row['price']),
                    'qty_current'=>htmlspecialchars($row['qty_current']));
                    ?>
                    <tr>
                    <td><?=$filtered['pnum']?></td>
                    <td><?=$filtered['pname']?></td>
                    <td><?=$filtered['price']?></td>
                    <td><?=$filtered['qty_current']?></td>
                    </tr>
                    <?php
                    }
                    ?>
                </tr>
            </table>
            <form action = "process_order.php" method="get">
                <p><input type="text" name="name" placeholder="상품이름"</p>
                <p><input type="text" name="qty" placeholder="상품수량"</p>
                <p><input type="submit" value="결제"></p>
            </form>
        </body>
    </html>
 
<?php
// statement 해제
sqlsrv_free_stmt($stmt);
// 데이터베이스 접속 해제
sqlsrv_close($dbconn);
?>