/*
	title: tradingAssistant
	author: yang
	date: 2020/10/30

*/
CREATE TABLE `setting` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT comment 'id' ,
  `serial` varchar(32) comment 'ҵ��id',
  `create_datetime` timestamp default CURRENT_TIMESTAMP not null comment '��������' ,
  `update_time` timestamp default CURRENT_TIMESTAMP not null comment '��������' ,
  `status` tinyint unsigned null comment '״̬',
  `type` tinyint unsigned null comment '���',
  `name` nvarchar(32) null comment '����',
  `value` nvarchar(512) null comment 'ֵ',

  PRIMARY KEY (`id`),
  KEY `idx_create_datetime` (`create_datetime`),
  KEY `idx_time` (`name`)
) comment '����' collate=utf8mb4_bin;

-- �ʺ� 
CREATE TABLE `account` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT comment 'id' ,
  `serial` varchar(32) comment 'ҵ��id',
  `create_datetime` timestamp default CURRENT_TIMESTAMP not null comment '��������' ,
  `update_time` timestamp default CURRENT_TIMESTAMP not null comment '��������' ,
  `status` tinyint unsigned null comment '״̬',
  `type` tinyint unsigned null comment '���',
  `name` nvarchar(32) null comment '����',
  `pwd` nvarchar(32) null comment 'ֵ',
  `amount` FLOAT(4) null comment '���',

  PRIMARY KEY (`id`),   
  KEY `idx_create_datetime` (`create_datetime`),
  KEY `idx_time` (`name`)
) comment '����' collate=utf8mb4_bin;


CREATE TABLE `securities` (
  `security` VARCHAR(20) NOT NULL COMMENT '��Ʊ����',
  `display_name` VARCHAR(20) NULL COMMENT '��������',
  `name` VARCHAR(50) NULL COMMENT '��д���',
  `start_date` DATE NULL COMMENT ' ��������',
  `end_date` DATE NULL COMMENT '�������ڣ����û��������Ϊ2200-01-01',
  PRIMARY KEY (`security`)
  )COMMENT = '���й�Ʊ��Ϣ' collate=utf8mb4_bin;

-- �����������ݣ�*ST����
-- ���� ��Ʊ���룬����
CREATE TABLE `kline_day` (
  `security` VARCHAR(20) NOT NULL COMMENT '��Ʊ����',
  `kday` DATE NOT NULL COMMENT '����',
  `open` DECIMAL(10,2) NULL COMMENT 'ʱ��ο�ʼʱ�۸�',
  `close` DECIMAL(10,2) NULL COMMENT 'ʱ��ν���ʱ�۸�',
  `low` DECIMAL(10,2) NULL COMMENT '��ͼ�',
  `high` DECIMAL(10,2) NULL COMMENT '��߼�',
  `volume` BIGINT NULL COMMENT '�ɽ��Ĺ�Ʊ����',
  `money` DECIMAL(20,2) NULL COMMENT '�ɽ��Ľ��',
  `factor` DECIMAL(15,8) NULL COMMENT 'ǰ��Ȩ����, �����ṩ�ļ۸���ǰ��Ȩ���, �����������ֵ�������ԭʼ�۸�, �����Ǽ۸����factor, ����: close/factor',
  `high_limit` DECIMAL(10,2) NULL COMMENT '��ͣ��',
  `low_limit` DECIMAL(10,2) NULL COMMENT '��ͣ��',
  `avg` DECIMAL(10,2) NULL COMMENT '���ʱ���ƽ����, ����money/volume',
  `pre_close` DECIMAL(10,2) NULL COMMENT 'ǰһ����λʱ�����ʱ�ļ۸�, ��������ǰһ������̼�, ����������ǰһ���ӵĽ����۸�',
  `paused` TINYINT NULL COMMENT '����ֵ, ��ֻ��Ʊ�Ƿ�ͣ��, ͣ��ʱopen/close/low/high/pre_close��Ȼ��ֵ,������ͣ��ǰ�����̼�, volume=money=0',
  PRIMARY KEY (`security`, `kday`)
  )COMMENT = '������������' collate=utf8mb4_bin;
  
 -- ָ��
