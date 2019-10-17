CREATE TABLE `byr_post_detail` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `post_id` varchar(255) NOT NULL COMMENT '帖子id',
  `title` varchar(255) NOT NULL COMMENT '帖子标题',
  `author` varchar(255) NOT NULL COMMENT '作者',
  `pub_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发帖时间',
  `broad` varchar(255) NOT NULL COMMENT '帖子板块',
  `link` varchar(255) NOT NULL COMMENT '帖子链接',
  `current_date` varchar(255) NOT NULL COMMENT '上十大日期',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `description` text COMMENT '内容',
  PRIMARY KEY (`id`),
  KEY `INDEX_POST_ID` (`post_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='北邮人论坛十大帖子详情';


CREATE TABLE `byr_post_reply_count` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `post_id` varchar(255) NOT NULL COMMENT '帖子id',
  `reply_count` int(8) NOT NULL COMMENT '回复数',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `byr_user_info` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` varchar(255) NOT NULL COMMENT '用户论坛id',
  `face_url` varchar(1024) DEFAULT NULL COMMENT '论坛头像',
  `user_name` varchar(255) DEFAULT NULL COMMENT '用户名称',
  `level` varchar(255) DEFAULT NULL COMMENT '论坛等级',
  `life` int(10) DEFAULT NULL COMMENT '生命力',
  `score` int(10) DEFAULT NULL COMMENT '积分',
  `post_count` int(10) DEFAULT NULL COMMENT '帖子总数',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `INDEX_USER_ID` (`user_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='北邮人论坛用户信息';