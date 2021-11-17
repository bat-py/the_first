-- MySQL dump 10.13  Distrib 8.0.26, for Linux (x86_64)
--
-- Host: localhost    Database: the_first
-- ------------------------------------------------------
-- Server version	8.0.26-0ubuntu0.20.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `active_orders`
--

DROP TABLE IF EXISTS `active_orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `active_orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chat_id` int NOT NULL,
  `order_number` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_time` datetime NOT NULL,
  `type` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `active_orders`
--

LOCK TABLES `active_orders` WRITE;
/*!40000 ALTER TABLE `active_orders` DISABLE KEYS */;
INSERT INTO `active_orders` VALUES (19,1868842357,'WRZQ-2835977','2021-10-27 16:06:17','product_order'),(21,1868842357,'ICGK-7472981','2021-10-27 17:27:29','product_order');
/*!40000 ALTER TABLE `active_orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `additional_data`
--

DROP TABLE IF EXISTS `additional_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `additional_data` (
  `id` int NOT NULL,
  `data_name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `data` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `additional_data`
--

LOCK TABLES `additional_data` WRITE;
/*!40000 ALTER TABLE `additional_data` DISABLE KEYS */;
INSERT INTO `additional_data` VALUES (1,'feedbacks_count','999'),(2,'password','helloworld'),(3,'bot_api_token','2064216907:AAHf7XNF59-1P9JSTQGW5ZZUaEMvmO2wxl8'),(4,'bot_user_name','@JYQSCBzyoot6wgjLne7Jbot');
/*!40000 ALTER TABLE `additional_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cities`
--

DROP TABLE IF EXISTS `cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cities` (
  `id` int NOT NULL,
  `city` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cities`
--

LOCK TABLES `cities` WRITE;
/*!40000 ALTER TABLE `cities` DISABLE KEYS */;
INSERT INTO `cities` VALUES (10,'Уфа'),(20,'Челябинск'),(30,'Оренбург'),(40,'Тольятти'),(50,'Воронеж'),(60,'Старый Оскол'),(70,'Новосибирск'),(80,'Красноярск');
/*!40000 ALTER TABLE `cities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedbacks`
--

DROP TABLE IF EXISTS `feedbacks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedbacks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_date` date NOT NULL,
  `customer_name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rate` int NOT NULL,
  `feedback_text` varchar(512) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedbacks`
--

LOCK TABLES `feedbacks` WRITE;
/*!40000 ALTER TABLE `feedbacks` DISABLE KEYS */;
INSERT INTO `feedbacks` VALUES (1,'2021-10-21','@hjikogfg',9,'Отличный товар'),(2,'2021-10-21','@hjikogfg',10,'Отличный товар'),(3,'2021-10-21',' @hjikogfg',10,'Отличный товар'),(4,'2021-10-21','На сайте',10,'Все четко, в одно косание поднял!!'),(5,'2021-10-21','@evgen3111',10,'Всё чётко и по факту'),(6,'2021-10-21','@zawirax',10,'Косание 👍🤙✌️'),(7,'2021-10-21','@Mark0fak',10,'Спасибо гуд'),(8,'2021-10-21','@K_chertu_love',10,'None'),(9,'2021-10-21','@mensever888',9,'Поднял правда пришлось поискать'),(10,'2021-10-21','Аноним',10,'Всё огонь'),(11,'2021-10-21','Аноним',10,'От души'),(12,'2021-10-21',' @powar100',10,'Все огонь'),(13,'2021-10-21','Аноним',7,'Пробки не было'),(14,'2021-10-22','@WEfildLOSED',7,'Еле нашёл. Координаты на фоло с реальным местом отличались метров на 100.'),(15,'2021-10-22','@Minimum163',10,'Всё очень просто и понятно!'),(16,'2021-10-22','@hbyvhdh',1,'Ненашол'),(17,'2021-10-22',' @Camelote935',9,'В касание 👍👍👍'),(18,'2021-10-22','На сайте',10,'Тайник поднят в касание. Курик красавчик. Стаф супер'),(19,'2021-10-22',' @Velcome82',10,'Все ровно как обычно:)'),(20,'2021-10-22','@hjikogfg',10,'Супер'),(21,'2021-10-22','@zima_73',1,'Ст. Оскол. Весь лес заминирован. На всех подьезах мусора. Уже 3 дня, район зоопарка'),(22,'2021-10-22','@Camelote935',9,'Просто в касание'),(23,'2021-10-22','@Praser777',10,'Поднял в касание всегда ровно'),(24,'2021-10-22','Аноним',10,'None\r\n'),(25,'2021-10-22','@Sangen174',10,'Всё меняется, кроме надёжности вашего магазина😉 Центр, 0,5 ск дома.'),(26,'2021-10-22','@Pilimeni',10,'Вес на месте сьем нет так быстрый т.к темное время суток'),(27,'2021-10-22','@vikit2',10,'None'),(28,'2021-10-22','@Petro33',10,'Всё чётко и в касание👍👍👍'),(29,'2021-10-22','@Mark0fak',10,'дома'),(30,'2021-10-23','@Yriy787_832038376',9,'Место клада супер,фото ясное и понятное\r\nСпасибо за отличный сервис'),(31,'2021-10-23',' @hjikogfg',10,'Клад лежит ок'),(32,'2021-10-23','@Camelote935',9,'Всё ок👍строго по отметки 👍👍👍'),(33,'2021-10-23','@Camelote935',7,'Всё прошло отлично 👍'),(34,'2021-10-23','@Mark0fak',10,'Огонь'),(35,'2021-10-23','@GrigoruiT',10,'.'),(36,'2021-10-23','@GrigoruiT',10,'.'),(37,'2021-10-23','@GrigoruiT',10,'.'),(38,'2021-10-23',' @GrigoruiT',10,'.'),(39,'2021-10-23',' @GrigoruiT',10,'.'),(40,'2021-10-23','@Rezervor',10,'H'),(41,'2021-10-23','Аноним',5,'Курьер перепутал адрес. А так все ровно'),(42,'2021-10-23','@pusaibnary666',9,'Все ок'),(43,'2021-10-23','@Camelote935',9,'Все просто супер 👍👍👍'),(44,'2021-10-23','Аноним',9,'Всё чётко, в одно касание.'),(45,'2021-10-23','@Anastasiy05',9,'Спасибо,ок!'),(46,'2021-10-23','@leonidleoni',10,'Ок поднял сразу'),(47,'2021-10-23',' @diman163rus',10,'Дома дома'),(48,'2021-10-23','@diman163rus',10,'Дома душа'),(49,'2021-10-23','@Tataru102',10,'все четко вершки к вершкам, корешки к корешкам'),(50,'2021-10-23','@Druuuyo',8,'Молодцы всё Ровно и чётко');
/*!40000 ALTER TABLE `feedbacks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `klad_types`
--

DROP TABLE IF EXISTS `klad_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `klad_types` (
  `id` int NOT NULL,
  `type` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `klad_types`
--

LOCK TABLES `klad_types` WRITE;
/*!40000 ALTER TABLE `klad_types` DISABLE KEYS */;
INSERT INTO `klad_types` VALUES (10,'Прикоп'),(20,'Магнит'),(30,'Тайник');
/*!40000 ALTER TABLE `klad_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `on/off`
--

DROP TABLE IF EXISTS `on/off`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `on/off` (
  `id` int NOT NULL,
  `status` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `on/off`
--

LOCK TABLES `on/off` WRITE;
/*!40000 ALTER TABLE `on/off` DISABLE KEYS */;
INSERT INTO `on/off` VALUES (0,'off'),(1,'on');
/*!40000 ALTER TABLE `on/off` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_methods`
--

DROP TABLE IF EXISTS `payment_methods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_methods` (
  `id` int NOT NULL AUTO_INCREMENT,
  `status` int NOT NULL,
  `method_name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `my_wallet` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payment_method_status` (`status`),
  CONSTRAINT `payment_method_status` FOREIGN KEY (`status`) REFERENCES `on/off` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Если хотите указать несколь. кошельков тогда укажите через ,';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_methods`
--

LOCK TABLES `payment_methods` WRITE;
/*!40000 ALTER TABLE `payment_methods` DISABLE KEYS */;
INSERT INTO `payment_methods` VALUES (1,1,'Оплата с баланса',''),(2,1,'Лайткоин','MFsJqCD2vh5DXVs4sBeqH1rQM7N6qWxzjJ'),(3,1,'Биткоин','1GNMBqQ9EedvtMa7NwVz58bDsnw1orGE63'),(4,1,'Банковской картой','5536-9140-4627-3359');
/*!40000 ALTER TABLE `payment_methods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `city` int NOT NULL,
  `product` int NOT NULL,
  `rayon` int NOT NULL,
  `massa` int NOT NULL,
  `price` int NOT NULL,
  `klad_type` int NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_massa` (`massa`),
  KEY `product_rayon` (`rayon`),
  KEY `product_status` (`status`),
  KEY `product_type` (`product`),
  KEY `city` (`city`),
  KEY `chosen_klad_type` (`klad_type`),
  CONSTRAINT `chosen_klad_type` FOREIGN KEY (`klad_type`) REFERENCES `klad_types` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `product_city` FOREIGN KEY (`city`) REFERENCES `cities` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `product_massa` FOREIGN KEY (`massa`) REFERENCES `products_massa` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `product_rayon` FOREIGN KEY (`rayon`) REFERENCES `products_rayons` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `product_status` FOREIGN KEY (`status`) REFERENCES `on/off` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `product_type` FOREIGN KEY (`product`) REFERENCES `products_types` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,10,40,5,40,3000,30,1),(2,20,10,15,50,4500,10,1),(3,20,10,85,20,1500,10,1),(4,20,50,85,20,1300,10,1),(5,30,10,25,50,6000,10,1),(6,30,50,30,40,3800,10,1);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_massa`
--

DROP TABLE IF EXISTS `products_massa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_massa` (
  `id` int NOT NULL,
  `massa_gr` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_massa`
--

LOCK TABLES `products_massa` WRITE;
/*!40000 ALTER TABLE `products_massa` DISABLE KEYS */;
INSERT INTO `products_massa` VALUES (20,'0.50gr'),(30,'1.00gr'),(40,'2.00gr'),(50,'3.00gr'),(60,'5.00gr'),(70,'20.00gr');
/*!40000 ALTER TABLE `products_massa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_rayons`
--

DROP TABLE IF EXISTS `products_rayons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_rayons` (
  `id` int NOT NULL,
  `region` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `region` (`region`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_rayons`
--

LOCK TABLES `products_rayons` WRITE;
/*!40000 ALTER TABLE `products_rayons` DISABLE KEYS */;
INSERT INTO `products_rayons` VALUES (70,'Березовка'),(25,'Дзержинский'),(35,'Железнодорожный'),(55,'Заельцовский'),(45,'Коминтерновский'),(75,'Ленинский'),(10,'Новомихайловка'),(60,'Октябрьский'),(30,'Оренбургский район, загородное шоссе'),(80,'Свердловский'),(50,'Северо-Восточный'),(40,'Советский'),(65,'Солнечный'),(15,'Сосновский'),(20,'Терема-моховички'),(85,'Центр'),(5,'Юматово');
/*!40000 ALTER TABLE `products_rayons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_types`
--

DROP TABLE IF EXISTS `products_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_types` (
  `id` int NOT NULL,
  `type` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `photo_name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `about` varchar(8192) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_types`
--

LOCK TABLES `products_types` WRITE;
/*!40000 ALTER TABLE `products_types` DISABLE KEYS */;
INSERT INTO `products_types` VALUES (10,'АЛЬФА (ПВП) КРИСТАЛЛ','alfa_pvp.jpg','Безупречное качество, лучшее на рынке в своей категории! Подтверждено огромным колличеством ваших восторженных отзывов! \r\n\r\nСильный стимулятор с эффектом эйфоретика. Приятно взбудоражит и расширит сознание без ярко выраженных побочных эффектов Способы употребления: перорально, интраназально, внутревенно, курение. \r\n\r\nВремя действия: до 8 часов ( в зависимости от вашего толлера ).'),(20,'Синтетический гашиш','sinteticheskiy_gashish.jpg','Пластичный и очень удобный в употребление. В составе натуральные ингредиенты и синтетические реагенты.\r\nУбивает наповал. Будьте осторожны.'),(30,'Убойные шишки','',''),(40,'Шишки Amnesia Feminised','shishki_amneziya.jpg','Действие Amnesia Feminised \r\n\r\nAmnesia обладает эффектом слабого наркотического опьянения, которое сочетается с психоделическими изменениями в восприятии и мышлении, а также бодрящим действием. В высоких дозировках приходит и stone-эффект, но это мощный сорт - принимать в крупных количествах не рекомендуется. Способствует радостному вхождению в утро, в вечернее время снимает стресс и усталость. На вечеринках способствует шумному веселью со смехом и танцами. Лёгкий афродизиак, Амнезия как никакой другой сорт подходит для интима и романтических свиданий. Приятно также любоваться природой или слушать музыку, или заниматься творчеством - резвая сативка поддержит любые ваши способы развлекаться. Эффект длится до 2 часов\r\n\r\n\r\nПод нашим чутким  руководоством гроверы совершают волшебство'),(50,'Мефедрон Мука','mefedron.jpg','Воздушная мука.\r\n\r\nС первого трека мир наполнится красками и любовью. Вихрь теплых эмоций, разрушая границы дозволенного понесет тебя в долгие часы мягкого наслаждения. Желания, еще недавно находившиеся под запретом, станут доступными. Все барьеры исчезнут, останется только первобытная страсть. Мягкий выход без побочных эффектов обусловлен непревзойденной чистотой препарата, изготовленного по идеальной формуле с использованием высококачественных прекурсоров.\r\n\r\n\r\nСпособы употребления: \r\n\r\nПерорально\r\nОжидание: 20 - 40 мин.\r\nДействие: 1.5 - 4 часа.\r\nЭффект: Нет выраженного прихода. Мягкий вход и плавный выход.\r\nСпособы:\r\n- растворить в жидкости, например в соке или воде\r\n- \"бомбочкой\" - завернуть в салфетку/бумагу/хлебныймякиш/лицетиновуюкапсули, проглотить и запить водой.\r\n\r\nИнтраназально\r\nОжидание: 5 - 15 мин.\r\nДействие: 40 мин. - 2 часа.\r\nЭффект: Есть приход - сильная эйфория. Резкий вход, быстрый выход.'),(60,'Мефедрон 4-ММС Кристалл','mefedron_4mmc.jpg','Мощный эйфоретик! При употреблении заставит Вас почувствовать сильную эйфорию, стимулирующий эффект, способствует более глубокому пониманию музыки, повышает общительность, поднимает настроение, вызывает улучшение умственной деятельности и оказывает легкое возбуждение/влечение к противоположному полу.');
/*!40000 ALTER TABLE `products_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL,
  `first_name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `referal` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `balance` int NOT NULL,
  `city` int DEFAULT NULL,
  `chosen_city` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_city` (`city`),
  KEY `user_chosen_city` (`chosen_city`),
  CONSTRAINT `user_chosen_city` FOREIGN KEY (`chosen_city`) REFERENCES `cities` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_city` FOREIGN KEY (`city`) REFERENCES `cities` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1466497132,'Me indoneysia','D201IPY',0,NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-28 11:22:13