CREATE TABLE `indicator_day` (
  `security` VARCHAR(20) NOT NULL COMMENT '��Ʊ����',
  `kday` DATE NOT NULL COMMENT '����',
  `open` DECIMAL(10,2) NULL COMMENT 'ʱ��ο�ʼʱ�۸�',
  `close` DECIMAL(10,2) NULL COMMENT 'ʱ��ν���ʱ�۸�',
  `low` DECIMAL(10,2) NULL COMMENT '��ͼ�',
  `high` DECIMAL(10,2) NULL COMMENT '��߼�',
  `volume` BIGINT NULL COMMENT '�ɽ��Ĺ�Ʊ����',
  `money` DECIMAL(20,2) NULL COMMENT '�ɽ��Ľ��',
  `high_limit` DECIMAL(10,2) NULL COMMENT '��ͣ��',
  `low_limit` DECIMAL(10,2) NULL COMMENT '��ͣ��',
  `avg` DECIMAL(10,2) NULL COMMENT '���ʱ���ƽ����, ����money/volume',
  `ma20` DECIMAL(10,2) NULL COMMENT '20����ֵ',
  `ma60` DECIMAL(10,2) NULL COMMENT '60����ֵ',
  `ma120` DECIMAL(10,2) NULL COMMENT '120����',
  `roc` DECIMAL(10,2) NULL COMMENT 'roc',
  `sroc` DECIMAL(10,2) NULL COMMENT '��ͣ��',
  `kd20` DECIMAL(10,2) NULL COMMENT '20�ֿ�close',
  `kd60` DECIMAL(10,2) NULL COMMENT 'close��ema60���ֵ',
  `kd120` DECIMAL(10,2) NULL COMMENT 'close��ema20���ֵ',
  `cs` DECIMAL(10,2) NULL COMMENT 'close��ema20���ֵ',
  `sm` DECIMAL(10,2) NULL COMMENT 'ema20��ema60���ֵ',
  `ml` DECIMAL(10,2) NULL COMMENT 'ema60��ema120���ֵ',
  `change_pct` DECIMAL(10,2) NULL COMMENT '�ǵ���',
  `day_pct` DECIMAL(10,2) NULL COMMENT '�������',
  `rel20` DECIMAL(10,2) NULL COMMENT '�����֤800ǿ��',
  PRIMARY KEY (`security`, `kday`)
  )COMMENT = 'ָ����������' collate=utf8mb4_bin;
 

