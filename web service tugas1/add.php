<?php

require 'koneksi.php';

?>
    
<html>

<head>
	<title>Add Users</title>
</head>

<body>

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
				<td><button type="submit" name="submit">Tambah Data</button></td>
			</tr>
		</table>
	</form>

	

</body>

</html>

<?php
if(isset($_POST['submit'])) {
		$title = $_POST['title'];
		$description = $_POST['description'];
		$deadline = $_POST['deadline'];
        $complete = $_POST['complete'];

        $query = "INSERT INTO tbltasks Value (NULL, '$title','$description','$deadline','$complete')";
		$task = mysqli_query($conn, $query);

        echo "<script> document.location.href = 'index.php'; </script>";
	}
?>