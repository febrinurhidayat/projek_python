-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 16, 2024 at 11:02 AM
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
-- Database: `projectpython`
--

-- --------------------------------------------------------

--
-- Table structure for table `stocks`
--

CREATE TABLE `stocks` (
  `item_id` varchar(20) NOT NULL,
  `name` mediumtext DEFAULT NULL,
  `price` mediumtext DEFAULT NULL,
  `quantity` mediumtext DEFAULT NULL,
  `category` mediumtext DEFAULT NULL,
  `tanggal_masuk` datetime NOT NULL DEFAULT current_timestamp(),
  `tanggal_keluar` datetime DEFAULT NULL
) ENGINE=Aria DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stocks`
--

INSERT INTO `stocks` (`item_id`, `name`, `price`, `quantity`, `category`, `tanggal_masuk`, `tanggal_keluar`) VALUES
('731-M', 'CPU case v2', '12354', '2', 'Computer Parts', '2023-09-04 01:56:32', '0000-00-00 00:00:00'),
('167-S', 'Screw Driver', '189', '40', 'Repair Tools', '2023-09-04 01:58:43', '2024-01-14 00:00:00'),
('344-A', 'Video Card', '10000', '12', 'Computer Parts', '2023-08-06 18:52:03', '2024-01-15 00:00:00'),
('543-C', 'Processor CPU i7', '240000', '50', 'Computer Parts', '2023-08-06 18:52:50', '0000-00-00 00:00:00'),
('851-Y', 'PSU 450 watts', '4000', '30', 'Computer Parts', '2023-09-04 01:16:41', '0000-00-00 00:00:00'),
('768-P', 'Processor AMD 5', '120993', '124', 'Computer Parts', '2023-09-04 01:16:53', '0000-00-00 00:00:00'),
('162-T', 'ROM', '12354', '120', 'Computer Parts', '2023-09-04 01:19:09', '0000-00-00 00:00:00'),
('871-U', 'keyboard', '150000', '5', 'Repair Tools', '2024-01-14 16:35:24', '0000-00-00 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `Jabatan` enum('admin','karyawan') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `Jabatan`) VALUES
(1, 'febri', 'admin123', 'admin'),
(3, 'gentar', 'gentar123', 'karyawan'),
(4, 'zanuar', 'zanuar123', 'admin'),
(5, 'coba', '123', 'admin'),
(10, 'a', 'a', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `stocks`
--
ALTER TABLE `stocks`
  ADD PRIMARY KEY (`item_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
