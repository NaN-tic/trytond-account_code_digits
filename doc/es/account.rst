#:after:account/account:paragraph:plan_contable#

Así mismo, podremos indicar el número de dígitos de los códigos de las cuentas 
contables, tanto en la creación como en la actualización de cuentas contables.


#:before:account/account:section:impuestos#

Si ya tenemos creado un plan de cuentas y queremos modificar (expandir o reducir) 
el número de dígitos deberemos de ejecturar de nuevo, manualmente, el asistente, 
este número de ceros dependerá de la plantilla de cuentas contables. Así por 
ejemplo, en un plan contable de ocho dígitos:

 * Si ponemos el código *4300* nos añadirá cuatro ceros al final, 43000000
 * Y si introducimos el código *430%1* nos reemplazará el % por ceros hasta llegar 
   los ocho dígitos, 43000001.
