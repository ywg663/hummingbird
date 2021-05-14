/*
	title: tradingAssistant
	author: yang
	date: 2020/10/30

*/
CREATE TABLE `setting` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT comment 'id' ,
  `serial` varchar(32) comment '业务id',
  `create_datetime` timestamp default CURRENT_TIMESTAMP not null comment '创建日期' ,
  `update_time` timestamp default CURRENT_TIMESTAMP not null comment '更新日期' ,
  `status` tinyint unsigned null comment '状态',
  `type` tinyint unsigned null comment '类别',
  `name` nvarchar(32) null comment '名称',
  `value` nvarchar(512) null comment '值',

  PRIMARY KEY (`id`),
  KEY `idx_create_datetime` (`create_datetime`),
  KEY `idx_time` (`name`)
) comment '设置' collate=utf8mb4_bin;

-- 帐号 
CREATE TABLE `account` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT comment 'id' ,
  `serial` varchar(32) comment '业务id',
  `create_datetime` timestamp default CURRENT_TIMESTAMP not null comment '创建日期' ,
  `update_time` timestamp default CURRENT_TIMESTAMP not null comment '更新日期' ,
  `status` tinyint unsigned null comment '状态',
  `type` tinyint unsigned null comment '类别',
  `name` nvarchar(32) null comment '名称',
  `pwd` nvarchar(32) null comment '值',
  `amount` FLOAT(4) null comment '金额',

  PRIMARY KEY (`id`),   
  KEY `idx_create_datetime` (`create_datetime`),
  KEY `idx_time` (`name`)
) comment '设置' collate=utf8mb4_bin;


CREATE TABLE `securities` (
  `security` VARCHAR(20) NOT NULL COMMENT '股票代码',
  `display_name` VARCHAR(20) NULL COMMENT '中文名称',
  `name` VARCHAR(50) NULL COMMENT '缩写简称',
  `start_date` DATE NULL COMMENT ' 上市日期',
  `end_date` DATE NULL COMMENT '退市日期，如果没有退市则为2200-01-01',
  PRIMARY KEY (`security`)
  )COMMENT = '所有股票信息' collate=utf8mb4_bin;

-- 日线行情数据：*ST猴王
-- 索引 股票代码，日期
CREATE TABLE `kline_day` (
  `security` VARCHAR(20) NOT NULL COMMENT '股票代码',
  `kday` DATE NOT NULL COMMENT '日期',
  `open` DECIMAL(10,2) NULL COMMENT '时间段开始时价格',
  `close` DECIMAL(10,2) NULL COMMENT '时间段结束时价格',
  `low` DECIMAL(10,2) NULL COMMENT '最低价',
  `high` DECIMAL(10,2) NULL COMMENT '最高价',
  `volume` BIGINT NULL COMMENT '成交的股票数量',
  `money` DECIMAL(20,2) NULL COMMENT '成交的金额',
  `factor` DECIMAL(15,8) NULL COMMENT '前复权因子, 我们提供的价格都是前复权后的, 但是利用这个值可以算出原始价格, 方法是价格除以factor, 比如: close/factor',
  `high_limit` DECIMAL(10,2) NULL COMMENT '涨停价',
  `low_limit` DECIMAL(10,2) NULL COMMENT '跌停价',
  `avg` DECIMAL(10,2) NULL COMMENT '这段时间的平均价, 等于money/volume',
  `pre_close` DECIMAL(10,2) NULL COMMENT '前一个单位时间结束时的价格, 按天则是前一天的收盘价, 按分钟这是前一分钟的结束价格',
  `paused` TINYINT NULL COMMENT '布尔值, 这只股票是否停牌, 停牌时open/close/low/high/pre_close依然有值,都等于停牌前的收盘价, volume=money=0',
  PRIMARY KEY (`security`, `kday`)
  )COMMENT = '日线行情数据' collate=utf8mb4_bin;
  
 -- 指标
