-- 建資料庫
CREATE DATABASE test2_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 進入資料庫
USE test2_db;

-- 依順序建立表單  
CREATE TABLE `county` (
  `county_ID` int not null auto_increment comment '縣市ID(PK)',
  `region` char(2) not null comment '區域',
  `county_name` char(3) not null comment '縣市',
  primary key (county_ID)
) comment="縣市表";

CREATE TABLE `TAG` (
  `TAG_ID` int not null auto_increment comment 'TAG ID(PK)',
  `TAG_name` varchar(20),
  primary key (TAG_ID)
) comment="TAG表";

CREATE TABLE `campground` (
  `campground_ID` int not null auto_increment comment '露營場ID(PK)',
  `county_ID` int not null comment '縣市ID(FK)',
  `camping_site_name` varchar(40) not null comment '露營場',
  `address` varchar(50) not null comment '地址',
  `total_rank` float comment '露營場評級',
  `total_comments_count` int comment '總評論數',
  `altitude` int comment '海拔高度',
  `traffic_rating` int comment '交通評級',
  `bathroom_rating` int comment '浴廁評級',
  `view_rating` int comment '景觀評級',
  `service_rating` int comment '服務評級',
  `facility_rating` int comment '設備評級',
  primary key (campground_ID),
  constraint fk_county_id foreign key(county_id) references county(county_id) on update cascade on delete restrict
) comment="露營場表";

CREATE TABLE `camping_site` (
  `camping_site_ID` int not null auto_increment comment '營位ID(PK)',
  `campground_ID` int not null comment '露營場ID(FK)',
  `camping_site_type_name` varchar(10) not null comment '營位',
  `price` int comment '營位價格',  
  primary key (camping_site_ID),
  constraint fk_camping_site_campground_ID foreign key(campground_ID) references campground(campground_ID) on update cascade on delete restrict
) comment="營位表";

CREATE TABLE `equipment` (
  `equipment_ID` int not null auto_increment comment '設備ID(PK)',
  `campground_ID` int not null comment '露營場ID(FK)',
  `equipment_details` varchar(80) not null comment '設備',
  primary key (equipment_ID) ,
  constraint fk_equipment_campground_ID foreign key(campground_ID) references campground(campground_ID) on update cascade on delete restrict
) comment="設備表";

CREATE TABLE `service` (
  `service_ID` int not null auto_increment comment '服務ID(PK)',
  `campground_ID` int not null comment '露營場ID(FK)',
  `service_details` varchar(80) not null comment '服務',
  primary key (service_ID),
  constraint fk_service_campground_ID foreign key(campground_ID) references campground(campground_ID) on update cascade on delete restrict
) comment="服務表";

CREATE TABLE `platform` (
  `platform_ID` int not null auto_increment comment '媒體平台ID(PK)',
  `platform_name` varchar(15) not null comment '媒體平台',
  primary key (platform_ID)
) comment="媒體平台表";

CREATE TABLE `campers` (
  `camper_ID` int not null auto_increment comment '露營客ID(PK)',
  `platform_ID` int not null comment '媒體平台ID(FK)',
  `camper_name` varchar(40) not null comment '露營客',
  primary key (camper_ID),
  constraint fk_campers_platform_ID foreign key(platform_ID) references platform(platform_ID) on update cascade on delete restrict
) comment="露營客表";

CREATE TABLE `articles` (
  `articles_ID` int not null auto_increment comment '文章ID(PK)',
  `platform_ID` int not null comment '媒體平台ID(FK)',
  `camper_ID` int not null comment '露營客ID(FK)',
  `campground_ID` int not null comment '露營場ID(FK)',
  `article_type` varchar(10) not null comment '類型',
  `publish_date` date comment '發表日期',
  `article_rank` float comment '評論星數',
  `content` text comment '內容',
  primary key (articles_ID),
  constraint fk_articles_platform_ID foreign key(platform_ID) references platform(platform_ID) on update cascade on delete restrict,
  constraint fk_articles_camper_ID foreign key(camper_ID) references campers(camper_ID) on update cascade on delete restrict,
  constraint fk_articles_campground_ID foreign key(campground_ID) references campground(campground_ID) on update cascade on delete restrict
) comment="發表文章表"; 

-- 建立縣市的資料
insert into
	county(region, county_name)
values
	("北區", "台北市"),
    ("北區", "新北市"),
    ("北區", "基隆縣"),
    ("北區", "桃園市"),
    ("北區", "苗栗縣"),
    ("北區", "新竹縣"),
    ("中區", "台中市"),
    ("中區", "彰化縣"),
	("中區", "南投縣"),
    ("中區", "雲林縣"),
    ("南區", "嘉義縣"),
    ("南區", "台南市"),
    ("南區", "高雄市"),
    ("南區", "屏東縣"),
    ("東區", "宜蘭縣"),
    ("東區", "花蓮縣"),
    ("東區", "台東縣");

select * from county;
