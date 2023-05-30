use monitor

db.createCollection('dados', {
   validator: {
      $jsonSchema: {
         bsonType: 'object',
         required: ['nome', 'login', 'data_cadastro', 'cpf'],
         properties: {
            nome: { bsonType: 'string' },
            login: { bsonType: 'string' },
            data_cadastro: { bsonType: 'date' },
            cpf: { bsonType: 'string' }
         }
      }
   }
})



use monitor

db.dados.insertMany([
   {
      "nome": "João Silva",
      "login": "joao123",
      "data_cadastro": ISODate("2022-10-01"),
      "cpf": "12345678901"
   },
   {
      "nome": "Maria Souza",
      "login": "maria456",
      "data_cadastro": ISODate("2022-11-05"),
      "cpf": "98765432109"
   },
   {
      "nome": "Carlos Santos",
      "login": "carlos789",
      "data_cadastro": ISODate("2022-12-15"),
      "cpf": "45678912304"
   },
   {
      "nome": "Ana Oliveira",
      "login": "ana12",
      "data_cadastro": ISODate("2023-01-08"),
      "cpf": "78901234567"
   },
   {
      "nome": "Pedro Rocha",
      "login": "pedro45",
      "data_cadastro": ISODate("2023-02-20"),
      "cpf": "23456789012"
   },
   {
      "nome": "Mariana Castro",
      "login": "mariana789",
      "data_cadastro": ISODate("2023-03-18"),
      "cpf": "89012345678"
   },
   {
      "nome": "Luiz Mendes",
      "login": "luizmendes",
      "data_cadastro": ISODate("2023-04-09"),
      "cpf": "34567890123"
   },
   {
      "nome": "Fernanda Almeida",
      "login": "feralmeida",
      "data_cadastro": ISODate("2023-05-03"),
      "cpf": "90123456789"
   },
   {
      "nome": "Rafael Lima",
      "login": "rafaellima",
      "data_cadastro": ISODate("2023-06-12"),
      "cpf": "45678901234"
   },
   {
      "nome": "Camila Pereira",
      "login": "camilapereira",
      "data_cadastro": ISODate("2023-07-25"),
      "cpf": "01234567890"
   },
   {
      "nome": "Bruno Carvalho",
      "login": "brunocarvalho",
      "data_cadastro": ISODate("2023-08-30"),
      "cpf": "56789012345"
   },
   {
      "nome": "Larissa Gomes",
      "login": "larissagomes",
      "data_cadastro": ISODate("2023-09-14"),
      "cpf": "12345678901"
   },
   {
      "nome": "Paulo Santos",
      "login": "paulosantos",
      "data_cadastro": ISODate("2023-10-21"),
      "cpf": "78901234567"
   },
   {
      "nome": "Amanda Fernandes",
      "login": "amandafernandes",
      "data_cadastro": ISODate("2023-11-28"),
      "cpf": "23456789012"
   },
   {
      "nome": "Gustavo Costa",
      "login": "gustavocosta",
      "data_cadastro": ISODate("2023-12-05"),
      "cpf": "89012345678"
   },
   {
      "nome": "Isabela Oliveira",
      "login": "isabelaoliveira",
      "data_cadastro": ISODate("2024-01-16"),
      "cpf": "34567890123"
   },
   {
      "nome": "Ricardo Pereira",
      "login": "ricardopereira",
      "data_cadastro": ISODate("2024-02-22"),
      "cpf": "90123456789"
   },
   {
      "nome": "Sara Castro",
      "login": "saracastro",
      "data_cadastro": ISODate("2024-03-11"),
      "cpf": "45678901234"
   },
   {
      "nome": "Lucas Mendonça",
      "login": "lucasmendonca",
      "data_cadastro": ISODate("2024-04-19"),
      "cpf": "01234567890"
   },
   {
      "nome": "Carolina Lima",
      "login": "carolinalima",
      "data_cadastro": ISODate("2024-05-28"),
      "cpf": "56789012345"
   }
]);
