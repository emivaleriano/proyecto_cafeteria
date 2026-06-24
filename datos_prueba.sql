

INSERT INTO `franjas_horarias` VALUES
(12,1,'08:00:00','13:00:00'),
(13,1,'15:00:00','20:00:00'),
(14,2,'08:00:00','20:00:00'),
(15,3,'08:00:00','20:00:00'),
(16,4,'08:00:00','22:00:00'),
(17,5,'08:00:00','22:00:00');


INSERT INTO `menu` VALUES
(1,'Tostado de Jamón y Queso','Pan de campo tostado con jamón y queso',8500.00,'Sandwiches','[\"contiene gluten\", \"contiene lacteos\"]','https://acdn-us.mitiendanube.com/stores/480/355/products/tostadas-jq1-d2c40500309175ab1315119478812711-640-0.webp',1),
(3,'Cheesecake de Frutos Rojos','Cheesecake artesanal con salsa de frutos rojos',6500.00,'Postres','[\"vegetariano\", \"contiene lacteos\"]','https://farchioni1780.com/cdn/shop/articles/cheesecake-senza-burro_4dba1f5b-8ca4-4a4d-8217-6bb590d6c353.jpg?v=1748596863',1),
(4,'Latte','Café espresso con leche vaporizada',3500.00,'Bebidas','[\"vegetariano\", \"contiene leche\"]','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTR8Q_RrELDLpBSuhHF9CEAWgSBo9mRQtSy-g&s',1),
(5,'Brownie Sin TACC','Brownie de chocolate apto celíacos',5800.00,'Postres','[\"sin tacc\", \"vegetariano\"]','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZTerEmJ5Z9tJee11PvNrc4_j2zESBF14mfQ&s',1),
(6,'Cappuccino','Espresso con leche vaporizada y abundante espuma de leche.',4000.00,'Bebidas','[\"contiene leche\"]','https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Cappuccino_at_Sightglass_Coffee.jpg/1280px-Cappuccino_at_Sightglass_Coffee.jpg',1),
(7,'Americano','Espresso diluido con agua caliente, de sabor suave, aroma intenso y cuerpo ligero.',4700.00,'Bebidas','[\"contiene leche\"]','https://www.somoselcafe.com.ar/img/novedades/47.jpg',1),
(8,'Sandwich de queso y tomate','Pan de campo con tomate y queso',7800.00,'Sandwiches','[\"vegetariano\"]','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5FZdeTCIUIKCirOMpq2xcm4z7k-bhfEp9zQ&s',1);


INSERT INTO `resenas` VALUES (1,1,5,'Excelente atención y ambiente muy agradable.','2026-06-23 11:57:55'),
(2,2,4,'Buen servicio aunque hubo algo de demora.','2026-06-23 11:57:55'),
(3,3,5,'La celebración salió perfecta.','2026-06-23 11:57:55'),
(4,4,4,'Muy cómodo para trabajar.','2026-06-23 11:57:55');


INSERT INTO `reservas` VALUES (1,1,'2026-07-05 10:00:00','2026-06-23 11:57:55',2,'[2]','Mesa cerca de la ventana','Confirmada','QR-RES-0001'),
(2,2,'2026-07-06 13:00:00','2026-06-23 11:57:55',4,'[4]','Almuerzo laboral','Pendiente','QR-RES-0002'),
(3,3,'2026-07-07 17:00:00','2026-06-23 11:57:55',6,'[1]','Celebración familiar','Completada','QR-RES-0003'),
(4,4,'2026-07-08 11:30:00','2026-06-23 11:57:55',1,'[2, 3]','Necesita enchufe cercano','Confirmada','QR-RES-0004'),
(5,5,'2026-07-09 20:00:00','2026-06-23 11:57:55',3,'[5]','Primera visita','Cancelada','QR-RES-0005'),
(6,6,'2026-06-25 17:00:00','2026-06-23 12:01:56',3,'[\"3\"]','','Pendiente','597f2012-388d-4823-a865-a46fe4d46f23'),
(7,6,'2026-06-23 10:00:00','2026-06-23 23:47:52',4,'[\"1\"]','','Completada','ce634cf1-6b5a-4183-ae81-2687635ac5b8'),
(8,6,'2026-06-23 11:00:00','2026-06-23 23:54:08',5,'[]','','Completada','de239f69-1a44-4e75-9a0c-6d734af8a665'),
(9,6,'2026-06-23 13:00:00','2026-06-23 23:58:35',5,'[]','','Completada','8809a5d7-4051-43a2-8fb1-033363a13dba');


INSERT INTO `servicios` VALUES (1,'Cumpleaños','Decoración y reserva para festejos de cumpleaños',1),
(2,'WiFi Premium','Acceso a red de alta velocidad',1),
(3,'Espacio de Trabajo','Mesa equipada para trabajo remoto',1),
(4,'Menú Ejecutivo','Menú especial para almuerzo',1);


INSERT INTO `usuarios` VALUES (1,'juan.perez@gmail.com','Juan Pérez','+54 11 1234-5678'),
(2,'maria.gomez@gmail.com','María Gómez','+54 11 2345-6789'),
(3,'carlos.lopez@gmail.com','Carlos López','+54 11 3456-7890'),
(4,'ana.martinez@gmail.com','Ana Martínez','+54 11 4567-8901'),
(5,'lucia.fernandez@gmail.com','Lucía Fernández','+54 11 5678-9012'),
(6,'stoledo@fi.uba.ar','sofia','1121575358');