-- ����һ����ҵ������������
-- ���� ��Ʊ���룬����
CREATE TABLE `sw1_daily_price` (
  `date` DATE NOT NULL COMMENT '����',
  `code` VARCHAR(20) NOT NULL COMMENT 'ָ������',
  `name` varchar(20) NOT NULL COMMENT 'ָ������',
  `open` DECIMAL(10,2) NULL COMMENT 'ʱ��ο�ʼʱ�۸�',
  `close` DECIMAL(10,2) NULL COMMENT 'ʱ��ν���ʱ�۸�',
  `low` DECIMAL(10,2) NULL COMMENT '��ͼ�',
  `high` DECIMAL(10,2) NULL COMMENT '��߼�',
  `volume` BIGINT NULL COMMENT '�ɽ��Ĺ�Ʊ����',
  `money` DECIMAL(20,2) NULL COMMENT '�ɽ��Ľ��',
  `change_pct` DECIMAL(10,4) NULL COMMENT '�ǵ���',
  PRIMARY KEY (`code`, `date`)
  )COMMENT = '����һ����ҵ������������' collate=utf8mb4_bin;
 -- truncate table `kline_day` 
 select * from sw1_daily_price where code = '801220' order by `date` desc 
 
 -- ��ֵ����-��Ʊ����ģ
 CREATE TABLE `valuation` (
  `code` VARCHAR(20) NOT NULL COMMENT '��Ʊ����  ����׺.XSHE/.XSHG',
  `day` DATE NOT NULL COMMENT 'ȡ���ݵ�����',
  `capitalization` DECIMAL(20,4) NULL COMMENT '�ܹɱ�(���)     ��˾�ѷ��е���ͨ�ɹɷ�����(����A�ɣ�B�ɺ�H�ɵ��ܹɱ�)',
  `circulating_cap` DECIMAL(20,4) NULL COMMENT '��ͨ�ɱ�(���)     ��˾�ѷ��еľ���������ͨ��������Ҷһ��Ĺɷ�����(A���г�����ͨ�ɱ�)',
  `market_cap` DECIMAL(20,10) NULL COMMENT '����ֵ(��Ԫ)     A�����̼�*�ѷ��й�Ʊ�ܹɱ���A��+B��+H�ɣ�',
  `circulating_market_cap` DECIMAL(20,10) NULL COMMENT '��ͨ��ֵ(��Ԫ)     ��ͨ��ֵָ��ĳ�ض�ʱ���ڵ�ʱ�ɽ��׵���ͨ�ɹ������Ե�ʱ�ɼ۵ó�����ͨ��Ʊ�ܼ�ֵ��     A���г������̼�*A���г�����ͨ����',
  `turnover_ratio` DECIMAL(10,4) NULL COMMENT '������(%)     ָ��һ��ʱ�����г��й�Ʊת��������Ƶ�ʣ��Ƿ�ӳ��Ʊ��ͨ��ǿ����ָ��֮һ��     ������=[ָ�������ճɽ���(��)100/�������չ�Ʊ��������ͨ�ɱ�(��)]100%',
  `pe_ratio` DECIMAL(15,4) NULL COMMENT '��ӯ��(PE, TTM)     ÿ���м�Ϊÿ������ı�������ӳͶ���˶�ÿԪ��������Ը֧���ļ۸��������ƹ�Ʊ��Ͷ�ʱ���ͷ���     ��ӯ�ʣ�PE��TTM��=����Ʊ��ָ���������ڵ����̼� * ��������������Ƽ� * ��ֹ���չ�˾�ܹɱ���/������ĸ��˾�ɶ��ľ�����TTM��',
  `pe_ratio_lyr` DECIMAL(15,4) NULL COMMENT '����һ���ÿ��ӯ������ľ�̬��ӯ��. �ɼ�/�����ȱ���EPS     ��ӯ�ʣ�PE��=����Ʊ��ָ���������ڵ����̼� * �������������Ƽ� * �������չ�˾�ܹɱ���/����ĸ��˾�ɶ��ľ�����',
  `pb_ratio` DECIMAL(15,4) NULL COMMENT '�о���(PB)     ÿ�ɹɼ���ÿ�ɾ��ʲ��ı���     �о���=����Ʊ��ָ���������ڵ����̼� * �������������Ƽ� * �������չ�˾�ܹɱ���/����ĸ��˾�ɶ���Ȩ�档',
  `ps_ratio` DECIMAL(15,4) NULL COMMENT '������(PS, TTM)     ������Ϊ��Ʊ�۸���ÿ����������֮�ȣ�������ԽС��ͨ������ΪͶ�ʼ�ֵԽ�ߡ�     ������TTM=����Ʊ��ָ���������ڵ����̼� * �������������Ƽ� * �������չ�˾�ܹɱ���/Ӫҵ������TTM',
  `pcf_ratio` DECIMAL(15,4) NULL COMMENT '������(PCF, �ֽ�����TTM)     ÿ���м�Ϊÿ���ֽ������ı���     ������=����Ʊ��ָ���������ڵ����̼� * �������������Ƽ� * �������չ�˾�ܹɱ���/�ֽ��ֽ�ȼ��ﾻ���Ӷ�TTM',
  PRIMARY KEY (`code`, `day`)
  )COMMENT = '��ֵ����' collate=utf8mb4_bin;
  
  -- ��ҵ��Ϣ
  /**
   * type
	"sw_l1": ����һ����ҵ
	"sw_l2": ���������ҵ
	"sw_l3": ����������ҵ
	"jq_l1": �ۿ�һ����ҵ
	"jq_l2": �ۿ������ҵ
	"zjw": ֤�����ҵ
  **/
 CREATE TABLE `industries` (
  `type` VARCHAR(20) not null COMMENT '����ַ�������֤��ᣬ�ۿ�',
  `index` VARCHAR(20) NOT NULL COMMENT '�������',
  `name`  VARCHAR(20) NOT NULL COMMENT '��������',
  `start` DATE NOT NULL COMMENT '��ʼ������',
  PRIMARY KEY (`index`, `type`)
  )COMMENT = '��ҵ��������' collate=utf8mb4_bin;
  
 select * from industries i2 where i2.`type` = 'sw_l1'
 select id.* from indicator_day id limit 0,10 left join securities s2 on id.`security` = s2.`security` where id.`security` = '000906.XSHG' order by id.kday 
	where id.sroc between -1 and 1 and id.ma20 > id.ma60 and id.ma60 > id.ma120 
	order by id.sroc desc limit 0,20
 select distinct id.`security` from indicator_day id where id.ml > 0 and id.ml < 4 and abs(id.cs) < 5 and abs(id.sm) <5
	order by id.sroc desc limit 0,20
select distinct security_type from indicator_day id limit 0,10 
select count(*) from indicator_day id2 where id2.rel20 is null 
delete from indicator_day where rel20 is null
ALTER TABLE securities add dc_code varchar(16) null comment '���ƴ���'
 alter table indicator_day add change_pct20  DECIMAL(10,2) null COMMENT '�ǵ�20��ֵ';
 alter table indicator_day add i_pct20  DECIMAL(10,2) null COMMENT '��֤800�ǵ�20��ֵ';
 alter table indicator_day add money20  DECIMAL(10,2) null COMMENT '20��ɽ�����ֵ';
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