CREATE TABLE `indicator_day` (
  `security` VARCHAR(20) NOT NULL COMMENT '股票代码',
  `kday` DATE NOT NULL COMMENT '日期',
  `open` DECIMAL(10,2) NULL COMMENT '时间段开始时价格',
  `close` DECIMAL(10,2) NULL COMMENT '时间段结束时价格',
  `low` DECIMAL(10,2) NULL COMMENT '最低价',
  `high` DECIMAL(10,2) NULL COMMENT '最高价',
  `volume` BIGINT NULL COMMENT '成交的股票数量',
  `money` DECIMAL(20,2) NULL COMMENT '成交的金额',
  `high_limit` DECIMAL(10,2) NULL COMMENT '涨停价',
  `low_limit` DECIMAL(10,2) NULL COMMENT '跌停价',
  `avg` DECIMAL(10,2) NULL COMMENT '这段时间的平均价, 等于money/volume',
  `ma20` DECIMAL(10,2) NULL COMMENT '20均线值',
  `ma60` DECIMAL(10,2) NULL COMMENT '60均线值',
  `ma120` DECIMAL(10,2) NULL COMMENT '120均线',
  `roc` DECIMAL(10,2) NULL COMMENT 'roc',
  `sroc` DECIMAL(10,2) NULL COMMENT '涨停价',
  `kd20` DECIMAL(10,2) NULL COMMENT '20抵扣close',
  `kd60` DECIMAL(10,2) NULL COMMENT 'close与ema60差比值',
  `kd120` DECIMAL(10,2) NULL COMMENT 'close与ema20差比值',
  `cs` DECIMAL(10,2) NULL COMMENT 'close与ema20差比值',
  `sm` DECIMAL(10,2) NULL COMMENT 'ema20与ema60差比值',
  `ml` DECIMAL(10,2) NULL COMMENT 'ema60与ema120差比值',
  `change_pct` DECIMAL(10,2) NULL COMMENT '涨跌幅',
  `day_pct` DECIMAL(10,2) NULL COMMENT '单日振幅',
  `rel20` DECIMAL(10,2) NULL COMMENT '相对中证800强度',
  PRIMARY KEY (`security`, `kday`)
  )COMMENT = '指标日线行情' collate=utf8mb4_bin;
 

