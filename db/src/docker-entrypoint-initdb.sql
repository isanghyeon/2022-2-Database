# Author: Sang Hyeon Lee
# Date: 2022.11.25
# Description: 
# 

CREATE TABLE IF NOT EXISTS `db_shop`.`consumer` (
    idxConsumer          int auto_increment primary key,
    ConsumerEmail        varchar(45)   null,
    ConsumerPWD          char(100)     not null,
    ConsumerName         varchar(45)   not null,
    Address              varchar(100)  null,
    PhoneNumber          varchar(45)   null,
    ClassificationNumber int default 1 null,
    IdentifyNumber       varchar(100)  null,
    LastLogin            datetime      null,
    CreateTime           datetime      not null,
    constraint ClassificationNumber_UNIQUE
        unique (ClassificationNumber),
    constraint ConsumerEmail_UNIQUE
        unique (ConsumerEmail),
    constraint IdentifyNumber_UNIQUE
        unique (IdentifyNumber),
    constraint PhoneNumber_UNIQUE
        unique (PhoneNumber)
)ENGINE = InnoDB CHARACTER SET 'utf8mb4';

CREATE TABLE IF NOT EXISTS `db_shop`.`producer` (
    idxProducer          int auto_increment primary key,
    ProducerEmail        varchar(45)   null,
    ProducerPWD          char(100)     not null,
    ProducerName         varchar(45)   not null,
    Address              varchar(100)  null,
    PhoneNumber          varchar(45)   null,
    ClassificationNumber int default 1 null,
    IdentifyNumber       varchar(100)  null,
    LastLogin            datetime      null,
    CreateTime           datetime      not null,
    constraint ClassificationNumber_UNIQUE
        unique (ClassificationNumber),
    constraint IdentifyNumber_UNIQUE
        unique (IdentifyNumber),
    constraint PhoneNumber_UNIQUE
        unique (PhoneNumber),
    constraint ProducerEmail_UNIQUE
        unique (ProducerEmail)
)ENGINE = InnoDB CHARACTER SET 'utf8mb4';

CREATE TABLE IF NOT EXISTS `db_shop`.`product` (
    idxProduct         int auto_increment           primary key,
    ProductName        varchar(45)                  not null,
    ProductCategory    varchar(45)                  not null,
    ProductID          varchar(45)                  not null,
    ProductRemaining   int unsigned default 0       null,
    ProductCost        int unsigned default 0       null,
    ProductInformation text                         not null,
    ProductImage       longtext collate utf8mb4_bin null,
    ProductOwnerID     varchar(45)                  not null,
    constraint product_ProductID_uindex
        unique (ProductID),
    constraint ProductImage
        check (json_valid(`ProductImage`))
)ENGINE = InnoDB CHARACTER SET 'utf8mb4';

CREATE TABLE IF NOT EXISTS `db_shop`.`cart` (
    idxCart                int auto_increment                       primary key,
    CartProductName        varchar(45)                              not null,
    CartProductCategory    varchar(45)                              not null,
    CartProductID          varchar(45)                              not null,
    CartProductRemaining   int unsigned default 0                   not null,
    CartProductCost        int unsigned default 0                   not null,
    CartProductInformation text                                     not null,
    ProducerIdentifyNumber varchar(100)                             not null,
    ConsumerIdentifyNumber varchar(100)                             not null,
    CartBuyChecked         tinyint(1)   default 0                   null,
    UpdateTimestamp        datetime     default current_timestamp() null
)ENGINE = InnoDB CHARACTER SET 'utf8mb4';