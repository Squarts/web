<?php
session_start();

require 'koneksi.php';

$id = $_GET["id"];

function hapus($id){
    global $conn;
    mysqli_query($conn, "DELETE FROM tbltasks WHERE id = $id");
    return mysqli_affected_rows($conn);
}

    if(hapus($id) > 0){
        echo "
        <script>
        alert('data berhasil dihapus');
        document.location.href = 'index.php';
        </script>";
    } else {
        echo "
        <script>
        alert('data gagal dihapus');
        document.location.href = 'index.php';
        </script>";
    }
?>