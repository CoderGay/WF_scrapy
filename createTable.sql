 CREATE TABLE paper(
	`paper_id` int not null AUTO_INCREMENT,
    `DOI` varchar(255),
    `title` varchar(128)  comment '标题',
    `title_en` varchar(128)  comment '书名',
	`abstract` text  comment '摘要',
    `abstract_en` text comment '英文摘要',
    `latest_update_time` varchar(128) comment '最新更新时间',
	`pages` int comment '页数',
     `paper_url` varchar(255),
	primary key (`paper_id`)
) comment '论文信息表' ;

CREATE TABLE author (
	`author_id` int not null AUTO_INCREMENT,
    `name` varchar(255) not null comment '姓名',
    `name_en` varchar(255) default null comment '英文名',
    `affiliation_id` int comment '发表单位id',
	primary key (`author_id`)
) comment '作者信息表' ;

CREATE TABLE author_rs (
	`aurs_id` int not null AUTO_INCREMENT,
    `author_id` int not null,
    `paper_id` int not null,
	primary key (`aurs_id`)
) comment '作者记录表author_relationship' ;

CREATE TABLE affiliation (
	`affiliation_id` int not null AUTO_INCREMENT,
    `name` varchar(255) not null comment '机构名',
	primary key (`affiliation_id`)
) comment '机构信息表' ;

CREATE TABLE affiliation_rs (
	`affrs_id` int not null AUTO_INCREMENT,
    `affiliation_id` int not null,
    `paper_id` int not null,
	primary key (`affrs_id`)
) comment '机构记录表affiliation_relationship' ;

CREATE TABLE keyword (
	`keyword_id` int not null AUTO_INCREMENT,
    `content` varchar(255) not null comment '内容',
	primary key (`keyword_id`)
) comment '关键词表' ;

CREATE TABLE keyword_rs (
	`krs_id` int not null AUTO_INCREMENT,
    `keyword_id` int not null,
    `paper_id` int not null,
	primary key (`krs_id`)
) comment '关键词记录表keyword_relationship' ;

CREATE TABLE classification (
	`class_id` int not null AUTO_INCREMENT,
    `content` varchar(255) not null comment '内容',
    `note` varchar(255) comment '注释',
	primary key (`class_id`)
) comment '分类号表' ;

CREATE TABLE classification_rs (
	`crs_id` int not null AUTO_INCREMENT,
    `class_id` int not null,
    `paper_id` int not null,
	primary key (`crs_id`)
) comment '分类号记录表classification_relationship' ;

CREATE TABLE fund (
	`fund_id` int not null AUTO_INCREMENT,
    `content` varchar(255) not null comment '内容',
    `type` varchar(255) comment '类型',
	primary key (`fund_id`)
) comment '资助基金表' ;

CREATE TABLE fund_rs (
	`frs_id` int not null AUTO_INCREMENT,
    `fund_id` int not null,
    `paper_id` int not null,
	primary key (`frs_id`)
) comment '资助基金记录表fund_relationship' ;
