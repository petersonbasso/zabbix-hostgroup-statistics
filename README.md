# Monitoramento Hostgroup Statistics

Monitoria de estatísitcas de hostgroup Zabbix.

## Introdução

Coleta informações por hostgroup no Zabbix:  
Total de Hosts  
Hosts Down  
Hosts UP  
Disponibilidade Hosts  

### Funcionamento
Monitoria composta por 1 regra de descoberta LLD com 4 protótipos de itens:

* discovery hostgroup:
	* Regra de descoberta do tipo external check.
	* Key => discovery_hostgroups.py["discovery"]  

* Hosts Total
	* Type: External Check
	* Key: discovery_hostgroups.py["coleta","{#GROUPID}"]
* Hosts UP:
	* Type: Zabbix Aggregate
	* Key: grpsum[{#GROUPNAME},"icmpping",last,0]
* Hosts DOWN:
	* Type: Calculated
	* Key: hosts.down[{#GROUPNAME}]
	* Formula: last("discovery_hostgroups.py[\"coleta\",\"{#GROUPID}\"]")-last("grpsum[{#GROUPNAME},\"icmpping\",last,0]")
* GRUPO - Disponibilidade:
	* Type: Zabbix Aggregate
	* Key: grpavg[{#GROUPNAME},"icmpping",avg,10m]	

### Dependências

#### Python libs
pyzabbix  
click

### Instalação

Executar comandos para instalação das dependências  
`pip install pyzabbix`  
`pip install click`

1. Copiar script [discovery_hostgroups.py](discovery_hostgroups.py) para pasta externalscript do Zabbix.  
2. Parametrizar variáveis de conexão à API Zabbix no script.  
3. Importar o template para o Zabbix.
4. Aplicar template a um host que irá concentrar as informações de estatistica.
5. Configurar Filtro da regra de descoberta LLD, filtrando somente os grupos que necessitam dessa informação.

### Resultado esperado

A monitoria cria 1 application para cada grupo retornado pela regra de descoberta, cada application possui 4 itens:  
**Hosts Total** - Quantidade total de hosts no grupo  
**Hosts UP** - Quantidade total de hosts UP no grupo  
**Hosts Down** - Quantidade total de hosts down no grupo  
**Grupo - disponibilidade** - Média das disponibilidades icmpping de todos os Hosts do grupo  

![Resultado](img/imagem01.png)

### Testando o script manualmente

É possível validar o funcionamento do script manualmente utilizando os comandos abaixo.  
**Processo de discovery**  
`./discovery_hostgroups.py discovery`  
Esse comando deverá retornar um json contendo todos os grupos criados no Zabbix.  

**Processo de coleta**  
`./discovery_hostgroups.py coleta --groupid {#GROUPID}`  
Esse comando deverá retornar um valor inteiro contento a quantidade total de hosts no id de grupo informado em {#GROUPID}.  
