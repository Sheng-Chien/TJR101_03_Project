-- MySQL dump 10.13  Distrib 8.4.4, for Win64 (x86_64)
--
-- Host: 104.199.214.113    Database: test2_db
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `MART_campground_with_emotion`
--

DROP TABLE IF EXISTS `MART_campground_with_emotion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MART_campground_with_emotion` (
  `campground_emotion_ID` int NOT NULL AUTO_INCREMENT COMMENT 'MART_熱門露營場及情緒ID(PK)',
  `campground_ID` int NOT NULL COMMENT '露營場ID(FK)',
  `camping_site_name` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '露營場',
  `campground_category` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '好評;普通;差評',
  `hot` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '是否是熱門露營場',
  `negative_ratio` float DEFAULT NULL COMMENT '負評比例',
  `positive_ratio` float DEFAULT NULL COMMENT '正評比例',
  `hot_but_negative` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '熱門但負評比例超過50%',
  `count` int DEFAULT NULL COMMENT '後續分析時計算用，固定為1',
  PRIMARY KEY (`campground_emotion_ID`),
  KEY `fk_mart_emotion_campground_id` (`campground_ID`),
  CONSTRAINT `fk_mart_emotion_campground_id` FOREIGN KEY (`campground_ID`) REFERENCES `campground` (`campground_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1254 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='MART_露營場熱度及對露營場的好評或差評';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `MART_campground_with_tag`
--

DROP TABLE IF EXISTS `MART_campground_with_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MART_campground_with_tag` (
  `campground_tag_ID` int NOT NULL AUTO_INCREMENT COMMENT 'MART_露營場tag表ID(PK)',
  `campground_ID` int NOT NULL COMMENT '露營場ID(FK)',
  `county_ID` int NOT NULL COMMENT '縣市ID(FK)',
  `camping_site_name` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '露營場',
  `address` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '地址',
  `Tag` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '露營場評級',
  `ref_keywords` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '總評論數',
  `tag_count` int DEFAULT '1' COMMENT '後續視覺化分析時計算用，固定數值1',
  PRIMARY KEY (`campground_tag_ID`),
  KEY `fk_mart_tag_campground_id` (`campground_ID`),
  KEY `fk_mart_tag_county_id` (`county_ID`),
  CONSTRAINT `fk_mart_tag_campground_id` FOREIGN KEY (`campground_ID`) REFERENCES `campground` (`campground_ID`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_mart_tag_county_id` FOREIGN KEY (`county_ID`) REFERENCES `county` (`county_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3982 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='MART_露營場TAG表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `TAG`
--

DROP TABLE IF EXISTS `TAG`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TAG` (
  `TAG_ID` int NOT NULL AUTO_INCREMENT COMMENT 'TAG ID(PK)',
  `TAG_name` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`TAG_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='TAG表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `articles` (
  `articles_ID` int NOT NULL AUTO_INCREMENT COMMENT '文章ID(PK)',
  `platform_ID` int NOT NULL COMMENT '媒體平台ID(FK)',
  `camper_ID` int NOT NULL COMMENT '露營客ID(FK)',
  `campground_ID` int NOT NULL COMMENT '露營場ID(FK)',
  `article_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '類型',
  `publish_date` date DEFAULT NULL COMMENT '發表日期',
  `article_rank` float DEFAULT NULL COMMENT '評論星數',
  `content` mediumtext COLLATE utf8mb4_unicode_ci COMMENT '內容',
  PRIMARY KEY (`articles_ID`),
  KEY `fk_articles_platform_ID` (`platform_ID`),
  KEY `fk_articles_camper_ID` (`camper_ID`),
  KEY `fk_articles_campground_ID` (`campground_ID`),
  CONSTRAINT `fk_articles_camper_ID` FOREIGN KEY (`camper_ID`) REFERENCES `campers` (`camper_ID`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_articles_campground_ID` FOREIGN KEY (`campground_ID`) REFERENCES `campground` (`campground_ID`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_articles_platform_ID` FOREIGN KEY (`platform_ID`) REFERENCES `platform` (`platform_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=41982 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='發表文章表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `campers`
--

DROP TABLE IF EXISTS `campers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `campers` (
  `camper_ID` int NOT NULL AUTO_INCREMENT COMMENT '露營客ID(PK)',
  `platform_ID` int NOT NULL COMMENT '媒體平台ID(FK)',
  `camper_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '露營客',
  PRIMARY KEY (`camper_ID`),
  KEY `fk_campers_platform_ID` (`platform_ID`),
  CONSTRAINT `fk_campers_platform_ID` FOREIGN KEY (`platform_ID`) REFERENCES `platform` (`platform_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=46993 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='露營客表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `campground`
--

DROP TABLE IF EXISTS `campground`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `campground` (
  `campground_ID` int NOT NULL AUTO_INCREMENT COMMENT '露營場ID(PK)',
  `county_ID` int NOT NULL COMMENT '縣市ID(FK)',
  `camping_site_name` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '露營場',
  `address` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '地址',
  `total_rank` float DEFAULT NULL COMMENT '露營場評級',
  `total_comments_count` int DEFAULT NULL COMMENT '總評論數',
  `altitude` int DEFAULT NULL COMMENT '海拔高度',
  `traffic_rating` int DEFAULT NULL COMMENT '交通評級',
  `bathroom_rating` int DEFAULT NULL COMMENT '浴廁評級',
  `view_rating` int DEFAULT NULL COMMENT '景觀評級',
  `service_rating` int DEFAULT NULL COMMENT '服務評級',
  `facility_rating` int DEFAULT NULL COMMENT '設備評級',
  PRIMARY KEY (`campground_ID`),
  KEY `fk_county_id` (`county_ID`),
  CONSTRAINT `fk_county_id` FOREIGN KEY (`county_ID`) REFERENCES `county` (`county_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1502 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='露營場表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `campground_merge`
--

DROP TABLE IF EXISTS `campground_merge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `campground_merge` (
  `idx` int NOT NULL COMMENT '對照表的營地索引',
  `name` char(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '上傳資料的人',
  `camping_site_name` char(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '營地名稱',
  `address` char(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '營地地址',
  `campground_ID` int DEFAULT NULL COMMENT '營地ID',
  `similar_idx` int DEFAULT NULL COMMENT '相似營地的索引',
  `repeat` tinyint(1) DEFAULT NULL COMMENT '是否重複',
  PRIMARY KEY (`name`,`camping_site_name`,`address`),
  KEY `fk_campground_ID` (`campground_ID`),
  CONSTRAINT `fk_campground_ID` FOREIGN KEY (`campground_ID`) REFERENCES `campground` (`campground_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `camping_site`
--

DROP TABLE IF EXISTS `camping_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `camping_site` (
  `camping_site_ID` int NOT NULL AUTO_INCREMENT COMMENT '營位ID(PK)',
  `campground_ID` int NOT NULL COMMENT '露營場ID(FK)',
  `camping_site_type_name` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '營位',
  `price` int DEFAULT NULL COMMENT '營位價格',
  PRIMARY KEY (`camping_site_ID`),
  KEY `fk_camping_site_campground_ID` (`campground_ID`),
  CONSTRAINT `fk_camping_site_campground_ID` FOREIGN KEY (`campground_ID`) REFERENCES `campground` (`campground_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1037 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='營位表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `county`
--

DROP TABLE IF EXISTS `county`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `county` (
  `county_ID` int NOT NULL AUTO_INCREMENT COMMENT '縣市ID(PK)',
  `region` char(2) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '區域',
  `county_name` char(3) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '縣市',
  PRIMARY KEY (`county_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='縣市表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment` (
  `equipment_ID` int NOT NULL AUTO_INCREMENT COMMENT '設備ID(PK)',
  `campground_ID` int NOT NULL COMMENT '露營場ID(FK)',
  `equipment_details` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '設備',
  PRIMARY KEY (`equipment_ID`),
  KEY `fk_equipment_campground_ID` (`campground_ID`),
  CONSTRAINT `fk_equipment_campground_ID` FOREIGN KEY (`campground_ID`) REFERENCES `campground` (`campground_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5336 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='設備表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `platform`
--

DROP TABLE IF EXISTS `platform`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform` (
  `platform_ID` int NOT NULL AUTO_INCREMENT COMMENT '媒體平台ID(PK)',
  `platform_name` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '媒體平台',
  PRIMARY KEY (`platform_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='媒體平台表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `special`
--

DROP TABLE IF EXISTS `special`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `special` (
  `special_ID` int NOT NULL AUTO_INCREMENT COMMENT '特色ID(PK)',
  `campground_ID` int NOT NULL COMMENT '露營場ID(FK)',
  `special_details` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '特色',
  PRIMARY KEY (`special_ID`),
  KEY `fk_special_campground_ID` (`campground_ID`),
  CONSTRAINT `fk_special_campground_ID` FOREIGN KEY (`campground_ID`) REFERENCES `campground` (`campground_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4597 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='服務表';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-13 11:34:34
