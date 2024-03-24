-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 24, 2024 at 10:23 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `taskdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbltasks`
--

CREATE TABLE `tbltasks` (
  `id` int(11) NOT NULL COMMENT 'Task ID - Primary Key',
  `title` varchar(255) NOT NULL COMMENT 'Task Title',
  `description` mediumtext NOT NULL COMMENT 'Task Description',
  `deadline` datetime NOT NULL COMMENT 'Task Deadline Date',
  `complete` enum('Y','N') NOT NULL DEFAULT 'N' COMMENT 'Task \r\nCompletion Status'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbltasks`
--

INSERT INTO `tbltasks` (`id`, `title`, `description`, `deadline`, `complete`) VALUES
(1, 'Task 1', 'Description 1', '2023-02-23 03:34:14', 'N'),
(2, 'Task 2', 'Description 2', '2023-02-23 03:34:14', 'N'),
(3, 'Task 3', 'Description 3', '2023-02-23 03:34:14', 'N'),
(4, 'Task 4', 'Description 4', '2023-02-23 03:34:14', 'Y'),
(5, 'Task 5', 'Description 5', '2023-02-23 03:34:14', 'N'),
(6, 'Task 6', 'Description 6', '2023-02-23 03:34:14', 'Y');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbltasks`
--
ALTER TABLE `tbltasks`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbltasks`
--
ALTER TABLE `tbltasks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Task ID - Primary Key', AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
