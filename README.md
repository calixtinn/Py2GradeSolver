Esta é uma aplicação desenvolvida em Python 3.5
que utiliza conceitos de banco de dados, programação multithread e ma-
temática básica.
Tem como objetivo receber do usuário os coeficientes de uma equação do
segundo grau, do tipo ax 2 + bx + c, calcular o seu resultado salvando em um
banco de dados local, e posteriormente em um arquivo texto, permitindo o
usuário que exiba os resultados na tela se desejar.
A escolha de unir estes três conceitos dentro de uma aplicação, moveu-
se a partir da execução eficiente de um código. Pois, não é necessário, por
exemplo, que o programa, só depois de ter recebido os dados do usuário,
comece a executar uma outra ação. Neste caso, o usuário entra com os três
coeficientes (a,b,c) e depois lhe é perguntado se deseja calcular outra equação.
Durante esse tempo, a parte do cálculo já pode ser executada, mesmo que o
usuário decida entrar com mais dados.