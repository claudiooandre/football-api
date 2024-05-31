SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema football
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `football` ;
USE `football` ;

-- -----------------------------------------------------
-- Table `football`.`season`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`season` (
  `season_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `start` INT NOT NULL,
  `end` INT NOT NULL,
  PRIMARY KEY (`season_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `football`.`season_league_relation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`season_league_relation` (
  `season_id` INT,
  `league_id` INT,
  PRIMARY KEY (`season_id`,`league_id`));

-- -----------------------------------------------------
-- Table `football`.`league`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`league` (
  `league_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `league` VARCHAR(50) NOT NULL,
  `country` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`league_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `football`.`league_team_relation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`league_team_relation` (
  `league_id` INT,
  `team_id` INT,
  PRIMARY KEY (`league_id`,`team_id`));
  
-- -----------------------------------------------------
-- Table `football`.`team`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`team` (
  `team_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `team` VARCHAR(50) NOT NULL,
  `country` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`team_id`))
ENGINE = InnoDB
AUTO_INCREMENT =1
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `football`.`team_athletes_relation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`team_athletes_relation` (
  `team_id` INT,
  `athletes_id` INT,
  PRIMARY KEY (`team_id`,`athletes_id`));
  
-- -----------------------------------------------------
-- Table `football`.`athletes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`athletes` (
  `athletes_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `birth day` INT NULL,
  `weight` INT NULL,
  `tall` INT NULL,
  `position` VARCHAR(45) NOT NULL,
  `foot` VARCHAR(45) NOT NULL,
  `country` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`athletes_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8
COMMENT = 'Table storing all customers. Holds foreign keys to the address table and the store table where this customer is registered.\n\nBasic information about the customer like first and last name are stored in the table itself. Same for the date the record was created and when the information was last updated.';

-- -----------------------------------------------------
-- Table `football`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`users` (
  `users_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`users_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = utf8;

USE `football` ;
