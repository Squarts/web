<?php

require 'koneksi.php';

$task = mysqli_query($conn, "SELECT * FROM tbltasks");

?>

<html>
<head>    
    <title>Home</title>
</head>
<body>
    <a href="add.php">Add New User</a><br/><br/>

    <table width = 50% border = 1>
        <tr>
            <th>ID</th> 
            <th>Title</th> 
            <th>Description</th> 
            <th>Deadline</th> 
            <th>Complete</th> 
            <th>Aksi</th>
        </tr>

    <?php $i = 1; ?>
    <?php foreach($task as $tsk){ ?>
        <tr>
            <td><?= $i; ?></td>
            <td><?= $tsk["title"]; ?></td>
            <td><?= $tsk["description"]; ?></td>
            <td><?= $tsk["deadline"]; ?></td>
            <td><?= $tsk["complete"]; ?></td>
            <td>
                <a href = "update.php?id=<?= $tsk["id"]; ?>">Edit</a> |
                <a href = "delete.php?id=<?= $tsk["id"]; ?>">Delete</a>
            </td>
        </tr>
    <?php $i++ ?> 
    <?php } ?> 
    </table>

</body>

</html>