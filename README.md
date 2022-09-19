# Fazendinha
Angelina's Farm

### Membros do Grupo

> [Fabricio Bizotto](https://fabricioifc.github.io/horarios/)\
> Matheus Wogt\
> João Danielewicz\
> Angelita Retore\

## ToDo List

- [X] Criar uma tela de `Ambientes` para que seja possível cadastrar cada um dos ambientes
   - [x] name (TEXT) - required
   - [x] status INTEGER (1 para TRUE ou 0 para FALSE) - required (`checkbox`)
> Exemplos: [1 - Horta, 2 - Plantação 2]

 - [x] Criar uma tela de `Instâncias` para que seja possível cadastrar cada uma das caixinhas
   - [x] name (TEXT) - required
   - [x] instance_number (INTEGER) - required
   - [x] status INTEGER (1 para TRUE ou 0 para FALSE) - required (`checkbox`)
> Exemplos: [Transdutor 1, Transdutor 2 ...]

- [x] Criar uma tela de `Recursos` para que seja possível cadastrar cada um dos sensores
   - [x] name (TEXT) - required
   - [x] resource_number (INTEGER) - required
   - [x] vlini (REAL) - required
   - [x] vlfim (REAL) - required (deve ser maior que o inicial)
> Exemplos: [(3304, 'Umidade do Ar', 0, 100), (3304, 'Temperatura', 0, 40)]

 Link para o site de IPSO numbers <https://techlibrary.hpe.com/docs/otlink-wo/IPSO-Object-Reference-Guide.html>