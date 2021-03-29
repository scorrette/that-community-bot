CREATE TABLE IF NOT EXISTS `guilds` (
  `guild_id` bigint UNIQUE PRIMARY KEY NOT NULL,
  `welcome` text(2000),
  `welcome_chn` varchar(100),
  `rules_chn` varchar(100),
  `category_id` bigint,
  `db_role_id` bigint,
  `verify_en` bit(1) NOT NULL DEFAULT 0,
  `delete_log_en` bit(1) NOT NULL DEFAULT 0,
  `edited_log_en` bit(1) NOT NULL DEFAULT 0,
  `join_log_en` bit(1) NOT NULL DEFAULT 0,
  `leave_log_en` bit(1) NOT NULL DEFAULT 0,
  `invite_log_en` bit(1) NOT NULL DEFAULT 0,
  `default_log_en` bit(1) NOT NULL DEFAULT 0,
  `disboard_en` bit(1) NOT NULL DEFAULT 0,
  `counter_verbose` bit(1) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS `prefixes` (
  `guild_id` bigint PRIMARY KEY NOT NULL,
  `prefix` char(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS `counters` (
  `user_id` bigint PRIMARY KEY NOT NULL,
  `word` varchar(255) NOT NULL,
  `count` int NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS `filters` (
  `guild_id` bigint PRIMARY KEY NOT NULL,
  `word` varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS `logs` (
  `guild_id` bigint UNIQUE PRIMARY KEY NOT NULL,
  `delete_msg_chn` varchar(100),
  `edited_msg_chn` varchar(100),
  `join_chn` varchar(100),
  `leave_chn` varchar(100),
  `invite_chn` varchar(100),
  `general_chn` varchar(100)
);

CREATE TABLE IF NOT EXISTS `muted_users` (
  `guild_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `end_time` timestamp NOT NULL,
  PRIMARY KEY (`guild_id`, `user_id`)
);

CREATE TABLE IF NOT EXISTS `levels` (
  `guild_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `level` int NOT NULL DEFAULT 0,
  `experience` int NOT NULL DEFAULT 0,
  PRIMARY KEY (`guild_id`, `user_id`)
);

CREATE TABLE IF NOT EXISTS `autoroles` (
  `guild_id` bigint PRIMARY KEY NOT NULL,
  `role_id` bigint NOT NULL
);

CREATE TABLE IF NOT EXISTS `role_assign` (
  `guild_id` bigint PRIMARY KEY NOT NULL,
  `message_id` bigint NOT NULL,
  `emoji_id` bigint NOT NULL,
  `role_id` bigint NOT NULL
);

CREATE TABLE IF NOT EXISTS `custom_commands` (
  `guild_id` bigint PRIMARY KEY NOT NULL,
  `command` varchar(255) NOT NULL,
  `output` text(2000) NOT NULL
);

CREATE TABLE IF NOT EXISTS `polls` (
  `guild_id` bigint PRIMARY KEY NOT NULL,
  `message_id` bigint NOT NULL,
  `multiselect` bit(1) NOT NULL DEFAULT 1,
  `change_choice` bit(1) NOT NULL DEFAULT 1,
  `end_time` timestamp,
  `option1` int NOT NULL DEFAULT 0,
  `option2` int NOT NULL DEFAULT 0,
  `option3` int NOT NULL DEFAULT 0,
  `option4` int NOT NULL DEFAULT 0,
  `option5` int NOT NULL DEFAULT 0,
  `option6` int NOT NULL DEFAULT 0,
  `option7` int NOT NULL DEFAULT 0,
  `option8` int NOT NULL DEFAULT 0,
  `option9` int NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS `name_history` (
  `user_id` bigint PRIMARY KEY NOT NULL,
  `name` varchar(1000) NOT NULL,
  `time_changed` timestamp
);

CREATE TABLE IF NOT EXISTS `nickname_history` (
  `guild_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `name` varchar(1000) NOT NULL,
  `time_changed` timestamp,
  PRIMARY KEY (`guild_id`, `user_id`)
);

CREATE TABLE IF NOT EXISTS `mutes` (
  `guild_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `reason` varchar(3000) NOT NULL,
  `time` timestamp,
  PRIMARY KEY (`guild_id`, `user_id`)
);

CREATE TABLE IF NOT EXISTS `kicks` (
  `guild_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `reason` varchar(3000) NOT NULL,
  `time` timestamp,
  PRIMARY KEY (`guild_id`, `user_id`)
);

CREATE TABLE IF NOT EXISTS `bans` (
  `guild_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `reason` varchar(3000) NOT NULL,
  `time` timestamp,
  PRIMARY KEY (`guild_id`, `user_id`)
);

CREATE TABLE IF NOT EXISTS `tickets` (
  `id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `guild_id` bigint NOT NULL,
  `channel_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `create_time` timestamp NOT NULL,
  `close_time` timestamp NOT NULL
);

CREATE TABLE IF NOT EXISTS `messages` (
  `ticket_id` int PRIMARY KEY NOT NULL,
  `user_id` bigint NOT NULL,
  `message` varchar(3000) NOT NULL,
  `time_sent` timestamp NOT NULL
);

CREATE UNIQUE INDEX `muted_users_index_0` ON `muted_users` (`guild_id`, `user_id`);

CREATE UNIQUE INDEX `levels_index_1` ON `levels` (`guild_id`, `user_id`);

CREATE UNIQUE INDEX `custom_commands_index_2` ON `custom_commands` (`guild_id`, `command`);

CREATE UNIQUE INDEX `prefixes_index_3` ON `prefixes` (`guild_id`, `prefix`);