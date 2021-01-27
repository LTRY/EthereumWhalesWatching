-- MySQL dump 10.13  Distrib 8.0.22, for Linux (x86_64)
--
-- Host: localhost    Database: ETH
-- ------------------------------------------------------
-- Server version	8.0.22

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
-- Table structure for table `iswhale`
--

DROP TABLE IF EXISTS `iswhale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `iswhale` (
  `address` varchar(42) NOT NULL,
  `nameTag` varchar(40) DEFAULT NULL,
  `whale` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iswhale`
--

LOCK TABLES `iswhale` WRITE;
/*!40000 ALTER TABLE `iswhale` DISABLE KEYS */;
INSERT INTO `iswhale` VALUES ('0x00000000219ab540356cbb839cbe05303d7705fa','Eth2 Deposit Contract',0),('0x024861e9f89d44d00a7ada4aa89fe03cab9387cd','',1),('0x059799f2261d37b829c2850cee67b5b975432271','Bitstamp 4',0),('0x07ee55aa48bb72dcc6e9d78256648910de513eca','Gemini: Contract 1',0),('0x091933ee1088cdf5daace8baec0997a4e93f0dd6','',1),('0x0a4c79ce84202b03e95b7a692e5d728d83c44c76','',1),('0x0c05ec4db907cfb91b2a1a29e7b86688b7568a6d','',1),('0x0e22e8c049f96170ac41e0e3b360a14feb8083a2','',1),('0x0f00294c6e4c30d9ffc0557fec6c586e6f8c3935','',1),('0x189b9cbd4aff470af2c0102f365fc1823d857965','',1),('0x19d599012788b991ff542f31208bab21ea38403e','',1),('0x1a71b118ac6c9086f43bcf2bb6ada3393be82a5c','',1),('0x1b3cb81e51011b549d78bf720b0d924ac763a7c2','',1),('0x1e2fcfd26d36183f1a5d90f0e6296915b02bcb40','Coinone 2',0),('0x1ffedd7837bcbc53f91ad4004263deb8e9107540','',1),('0x229b5c097f9b35009ca1321ad2034d4b3d5070f6','Huobi 18',0),('0x267be1c1d684f78cb4f6a176c4911b741e4ffdc0','Kraken 4',0),('0x2b6ed29a95753c3ad948348e3e7b1a251080ffb9','',1),('0x2bf792ffe8803585f74e06907900c2dc2c29adcb','',1),('0x367989c660881e1ca693730f7126fe0ffc0963fb','',1),('0x3ba25081d3935fcc6788e6220abcace39d58d95d','',1),('0x3bfc20f0b9afcace800d73d2191166ff16540258','Polkadot: MultiSig',0),('0x3dfd23a6c5e8bbcfc9581d2e864a68feb6a076d3','Aave: Lending Pool Core V1',0),('0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be','Binance',0),('0x40f0d6fb7c9ddd9cbc1c02a208380c08cf77189b','',1),('0x4756eeebf378046f8dd3cb6fa908d93bfd45f139','',1),('0x4b4a011c420b91260a272afd91e54accdafdfc1d','',1),('0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5','Compound Ether',0),('0x53d284357ec70ce289d6d64134dfac8e511c8a3d','Kraken 6',0),('0x550cd530bc893fc6d2b4df6bea587f17142ab64e','',1),('0x554f4476825293d4ad20e02b54aca13956acc40a','',1),('0x558553d54183a8542f7832742e7b4ba9c33aa1e6','',1),('0x5b5b69f4e0add2df5d2176d7dbd20b4897bc7ec4','',1),('0x61edcdf5bb737adffe5043706e7c5bb1f1a56eea','Gemini 3',0),('0x6262998ced04146fa42253a5c0af90ca02dfd2a3','Crypto.com',0),('0x657e46adad8be23d569ba3105d7a02124e8def97','',1),('0x66f820a414680b5bcda5eeca5dea238543f42054','Bittrex 3',0),('0x701bd63938518d7db7e0f00945110c80c67df532','',1),('0x701c484bfb40ac628afa487b6082f084b14af0bd','',1),('0x73263803def2ac8b1f8a42fac6539f5841f4e673','',1),('0x73bceb1cd57c711feac4224d062b0f6ff338501e','',1),('0x742d35cc6634c0532925a3b844bc454e4438f44e','Bitfinex 2',0),('0x7712bdab7c9559ec64a1f7097f36bc805f51ff1a','',1),('0x77afe94859163abf0b90725d69e904ea91446c7b','',1),('0x78b96178e7ae1ff9adc5d8609e000811657993c8','',1),('0x7ae92148e79d60a0749fd6de374c8e81dfddf792','',1),('0x7da82c7ab4771ff031b66538d2fb9b0b047f6cf9','Golem: MultiSig',0),('0x8103683202aa8da10536036edef04cdd865c225e','',1),('0x828103b231b39fffce028562412b3c04a4640e64','',1),('0x844ada2ed8ecd77a1a9c72912df0fcb8b8c495a7','',1),('0x8b83b9c4683aa4ec897c569010f09c6d04608163','',1),('0x8cf23cd535a240eb0ab8667d24eedbd9eccd5cba','',1),('0x90a9e09501b70570f9b11df2a6d4f047f8630d6d','',1),('0x9845e1909dca337944a0272f1f9f7249833d2d19','',1),('0x98ec059dc3adfbdd63429454aeb0c990fba4a128','',1),('0x9a1ed80ebc9936cee2d3db944ee6bd8d407e7f9f','',1),('0x9a9bed3eb03e386d66f8a29dc67dc29bbb1ccb72','Bitstamp 3',0),('0x9bf4001d307dfd62b26a2f1307ee0c0307632d59','',1),('0x9c2fc4fc75fa2d7eb5ba9147fa7430756654faa9','',1),('0x9cf36e93a8e2b1eaaa779d9965f46c90b820048c','',1),('0xa0efb63be0db8fc11681a598bf351a42a6ff50e0','',1),('0xa7e4fecddc20d83f36971b67e13f1abc98dfcfa6','',1),('0xa7efae728d2936e78bda97dc267687568dd593f3','OKEx 3',0),('0xa8dcc0373822b94d7f57326be24ca67bafcaad6b','',1),('0xab5801a7d398351b8be11c439e05c5b3259aec9b','Vb',0),('0xae93ec389ae6fa1c788ed2e1d222460bb6d0177b','',1),('0xb20411c403687d1036e05c8a7310a0f218429503','',1),('0xb8808f9e9b88497ec522304055cd537a0913f6a0','',1),('0xb8cda067fabedd1bb6c11c626862d7255a2414fe','',1),('0xb9fa6e54025b4f0829d8e1b42e8b846914659632','',1),('0xba18ded5e0d604a86428282964ae0bb249ceb9d0','',1),('0xbe0eb53f46cd790cd13851d5eff43d12404d33e8','Binance 7',0),('0xbf3aeb96e164ae67e763d9e050ff124e7c3fdd28','',1),('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2','Wrapped Ether',0),('0xc098b2a3aa256d2140208c3de6543aaef5cd3a94','FTX Exchange 2',0),('0xc4cf565a5d25ee2803c9b8e91fc3d7c62e79fe69','',1),('0xc61b9bb3a7a0767e3179713f3a5c7a9aedce193c','',1),('0xca582d9655a50e6512045740deb0de3a7ee5281f','',1),('0xca8fa8f0b631ecdb18cda619c4fc9d197c8affca','',1),('0xd05e6bf1a00b5b4c9df909309f19e29af792422b','',1),('0xd44023d2710dd7bef797a074ecec4fc74fdd52b2','',1),('0xd4fcc07a8da7d55599167991d4ab47f976d0a306','',1),('0xd65bd7f995bcc3bdb2ea2f8ff7554a61d1bf6e53','',1),('0xdc76cd25977e0a5ae17155770273ad58648900d3','Huobi 6',0),('0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae','EthDev',0),('0xe04cf52e9fafa3d9bf14c407afff94165ef835f7','',1),('0xe0f5b79ef9f748562a21d017bb7a6706954b7585','',1),('0xe35b0ef92452c353dbb93775e0df97cedf873c72','',1),('0xe853c56864a2ebe4576a807d26fdc4a0ada51919','Kraken 3',0),('0xe92d1a43df510f82c66382592a047d288f85226f','',1),('0xe9778e69a961e64d3cdbb34cf6778281d34667c2','NuCypher: WorkLock',0),('0xe9fb0895312d39da56c173f1486b1ce934b4004a','',1),('0xeb2b00042ce4522ce2d1aacee6f312d26c4eb9d6','',1),('0xf274483d5bb6e2522afea3949728f870ba32bb9c','',1),('0xf66852bc122fd40bfecc63cd48217e88bda12109','',1),('0xf977814e90da44bfa03b6295a0616a897441acec','Binance 8',0),('0xfc39f0dc7a1c5d5cd1cdf3b460d5fa99a56abf65','',1),('0xfd61352232157815cf7b71045557192bf0ce1884','Nexus Mutual: Pool',0),('0xfd898a0f677e97a9031654fc79a27cb5e31da34a','',1),('0xfe01a216234f79cfc3bea7513e457c6a9e50250d','',1);
/*!40000 ALTER TABLE `iswhale` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-20 15:16:56
