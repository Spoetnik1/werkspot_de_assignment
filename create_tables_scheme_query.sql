CREATE SCHEMA IF NOT EXISTS `professional_activity`;

USE `professional_activity`;

CREATE TABLE IF NOT EXISTS `professionals`.`event_log` (
  `event_id` INT NOT NULL,
  `event_type` VARCHAR(45) NOT NULL,
  `prof_id_anonymized` INT NOT NULL,
  `time_stamp` VARCHAR(45) NOT NULL,
  `meta_data` VARCHAR(200) NULL,
  PRIMARY KEY (`event_id`),
  UNIQUE INDEX `event_id_UNIQUE` (`event_id` ASC) VISIBLE);

-- CREATE TABLE IF NOT EXISTS `professional_activity`.`event_type_ids` (
--        `event_type_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
--        `event_type` VARCHAR(255) NOT NULL,
--        PRIMARY KEY (`event_type_id`), 
--        INDEX(`event_type_id`));

CREATE TABLE IF NOT EXISTS `professional_activity`.`account_status_events` (
        `event_id` INT NOT NULL,
        `event_type` VARCHAR(255) NOT NULL,
        `prof_id_anonymized` VARCHAR(255) NOT NULL,
        `time_stamp` VARCHAR(255) NOT NULL,
        PRIMARY KEY (`event_id`));
        
CREATE TABLE IF NOT EXISTS `professional_activity`.`services_info` (
        `service_id` INT NOT NULL,
        `name_nl` VARCHAR(255) NOT NULL,
        `name_en` VARCHAR(255) NOT NULL,
        PRIMARY KEY (`service_id`));
        
CREATE TABLE IF NOT EXISTS `professional_activity`.`proposal_events` (
        `event_id` INT NOT NULL,
        `prof_id_anonymized` VARCHAR(255) NOT NULL,
        `service_id` VARCHAR(255) NOT NULL,
        `lead_fee` FLOAT NOT NULL,
        `time_stamp` VARCHAR(255) NOT NULL,
        PRIMARY KEY (`event_id`));