-- 申万一级行业日线行情数据
-- 索引 股票代码，日期
CREATE TABLE `sw1_daily_price` (
  `date` DATE NOT NULL COMMENT '日期',
  `code` VARCHAR(20) NOT NULL COMMENT '指数编码',
  `name` varchar(20) NOT NULL COMMENT '指数名称',
  `open` DECIMAL(10,2) NULL COMMENT '时间段开始时价格',
  `close` DECIMAL(10,2) NULL COMMENT '时间段结束时价格',
  `low` DECIMAL(10,2) NULL COMMENT '最低价',
  `high` DECIMAL(10,2) NULL COMMENT '最高价',
  `volume` BIGINT NULL COMMENT '成交的股票数量',
  `money` DECIMAL(20,2) NULL COMMENT '成交的金额',
  `change_pct` DECIMAL(10,4) NULL COMMENT '涨跌幅',
  PRIMARY KEY (`code`, `date`)
  )COMMENT = '申万一级行业日线行情数据' collate=utf8mb4_bin;
 -- truncate table `kline_day` 
 select * from sw1_daily_price where code = '801220' order by `date` desc 
 
 -- 市值数据-股票代码模
 CREATE TABLE `valuation` (
  `code` VARCHAR(20) NOT NULL COMMENT '股票代码  带后缀.XSHE/.XSHG',
  `day` DATE NOT NULL COMMENT '取数据的日期',
  `capitalization` DECIMAL(20,4) NULL COMMENT '总股本(万股)     公司已发行的普通股股份总数(包含A股，B股和H股的总股本)',
  `circulating_cap` DECIMAL(20,4) NULL COMMENT '流通股本(万股)     公司已发行的境内上市流通、以人民币兑换的股份总数(A股市场的流通股本)',
  `market_cap` DECIMAL(20,10) NULL COMMENT '总市值(亿元)     A股收盘价*已发行股票总股本（A股+B股+H股）',
  `circulating_market_cap` DECIMAL(20,10) NULL COMMENT '流通市值(亿元)     流通市值指在某特定时间内当时可交易的流通股股数乘以当时股价得出的流通股票总价值。     A股市场的收盘价*A股市场的流通股数',
  `turnover_ratio` DECIMAL(10,4) NULL COMMENT '换手率(%)     指在一定时间内市场中股票转手买卖的频率，是反映股票流通性强弱的指标之一。     换手率=[指定交易日成交量(手)100/截至该日股票的自由流通股本(股)]100%',
  `pe_ratio` DECIMAL(15,4) NULL COMMENT '市盈率(PE, TTM)     每股市价为每股收益的倍数，反映投资人对每元净利润所愿支付的价格，用来估计股票的投资报酬和风险     市盈率（PE，TTM）=（股票在指定交易日期的收盘价 * 当日人民币外汇挂牌价 * 截止当日公司总股本）/归属于母公司股东的净利润TTM。',
  `pe_ratio_lyr` DECIMAL(15,4) NULL COMMENT '以上一年度每股盈利计算的静态市盈率. 股价/最近年度报告EPS     市盈率（PE）=（股票在指定交易日期的收盘价 * 当日人民币外汇牌价 * 截至当日公司总股本）/归属母公司股东的净利润。',
  `pb_ratio` DECIMAL(15,4) NULL COMMENT '市净率(PB)     每股股价与每股净资产的比率     市净率=（股票在指定交易日期的收盘价 * 当日人民币外汇牌价 * 截至当日公司总股本）/归属母公司股东的权益。',
  `ps_ratio` DECIMAL(15,4) NULL COMMENT '市销率(PS, TTM)     市销率为股票价格与每股销售收入之比，市销率越小，通常被认为投资价值越高。     市销率TTM=（股票在指定交易日期的收盘价 * 当日人民币外汇牌价 * 截至当日公司总股本）/营业总收入TTM',
  `pcf_ratio` DECIMAL(15,4) NULL COMMENT '市现率(PCF, 现金净流量TTM)     每股市价为每股现金净流量的倍数     市现率=（股票在指定交易日期的收盘价 * 当日人民币外汇牌价 * 截至当日公司总股本）/现金及现金等价物净增加额TTM',
  PRIMARY KEY (`code`, `day`)
  )COMMENT = '市值数据' collate=utf8mb4_bin;
  
  -- 行业信息
  /**
   * type
	"sw_l1": 申万一级行业
	"sw_l2": 申万二级行业
	"sw_l3": 申万三级行业
	"jq_l1": 聚宽一级行业
	"jq_l2": 聚宽二级行业
	"zjw": 证监会行业
  **/
 CREATE TABLE `industries` (
  `type` VARCHAR(20) not null COMMENT '行情分法，申万，证监会，聚宽',
  `index` VARCHAR(20) NOT NULL COMMENT '行情代码',
  `name`  VARCHAR(20) NOT NULL COMMENT '行情名称',
  `start` DATE NOT NULL COMMENT '开始的日期',
  PRIMARY KEY (`index`, `type`)
  )COMMENT = '行业基础数据' collate=utf8mb4_bin;
  
 select * from industries i2 where i2.`type` = 'sw_l1'
 select id.* from indicator_day id limit 0,10 left join securities s2 on id.`security` = s2.`security` where id.`security` = '000906.XSHG' order by id.kday 
	where id.sroc between -1 and 1 and id.ma20 > id.ma60 and id.ma60 > id.ma120 
	order by id.sroc desc limit 0,20
 select distinct id.`security` from indicator_day id where id.ml > 0 and id.ml < 4 and abs(id.cs) < 5 and abs(id.sm) <5
	order by id.sroc desc limit 0,20
