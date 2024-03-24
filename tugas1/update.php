<?php
session_start();

require 'koneksi.php';

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ubah data mahasiswa</title>
</head>
<body>
<h1>Ubah data mahasiswa</h1>

    <form action="" method="post">
		<table width="25%" border="0">
            <tr> 
				<td>Title :</td>
				<td><input type="text" name="title"></td>
			</tr>

			<tr> 
				<td>Description :</td>
				<td><input type="text" name="description"></td>
			</tr>

			<tr> 
				<td>Deadline : </td>
				<td><input type="text" name="deadline"></td>
			</tr>

            <tr> 
				<td>Complete : </td>
				<td><input type="text" name="complete"></td>
			</tr>

            <tr> 
				<td></td>
				<td><button type="submit" name="submit">Ubah Data</button></td>
			</tr>
        </table>
    </form>
</body>
</html>

<?php

if(isset($_POST['submit'])) {
    $id = $_GET['id'];
    $title = $_POST['title'];
    $description = $_POST['description'];
    $deadline = $_POST['deadline'];
    $complete = $_POST['complete'];

    $query = "UPDATE tbltasks SET title = '$title', deadline='$deadline', description='$description', complete='$complete' WHERE id=$id";
    $task = mysqli_query($conn, $query);

    echo "<script> document.location.href = 'index.php'; </script>";
}

?>