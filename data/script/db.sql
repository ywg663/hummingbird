/*
	title: tradingAssistant
	author: yang
	date: 2020/10/30

*/
-- ta.account definition

CREATE TABLE `account` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'id',
  `serial` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '业务id',
  `create_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建日期',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日期',
  `status` tinyint unsigned DEFAULT NULL COMMENT '状态',
  `type` tinyint unsigned DEFAULT NULL COMMENT '类别',
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '名称',
  `pwd` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '值',
  `amount` float DEFAULT NULL COMMENT '金额',
  PRIMARY KEY (`id`),
  KEY `idx_create_datetime` (`create_datetime`),
  KEY `idx_time` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='帐号';

-- ta.indicator_day definition

CREATE TABLE `indicator_day` (
  `security` varchar(20) COLLATE utf8mb4_bin NOT NULL COMMENT '股票代码',
  `kday` date NOT NULL COMMENT '日期',
  `open` decimal(10,2) DEFAULT NULL COMMENT '时间段开始时价格',
  `close` decimal(10,2) DEFAULT NULL COMMENT '时间段结束时价格',
  `low` decimal(10,2) DEFAULT NULL COMMENT '最低价',
  `high` decimal(10,2) DEFAULT NULL COMMENT '最高价',
  `volume` bigint DEFAULT NULL COMMENT '成交的股票数量',
  `money` decimal(20,2) DEFAULT NULL COMMENT '成交的金额',
  `high_limit` decimal(10,2) DEFAULT NULL COMMENT '涨停价',
  `low_limit` decimal(10,2) DEFAULT NULL COMMENT '跌停价',
  `avg` decimal(10,2) DEFAULT NULL COMMENT '这段时间的平均价, 等于money/volume',
  `ma20` decimal(10,2) DEFAULT NULL COMMENT '20均线值',
  `ma60` decimal(10,2) DEFAULT NULL COMMENT '60均线值',
  `ma120` decimal(10,2) DEFAULT NULL COMMENT '120均线',
  `roc` decimal(10,2) DEFAULT NULL COMMENT 'roc',
  `sroc` decimal(10,2) DEFAULT NULL COMMENT '涨停价',
  `kd20` decimal(10,2) DEFAULT NULL COMMENT '20抵扣close',
  `kd60` decimal(10,2) DEFAULT NULL COMMENT 'close与ema60差比值',
  `kd120` decimal(10,2) DEFAULT NULL COMMENT 'close与ema20差比值',
  `cs` decimal(10,2) DEFAULT NULL COMMENT 'close与ema20差比值',
  `sm` decimal(10,2) DEFAULT NULL COMMENT 'ema20与ema60差比值',
  `ml` decimal(10,2) DEFAULT NULL COMMENT 'ema60与ema120差比值',
  `change_pct` decimal(10,2) DEFAULT NULL COMMENT '涨跌幅',
  `day_pct` decimal(10,2) DEFAULT NULL COMMENT '单日振幅',
  `rel20` decimal(10,2) DEFAULT NULL COMMENT '相对中证800强度',
  `update_date` int DEFAULT NULL,
  `status` int NOT NULL DEFAULT '0',
  `i_pct20` decimal(10,2) DEFAULT NULL COMMENT '中证800涨跌20均值',
  `money20` decimal(20,2) DEFAULT NULL COMMENT '20天成交量均值',
  `change_pct20` decimal(10,2) DEFAULT NULL COMMENT '涨跌20均值',
  `kst` decimal(10,2) DEFAULT NULL COMMENT 'KST',
  `sig` decimal(10,2) DEFAULT NULL COMMENT 'KST.SIG',
  `security_type` int DEFAULT '0',
  PRIMARY KEY (`security`,`kday`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='指标日线行情';

-- ta.industries definition

CREATE TABLE `industries` (
  `type` varchar(20) COLLATE utf8mb4_bin NOT NULL COMMENT '行情分法，申万，证监会，聚宽',
  `index` varchar(20) COLLATE utf8mb4_bin NOT NULL COMMENT '行情代码',
  `name` varchar(20) COLLATE utf8mb4_bin NOT NULL COMMENT '行情名称',
  `start_date` date NOT NULL COMMENT '开始的日期',
  `update_date` date DEFAULT NULL,
  `status` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`index`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='行业基础数据';

-- ta.kline_day definition

CREATE TABLE `kline_day` (
  `security` varchar(20) COLLATE utf8mb4_bin NOT NULL COMMENT '股票代码',
  `kday` date NOT NULL COMMENT '日期',
  `open` decimal(10,2) DEFAULT NULL COMMENT '时间段开始时价格',
  `close` decimal(10,2) DEFAULT NULL COMMENT '时间段结束时价格',
  `low` decimal(10,2) DEFAULT NULL COMMENT '最低价',
  `high` decimal(10,2) DEFAULT NULL COMMENT '最高价',
  `volume` bigint DEFAULT NULL COMMENT '成交的股票数量',
  `money` decimal(20,2) DEFAULT NULL COMMENT '成交的金额',
  `factor` decimal(15,8) DEFAULT NULL COMMENT '前复权因子, 我们提供的价格都是前复权后的, 但是利用这个值可以算出原始价格, 方法是价格除以factor, 比如: close/factor',
  `high_limit` decimal(10,2) DEFAULT NULL COMMENT '涨停价',
  `low_limit` decimal(10,2) DEFAULT NULL COMMENT '跌停价',
  `avg` decimal(10,2) DEFAULT NULL COMMENT '这段时间的平均价, 等于money/volume',
  `pre_close` decimal(10,2) DEFAULT NULL COMMENT '前一个单位时间结束时的价格, 按天则是前一天的收盘价, 按分钟这是前一分钟的结束价格',
  `paused` tinyint DEFAULT NULL COMMENT '布尔值, 这只股票是否停牌, 停牌时open/close/low/high/pre_close依然有值,都等于停牌前的收盘价, volume=money=0',
  `update_date` date DEFAULT NULL,
  `status` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`security`,`kday`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='日线行情数据';

-- ta.securities definition

CREATE TABLE `securities` (
  `security` varchar(20) COLLATE utf8mb4_bin NOT NULL COMMENT '股票代码',
  `display_name` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '中文名称',
  `name` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '缩写简称',
  `start_date` date DEFAULT NULL COMMENT '上市日期',
  `end_date` date DEFAULT NULL COMMENT '退市日期，如果没有退市则为2200-01-01',
  `type` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '类型，股票，指数，基金\r\nstock，fund, index futures，options, etf, ''lof'', ''fja'', ''fjb'', ''open_fund'', ''bond_fund'', ''stock_fund'', ''QDII_fund'', ''money_market_fund',
  `update_date` date DEFAULT NULL,
  `status` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`security`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='所有股票信息';

-- ta.setting definition

CREATE TABLE `setting` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'id',
  `serial` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '业务id',
  `create_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建日期',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日期',
  `status` tinyint unsigned DEFAULT NULL COMMENT '状态',
  `type` tinyint unsigned DEFAULT NULL COMMENT '类别',
  `name` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '名称',
  `value` varchar(512) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '值',
  PRIMARY KEY (`id`),
  KEY `idx_create_datetime` (`create_datetime`),
  KEY `idx_time` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='设置';

-- ta.sw1_daily_price definition

CREATE TABLE `sw1_daily_price` (
  `date` date NOT NULL COMMENT '日期',
  `code` varchar(20) COLLATE utf8mb4_bin NOT NULL COMMENT '指数编码',
  `name` varchar(20) COLLATE utf8mb4_bin NOT NULL COMMENT '指数名称',
  `open` decimal(10,2) DEFAULT NULL COMMENT '时间段开始时价格',
  `close` decimal(10,2) DEFAULT NULL COMMENT '时间段结束时价格',
  `low` decimal(10,2) DEFAULT NULL COMMENT '最低价',
  `high` decimal(10,2) DEFAULT NULL COMMENT '最高价',
  `volume` bigint DEFAULT NULL COMMENT '成交的股票数量',
  `money` decimal(20,2) DEFAULT NULL COMMENT '成交的金额',
  `change_pct` decimal(10,4) DEFAULT NULL COMMENT '涨跌幅',
  `id` int NOT NULL,
  `update_date` date DEFAULT NULL,
  `status` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`code`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='申万一级行业日线行情数据';