select distinct security_type from indicator_day id limit 0,10 
select count(*) from indicator_day id2 where id2.rel20 is null 
delete from indicator_day where rel20 is null
ALTER TABLE securities add dc_code varchar(16) null comment '东财代码'
 alter table indicator_day add change_pct20  DECIMAL(10,2) null COMMENT '涨跌20均值';
 alter table indicator_day add i_pct20  DECIMAL(10,2) null COMMENT '中证800涨跌20均值';
 alter table indicator_day add money20  DECIMAL(10,2) null COMMENT '20天成交量均值';
SELECT * FROM ta.kline_day where security = '000906.XSHG' order by kday desc limit 1
SELECT * FROM ta.kline_day where paused  = 1 and `security`= '515620.XSHG' order by kday desc 
select * from setting s2 
update setting set value = '["300737.XSHE","601888.XSHG","300003.XSHE","600989.XSHG","600873.XSHG","603501.XSHG","603916.XSHG","600436.XSHG","000157.XSHE"]' where id = 4
INSERT INTO ta.setting
(serial, create_datetime, update_time, status, `type`, name, value)
VALUES('', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0, 0, 'holds', '["300737.XSHE","601888.XSHG","300003.XSHE","600989.XSHG","600873.XSHG","603501.XSHG","603916.XSHG","600436.XSHG","000157.XSHE"]');

-- delete from kline_day where `security` = ''
-- delete from indicator_day where `security` = ''
select COUNT(*) from securities where type ='stock' and status = 1 and end_date < NOW()  `security` = '000768.XSHE'
delete from securities where update_date > '2021-04-03'
update securities set status = 1 where end_date > NOW()  and type = 'etf'
select * from indicator_day where `security` = '000799.XSHE' order by kday desc limit 0,10
-- 1904797550.67
 select count(*) from securities s where s.status = 1 and `type` = 'stock'
 
 select * from securities s3 order by update_date desc limit 0,10
 select * FROM securities s3 where s3.`security` = '300573.XSHE'
  select count(*) from securities s 
 	where s.end_date < now() or locate('ST',s.display_name) or timestampdiff(year,s.start_date,now()) < 1 and s.type='stock' and s.status = 1
update securities set status = 0 where (end_date < now() or locate('ST',display_name) or timestampdiff(year,start_date,now()) < 1) and type='stock' and status = 1
select * from securities s where s.`type` = 'etf'
  where (s.end_date < now() or locate('ST',s.display_name) or timestampdiff(year,s.start_date,now()) < 1) and s.type='stock' and s.status = 1
 select count(*) from securities s2 where s2.status  = 1 and s2.type = 'index'
 update securities set status = 0 where start_date > '2021-04-13'
 
 select * from setting s3 
 select * from kline_day kd4 where kd4.`security` = '300725.XSHE'
 select count(*) from securities s8 where s8.status = 1
 delete from kline_day kd3 where kd3.`close` is null or kd3.`security` in (select security from securities s7 where s7.start_date > '2020-9-16')
 select * from indicator_day id2 where id2.`security` = '300725.XSHE'
 select * from kline_day kd left join securities s6 on kd.`security` = s6.`security` where s6.status = 1 and s6.`type` = 'etf'
select k.*  from kline_day k left join securities s3 on  k.`security` = s3.`security` where s3.type = 'etf' order by kday desc limit 0,10
delete from  kline_day where `security` in (select `security` from securities s5 where s5.status = 0 and type = 'stock')
select * from  indicator_day order by kday desc limit 0,10 where `security`  in (select `security` from securities s5 where s5.status = 0 and type = 'stock')
select * from sw1_daily_price sdp order by sdp.`date` desc limit 0,10
select count(s2.display_name) from securities s2 where not (s2.end_date < now() or locate('ST',s2.display_name)) and timestampdiff(year,s2.start_date,now()) > 1 order by s2.start_date desc limit 0,100

